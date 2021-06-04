#! /usr/bin/python3

import re, sys

class Site():
    def __init__(self, siteref):
        self.siteref = siteref
        self.iss = "not found"
        self.w_refs = list()


def get_wref(line):
    match = re.search(
        "(W\d{2}-[0-9a-zA-Z]{8})",
        line
    )
    if match:
        return match.group(1)
    else: 
        return ""

def read_log(file):
    print("\nReading " + file)
    sites = list()
    found_siterefs = list()
    lines = list()

    with open(file) as log:
        for line in log:
            wref = get_wref(line)
            lines.append(line)

            if "STJSVERSION STJS::N/A::2." in line:
                match_siteref = re.search(
                    "\s([a-z]+[0-9]+|test_[a-z]+[0-9]+)",
                    line
                )
                if match_siteref:
                    siteref = match_siteref.group(1)
                    if siteref not in found_siterefs:
                        found_siterefs.append(siteref)
                        new_site = Site(siteref)
                        if wref not in new_site.w_refs:
                            new_site.w_refs.append(wref)
                        sites.append(new_site)
                    else:
                        for site in sites:
                            if site.siteref == siteref:
                                if wref not in new_site.w_refs:
                                    new_site.w_refs.append(wref)
    return sites, lines

def process_sites(sites, lines):
    count = 0
    for site in sites:
        found = False
        for wref in site.w_refs:
            for i, line in enumerate(lines):
                if wref in line:
                    match_iss = re.search(
                        # "\"iss\": \"([^\"]*)\", \"payload\"",
                        """(?:'|")iss(?:'|"): (?:u|)(?:'|")([a-zA-Z0-9_@.]+)(?:'|")""",
                        line
                    )
                    if match_iss:
                        iss = match_iss.group(1)
                        site.iss = iss
                        found = True
                if found:
                    lines = lines[i:]
                    break
            if found:
                break
        count += 1    
        print("Processed " + str(count) + "/" + str(len(sites)) + " v2 users", end="\r", flush=True)
    return sites


if __name__ == "__main__":
    sites = list()
    # for each supplied file
    for file in sys.argv[1:]:
        # get a list of all the lines in the log and all the siterefs on v2
        new_sites, lines = read_log(file)
        sites += process_sites(new_sites, lines)

    results = list()
    print("\nThe following sites should migrate:\n")
    for site in sorted(sites, key=lambda s: len(s.w_refs), reverse=True):
        if site.iss != "ppagejwt":
            results.append(site.siteref + ": " + str(len(site.w_refs)))
    
    for i in results:
        print(i)
    
