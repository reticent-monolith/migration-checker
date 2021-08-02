class Site():
    def __init__(self, siteref):
        self.siteref = siteref
        self.iss = "not found"
        self.w_refs = list()

    def add_wref(self, wref: str):
        self.w_refs.append(wref)



class SiteList():
    def __init__(self):
        self.sites: dict[str, Site] = dict()

    def get_site(self, siteref: str):
        return self.sites[siteref]

    def add(self, site: Site):
        self.sites[site.siteref] = site

    def does_not_contain(self, siteref: str):
        return siteref not in self.sites.keys()

    def get(self) -> dict:
        """Returns a dict[str, Site]"""
        return self.sites.items()

    def get_total(self):
        return len(self.sites.keys())

