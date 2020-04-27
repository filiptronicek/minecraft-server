from typing import Optional

import requests

from versions.version import Version


class PaperMC(Version):
    def __init__(self, main_link: Optional[str] = None):
        super().__init__(main_link=main_link or "https://papermc.io")

    def get_download_url(self, mc_version: str) -> str:
        data = requests.get("https://papermc.io/api/v1/paper/")
        version = list(filter(lambda a: a == mc_version, data.json()["versions"]))[0]
        latest_build = requests.get(f"{self.main_link}/api/v1/paper/{version}").json()[
            "builds"
        ]["latest"]
        return f"{self.main_link}/api/v1/paper/{version}/{latest_build}/download"
