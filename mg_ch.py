#! /usr/bin/python3
"""
Arguments are files to process
"""
import sys
import time

from models import *
from funcs import *


def main():
    start_time = time.time() # for timing
    # Read through logs and process sites as they are found
    sites = SiteList()
    for file in sys.argv[1:]:
        with open(file, "r") as log:
            while True:
            # Go line by line through the log file, enumerating
                line = log.readline()
                if line == "": 
                    break
                pos = log.tell()
            # if line contains STJSVERSION... 
                if "STJSVERSION STJS::N/A::2." in line:
                    # ..and the siteref isn't in sites.get_refs()..
                    match_siteref = re.search(
                        "\s([a-z]+[0-9]+|test_[a-z]+[0-9]+)", line)
                    if match_siteref:
                        siteref = match_siteref.group(1)
                        w_ref = get_wref(line)
                        if sites.does_not_contain(siteref):
                        #   search from this line onwards in lines that have the above wref (max 30 lines)
                            for i in range(20):
                                search_line = log.readline()
                                if w_ref in search_line:
                                    match_iss = re.search(
                                        """(?:'|")iss(?:'|"): u?(?:'|")([^(?:'|")]+)(?:'|")""",
                                        search_line
                                    )
                                    #if iss is found (and is not ppagejwt), add Site to sites with siteref,iss and wref
                                    if match_iss:
                                        iss = match_iss.group(1)
                                        if iss == "ppagejwt":
                                            break
                                        new_site = Site(siteref)
                                        new_site.add_wref(w_ref)
                                        new_site.iss = iss
                                        sites.add(new_site)
                                        print(f"Added {siteref}")
                                        break
                            log.seek(pos)
                        # elif line contains stjsversion and siteref IS in sites.get_refs():
            #   add wref to Site    
                        else:
                            site = sites.get_site(siteref)
                            site.add_wref(w_ref)
    # select all non ppages sites and count how many transactions they processed
    results = {}
    
    # write the results to file
    with open("./migration_output.csv", "w") as file:
        file.write("sitereference,transactions\n")
        for site in sites:
            file.write(f"{site.siteref},{len(site.w_refs)}\n")
    print("*"*40)
    print("Output written to migration_output.csv" + " "*20)
    print(f"Completed in {round(time.time()-start_time)} seconds") # for timing


if __name__=="__main__":
    main()
