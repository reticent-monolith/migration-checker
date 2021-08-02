#! /usr/bin/python3
"""
First argument is stjs version to search for
Arguments after that are files to search in
e.g.
python mg_ch.py 2 gateway.log gateway2.log
"""
import sys
import time
from models import *
from funcs import *

versions = {
    "2": "STJSVERSION STJS::N/A::2.",
    "1": ""
}


if __name__ == "__main__":
    start_time = time.time() # for timing
    # read and process
    site_list = list() 
    # for all of the selected files
    for file in sys.argv[2:]:
        # get a list of all the lines in the log and a list of all the siterefs on v2
        lines = get_lines(file)
        new_sites = find_sites(lines, versions[sys.argv[1]])
        # give each site its iss and list of wrefs
        site_list += process_sites(new_sites, lines)
    # select all non ppages sites and count how many transactions they processed
    results = dict()
    for site in site_list:
        if site.iss != "ppagejwt":
            if site.siteref not in results.keys():
                results[site.siteref] = len(site.w_refs)
            else:
                results[site.siteref] = results[site.siteref] + len(site.w_refs)
    # write the results to file
    with open("./migration_output.csv", "w") as file:
        file.write("sitereference,transactions\n")
        for site in sorted(results.items(), key=lambda s: s[1]):
            line = f"{site[0]},{site[1]}\n"
            file.write(line)
    print("*"*40)
    print("Output written to migration_output.csv" + " "*20)
    print(f"Completed in {round(time.time()-start_time)} seconds") # for timing