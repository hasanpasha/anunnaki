from PySide6.QtCore import QObject, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from anunnaki.controller.sql_worker import SQLThread
from anunnaki import DATA_DB, EXTS_DIR
from anunnaki.model.models import Extension, Repo
from anunnaki.controller import repos as repos_loader
from anunnaki.controller.utils.downloader import FileDownloader
from anunnaki.controller.utils.extract_file import extract_file

from typing import Callable

import logging
import json
import os
import shutil

class ExtensionsController(QObject):
    def __init__(self, model):
        super().__init__()

        self.__model = model
        self.__sql_thread = SQLThread(self)

        self.__nam = QNetworkAccessManager(self)
        # TODO: make timeout configurable 
        self.__nam.setTransferTimeout(5000) # 5s 
        self.__nam.finished.connect(self.__collect_replies)

        # print(self.__model.table_exists)
        if not self.__model.table_exists:
            self.setup_table()

    def setup_table(self):
        logging.debug("creating table")
        query = '''CREATE TABLE IF NOT EXISTS extensions(
            id INTEGER NOT NULL PRIMARY KEY UNIQUE,
            pkg TEXT NOT NULL,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            lang TEXT NOT NULL,
            base_url TEXT NOT NULL
        );'''
        self.__sql_thread.execute(DATA_DB, query,
                                  # set the model property to true on success  
                                  lambda _: setattr(self.__model, "table_exists", True),
                                self.__model.emit_error)

    def load_sources(self, force: bool = False):
        if not force and self.__model.sources:
            return
        
        self.__model.start_loading()
        def on_result(result):
            exts = [ExtensionsController.serialize_extension(ext)
                    for ext in result]
            self.__model.sources = exts

        query = '''SELECT * FROM extensions'''
        self.__sql_thread.execute(DATA_DB, query, on_result, self.__model.emit_error)

    def load_extensions(self, force: bool = False):
        if not force and self.__model.extensions:
            return

        self.__model.start_loading()
        repos = repos_loader.load_repos()
        for repo in repos:
            logging.debug(f"loading from {repo.index_file()}")
            request = QNetworkRequest(repo.index_file())
            reply = self.__nam.get(request)
            reply.setProperty('repo', repo)
            reply.errorOccurred.connect(self.__model.emit_error)

    def on_ext_downloaded(self, path, ext: Extension, on_ext_extract: Callable):
        dest = os.path.join(EXTS_DIR, ext.lang, ext.pkg)
        if not extract_file(path, dest):
            self.__model.emit_error(f"failed to unzip the extension {path}")
        on_ext_extract(ext)
        
    def download_extensions(self, ext: Extension, on_download: Callable):
        logging.debug(f"downloading the extensions {ext.name}")
        downloader = FileDownloader(self, self.__nam)
        downloader.finished.connect(on_download)
        downloader.error_occured.connect(self.__model.emit_error)
        downloader.start_download(ext.zip_url)

    def remove_extension_folder(self, ext: Extension) -> bool:
        ext_path = os.path.join(EXTS_DIR, ext.lang, ext.pkg)
        try:
            shutil.rmtree(ext_path)
        except Exception as e:
            self.__model.emit_error(e)
            return False
        else:
            return True

    def add_source(self, ext: Extension):
        query = f'''INSERT INTO extensions(id, pkg, name, lang, version, base_url) 
        VALUES ({ext.id}, "{ext.pkg}", "{ext.name}", "{ext.lang}", "{ext.version}", "{ext.base_url}")'''
        self.__sql_thread.execute(DATA_DB, query, 
                    lambda: self.__model.add_source(ext),
                    lambda error: self.__model.emit_error(error, ext))
        
    def remove_source(self, ext: Extension):
        query = f'''DELETE FROM extensions WHERE id={ext.id};'''
        self.__sql_thread.execute(DATA_DB, query, 
                    lambda: self.__model.remove_source(ext),
                    lambda error: self.__model.emit_error(error, ext))

    def update_source(self, ext: Extension):
        query = f'''UPDATE extensions SET pkg = "{ext.pkg}", name = "{ext.name}", lang = "{ext.lang}",
             version = "{ext.version}", base_url = "{ext.base_url}" WHERE id = {ext.id}'''
        self.__sql_thread.execute(DATA_DB, query, 
                    lambda: self.__model.update_source(ext),
                    lambda error: self.__model.emit_error(error, ext))

    def install_extension(self, ext: Extension):
        def on_ext_downloaded(path):
            dest = os.path.join(EXTS_DIR, ext.lang, ext.pkg)
            if not extract_file(path, dest):
                self.__model.emit_error(f"failed to unzip the extension {path}")
            self.add_source(ext)
        
        self.download_extensions(ext, on_ext_downloaded)
    
    def uninstall_extension(self, ext: Extension):
        if self.remove_extension_folder(ext):
            self.remove_source(ext)

    def update_extension(self, ext: Extension):
        """
        Remove the extension from the disk then download the new one and extract it 
        and update the database at last to the new information of the extension
        """
        assert ext.has_new_update

        def on_ext_downloaded(path):
            dest = os.path.join(EXTS_DIR, ext.lang, ext.pkg)
            if not self.remove_extension_folder(ext):
                return
            if not extract_file(path, dest):
                self.__model.emit_error(f"failed to unzip the extension {path}")
            self.update_source(ext)

        self.download_extensions(ext, on_ext_downloaded)

    def __collect_replies(self, reply: QNetworkReply):
        repo: Repo = reply.property('repo')

        if repo:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                return
            
            logging.debug(f"collecting extensions: {reply.request().url().url()}")
            data = json.loads(reply.readAll().data())
            raw_exts = [ExtensionsController.serialize_extension(ext)
                    for ext in data]
            
            exts = []
            for ext in raw_exts:
                ext.installed = False
                ext.zip_file=repo.zip_file(ext)
                ext.zip_url=repo.zip_url(ext)
                ext.icon_file=repo.icon_file(ext)
                ext.icon_url=repo.icon_url(ext)

                # Check if the extension is installed
                for src in self.__model.sources:
                    if ext == src:
                        ext.installed = True
                        logging.debug("setting installed")
                        if src.is_older_version(ext):
                            ext.has_new_update = True
                            logging.debug("setting new update")
                        break

                exts.append(ext)
            logging.debug(exts)

            self.__model.update_extensions(exts)

    @staticmethod
    def serialize_extension(extension: dict) -> Extension:
        return Extension(**extension)

    