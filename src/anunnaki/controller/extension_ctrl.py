from PySide6.QtCore import QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
import tinydb as tdb

from anunnaki.controller.sql_worker import SQLThread
from anunnaki import DATA_DB, EXTS_DIR
from anunnaki.model.models import Extension, Repo
from anunnaki.controller import repos as repos_loader
from anunnaki.utils.downloader import FileDownloader
from anunnaki.utils.extract_file import extract_file

from typing import Callable

import logging
import json
import os
import shutil


class ExtensionsController(QObject):
    def __init__(self, model):
        super().__init__()
        self.__model = model

        # create necessary folder
        self.make_dirs()

        self.__nam = QNetworkAccessManager(self)
        # TODO: make timeout configurable 
        self.__nam.setTransferTimeout(5000)  # 5s
        self.__nam.finished.connect(self.__collect_replies)

        self.load_sources()
        if not self.__model.extensions:
            self.load_extensions(force=True)

    def make_dirs(self):
        """mkdir missing paths"""
        paths = [EXTS_DIR]
        for path in paths:
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except Exception as e:
                    self.__model.emit_error(str(Exception))
                else:
                    logging.info(f"created missing path: {path}")

    def load_sources(self, force: bool = True):
        if not force and self.__model.sources:
            return

        with tdb.TinyDB(DATA_DB) as db:
            table = db.table("extensions")
            sources = [Extension(**ext) for ext in table.all()]
            self.__model.sources = sources

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
        with tdb.TinyDB(DATA_DB) as db:
            table = db.table("extensions")
            table.insert(vars(ext))
            self.__model.add_source(ext)


    def remove_source(self, ext: Extension):
        with tdb.TinyDB(DATA_DB) as db:
            table = db.table("extensions")
            table.remove(tdb.where('id') == ext.id)
            self.__model.remove_source(ext)


    def update_source(self, ext: Extension):
        with tdb.TinyDB(DATA_DB) as db:
            table = db.table("extensions")
            table.update(vars(ext), tdb.where('id') == ext.id)
            self.__model.update_source(ext)

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
                ext.zip_file = repo.zip_file(ext)
                ext.zip_url = repo.zip_url(ext)
                ext.icon_file = repo.icon_file(ext)
                ext.icon_url = repo.icon_url(ext)

                # Check if the extension is installed and has_new_update
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
