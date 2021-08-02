import sys
import re
from progressbar import progressbar as pbar
from models import *
 
def get_wref(line):
    match = re.search(
        "(W\d{2}-[0-9a-zA-Z]{8})",
        line
    )
    if match:
        return match.group(1)
    else:
        # 1/0
        return ""


def get_lines(file) -> list:
    print(f"Importing {file}... ", end="", flush=True)
    lines = list()
    with open(file) as log:
        lines = log.readlines()
    print("Done!")
    return lines

def find_sites(lines):
    """
    get a list of all the lines in the log and all the siterefs on v2
    """
    sites = SiteList()
    w_ref = ""
    for i, line in enumerate(lines):
        # If this line indicates that stjs v2 is being used
        if "STJSVERSION STJS::N/A::2." in line:
            # Get the siteref and w-ref from this line
            match_siteref = re.search(
                "\s([a-z]+[0-9]+|test_[a-z]+[0-9]+)", line)
            if match_siteref:
                siteref = match_siteref.group(1)
                w_ref = get_wref(line)
                # add the Site to sites if new, or add the w_ref if already in list
                if sites.does_not_contain(siteref):
                    new_site = Site(siteref)
                    new_site.add_wref(w_ref)
                    new_site.first_index = i
                    sites.add(new_site)
                else:
                    site = sites.get_site(siteref)
                    site.add_wref(w_ref)
    print(f"Processing {sites.get_total()} sites...\t\t\t\t\t\t")
    return sites


def process_sites(site_list: SiteList, lines):
    """
    For each site in site_list, give it a list of wrefs and an iss
    """
    sites = site_list.get()
    processed_sites = list()
    for _, site in pbar(sites, redirect_stdout=True):
        site = process_site(site, lines)
        processed_sites.append(site)
    print(f"{len(sites)} sites processed!\t\t\t\t\t\t")
    return processed_sites

def process_site(site, lines):
    # Print the current process
    # Flag to end the loop searching for the site's iss
    found = False
    for wref in site.w_refs:
        for line in lines[site.first_index:]: # Only search from first mention of this site
            if wref in line:
                match_iss = re.search(
                    """(?:'|")iss(?:'|"): u?(?:'|")([^(?:'|")]+)(?:'|")""",
                    line
                )
                if match_iss:
                    iss = match_iss.group(1)
                    # Add the iss to the site
                    site.iss = iss
                    # print(f"Found {iss} for {ref}\t\t\t\t\t\t")
                    # Flag that this site is done
                    found = True
                    break
            if found:
                break
        if found:
            break
    return site
    
