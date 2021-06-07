#! /usr/bin/python3

import re, sys, time

class Site():
    def __init__(self, siteref):
        self.siteref = siteref
        self.iss = "not found"
        self.w_refs = list()

class SiteList():
    def __init__(self):
        self.sites = list()
        self.total = len(list())

    def get(self, siteref):
        for site in self.sites:
            if site.siteref == siteref:
                return site

    def append(self, site):
        self.sites.append(site)

    def does_not_contain(self, siteref):
        for site in self.sites:
            if site.siteref == siteref:
                return False
        return True


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

def read_log(file):
    print(f"\nReading {file}")
    sites = SiteList()
    lines = list()
    w_ref = ""

    with open(file) as log:
        for line in log:
            # add this line to the in-memory list of log lines
            lines.append(line)

            # If this line indicates that stjs v2 is being used
            if "STJSVERSION STJS::N/A::2." in line:

                # Get the siteref and w-ref from this line
                match_siteref = re.search("\s([a-z]+[0-9]+|test_[a-z]+[0-9]+)",line)
                if match_siteref:
                    siteref = match_siteref.group(1)
                    w_ref = get_wref(line)

                    if sites.does_not_contain(siteref):
                        new_site = Site(siteref)
                        new_site.w_refs.append(w_ref)
                        sites.append(new_site)
                    else:
                        sites.get(siteref).w_refs.append(w_ref)
    return sites.sites, lines

def process_sites(sites, lines):
    count = 1
    for site in sites:
        
        print(f"Processing ({str(count)}/{str(len(sites))}) {site.siteref}" + " "*20, end="\r")

        found = False
        wref_count = 1
        wref_max = len(site.w_refs)


        for wref in site.w_refs:
            
            # print(f"-- Searching {str(wref_count)}/{str(wref_max)} W-refs", end="\r")

            for i, line in enumerate(lines):
                if wref in line:
                    match_iss = re.search(
                        # "\"iss\": \"([^\"]*)\", \"payload\"",
                        # """(?:'|")iss(?:'|"): (?:u|)(?:'|")([a-zA-Z0-9_@.]+)(?:'|")""",
                        """(?:'|")iss(?:'|"): u?(?:'|")([^(?:'|")]+)(?:'|")""",
                        line
                    )
                    # lines.remove(line)
                    if match_iss:
                        iss = match_iss.group(1)
                        site.iss = iss
                        found = True

                        # print(f"\n##### Found {iss}! #####\n")
                    elif 'Res:{"jwt"' in line:
                        # print(f"Could not locate iss in this: {line}")
                        if "False" in line:
                            site.iss = "False"
                            found = True
                        if "None" in line:
                            site.iss = "None"
                            found = True

                if found:
                    # lines = lines[i:]
                    break
                
            if found:
                break
            wref_count += 1
        count += 1    
    return sites


if __name__ == "__main__":

    start_time = time.time()

    site_list = list()
    for file in sys.argv[1:]:
        # get a list of all the lines in the log and all the siterefs on v2
        new_sites, lines = read_log(file)
        site_list += process_sites(new_sites, lines)

    results = dict()

    for site in site_list:
        if site.iss != "ppagejwt":
            if site.siteref not in results.keys():
                results[site.siteref] = len(site.w_refs)
            else:
                results[site.siteref] = results[site.siteref] + len(site.w_refs)

    with open("./migration_output.txt", "w") as file:
        for site in sorted(results.items(), key=lambda s: s[1]):
            line = f"{site[0]},{site[1]}\n"
            # print(line)
            file.write(line)
    print("Output written to migration_output.txt")


    print(f"\n**********************\n\nCompleted in {round(time.time() - start_time)} seconds")

    # with open("output.txt", "w") as file:
    #     for site in site_list.sites:
    #         string = (
    #             f"Site Reference: {site.siteref}"
    #             f"--- iss: {site.iss}"
    #             f"--- W-refs: {site.w_refs}"
    #             "\n"
    #         )
    #         file.write(string)
                




# (grandseiko84372|ferguson21609|thoburns67261|jksupermarket79545|strawberry38295)