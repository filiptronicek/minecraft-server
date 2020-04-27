from abc import ABC, abstractmethod


class Version(ABC):
    def __init__(self, main_link):
        self.main_link = main_link

    @abstractmethod
    def get_download_url(self, mc_version: str) -> str:
        pass
