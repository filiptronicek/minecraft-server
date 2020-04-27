from typing import Optional

import requests

from versions.version import Version


class Vanilla(Version):
    def __init__(self, main_link: Optional[str] = None):
        super().__init__(main_link=main_link or "https://papermc.io")

    def get_download_url(self, mc_version: str) -> str:
        versions_manifest = requests.get(
            f"{self.main_link}/mc/game/version_manifest.json"
        ).json()
        version_manifest = list(
            filter(lambda a: a["id"] == mc_version, versions_manifest["versions"])
        )[0]
        download_url = requests.get(version_manifest["url"]).json()
        return download_url["downloads"]["server"]["url"]
