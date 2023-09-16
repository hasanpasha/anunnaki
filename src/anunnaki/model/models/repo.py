from dataclasses import dataclass
from anunnaki.model.models.extension import Extension

import logging

@dataclass
class Repo:
    name: str
    url: str

    def index_file(self):
        return f"{self.url}/index.min.json"
    
    def __pkg_name(self, ext: Extension):
        pkg_name = f"{ext.lang}_{ext.pkg}_v{ext.version}"
        logging.debug(pkg_name)
        return pkg_name

    def zip_file(self, ext: Extension):
        return f"{self.__pkg_name(ext)}.zip"
        
    def zip_url(self, ext: Extension):
        return f"{self.url}/zip/{self.zip_file(ext)}"

    def icon_file(self, ext: Extension):
        return f"{self.__pkg_name(ext)}.png"
    
    def icon_url(self, ext: Extension):
        return f"{self.url}/icon/{self.icon_file(ext)}"