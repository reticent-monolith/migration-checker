class Site():
    def __init__(self, siteref):
        self.siteref = siteref
        self.iss = "not found"
        self.w_refs = list()
    
    def __repr__(self):
        return f"{self.siteref} [{self.iss}] - {len(self.w_refs)} w-refs"

    def add_wref(self, wref: str):
        self.w_refs.append(wref)



class SiteList():
    def __init__(self):
        self._sites: dict[str, Site] = dict()

    def get_site(self, siteref: str) -> Site:
        return self._sites[siteref]

    def add(self, site: Site):
        self._sites[site.siteref] = site

    def does_not_contain(self, siteref: str) -> bool:
        return siteref not in self._sites.keys()

    def get(self) -> dict:
        """Returns a dict[str, Site]"""
        return self._sites.items()

    def get_total(self) -> int:
        return len(self._sites.keys())

