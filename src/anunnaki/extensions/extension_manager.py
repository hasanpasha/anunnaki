import requests

from anunnaki.extensions.repos import load_repos
from anunnaki.extensions.models import Extension, RepoType
from anunnaki.extensions import svn
from anunnaki.extensions import SOURCES_DIR, INDEX
from anunnaki.data.data import Data
from anunnaki import DATA_DIR, EXTS_DIR

from anunnaki_source.source import Source
import importlib

import os
import sys
import logging


class ExtensionManager:
    extensions = []

    def __init__(self) -> None:
        self.load_local_extensions()
        self.load_online_extensions()

    @property
    def extensions(self) -> list[Extension]:
        return self.__local_extensions

    def load_extension(self, ext: Extension) -> Source:
        if not ext.installed:
            return

        module_name = ext.local_path
        if EXTS_DIR not in sys.path:
            sys.path.append(EXTS_DIR)

        logging.debug(f"loading {module_name}")
        module = importlib.import_module(module_name)

        klass: Source = module.load_extension()
        logging.debug(f"loaded {klass.id}")

        return klass

    def check_for_updates(self) -> bool:
        for online_ext in self.__online_extensions:
            for local_ext in self.__local_extensions:
                if local_ext == online_ext:
                    if local_ext.is_older_version(online_ext):
                        self.__local_extensions.remove(local_ext)
                        local_ext.new_update = online_ext
                        self.__local_extensions.append(local_ext)
            else:
                if online_ext not in self.__local_extensions:
                    self.__local_extensions.append(online_ext)

        self.__save_to_local_db(self.extensions)

    def __save_to_local_db(self, exts: list[Extension]) -> bool:
        for ext in exts:
            with Data() as data:
                if not data.get_extension(ext.id):
                    return bool(data.insert_extension(ext))

                else:
                    return bool(data.update_extension(ext))

    def install_extensions(self, ext: Extension) -> bool:
        if ext.installed:
            return True

        if not self.download_extension(ext):
            return False

        ext.installed = True
        ext.local_path = ext.id.replace('.', '_')

        # update db
        result = self.__save_to_local_db([ext])
        print(result)
        # if updating succeed
        if result:
            logging.debug("reloading after updating")
            self.load_local_extensions()

    def update_extension(self, ext: Extension) -> bool:
        if not ext.has_updates:
            return True
        if not self.download_extension(ext.new_update):
            return False

        ext.version = ext.new_update.version
        ext.name = ext.new_update.name
        ext.base_url = ext.new_update.base_url
        ext.lang = ext.new_update.lang
        ext.repo_type = ext.new_update.repo_type
        ext.new_update = None

        result = self.__save_to_local_db([ext])

        if result:
            self.load_local_extensions()

    def download_extension(self, ext: Extension, force: bool = True) -> bool:

        if not os.path.exists(EXTS_DIR):
            os.mkdir(EXTS_DIR)

        download_path = os.path.join(EXTS_DIR, ext.id.replace('.', '_'))
        if os.path.exists(download_path) and not force:
            return False
        if ext.repo_type == RepoType.GIT:
            logging.debug(f"Downloading using git to {download_path}")
            return svn.export(ext.source_url, output=download_path, force=True)
        else:
            raise NotImplemented("TODO: add http folder download")

    def load_local_extensions(self) -> None:
        logging.debug("loading local db")
        self.__local_extensions = []
        with Data() as data:
            self.__local_extensions = data.list_extensions()

    def load_online_extensions(self) -> None:
        self.__online_extensions = []
        repos = load_repos()

        for repo in repos:
            logging.info(f"loading from {repo.base_url}")

            exts = requests.get(repo.index_url).json()
            for ext in exts:
                self.__online_extensions.append(Extension(
                    id=ext['id'],
                    name=ext['name'],
                    lang=ext['lang'],
                    version=ext['version'],
                    repo_type=repo.repo_type,
                    base_url=ext['base_url'],
                    source_url=repo.source_url + ext['source'],
                ))
