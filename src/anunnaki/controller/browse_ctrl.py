from typing import Callable, Any

from PySide6.QtCore import QObject, QRunnable, Signal, QThreadPool
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from anunnaki.model.models import Extension
from anunnaki.constants import AppPaths

from anunnaki_source import Source

import importlib
import sys
import logging


class FunctionWrapperSignals(QObject):
    result = Signal(object)
    error = Signal(Exception)

    def __init__(self, parent):
        super().__init__(parent)


class FunctionRunner(QRunnable):
    def __init__(self, parent: QObject, func: Callable, *args, **kwargs):
        super().__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_pool = parent
        self.__signals = FunctionWrapperSignals(parent)

    def on_result(self, func: Callable):
        self.__signals.result.connect(func)

    def on_error(self, func: Callable):
        self.__signals.error.connect(func)

    def start(self):
        self.thread_pool.start(self)

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.__signals.error.emit(e)
        else:
            self.__signals.result.emit(result)

class SourceBridge(QThreadPool):
    def __init__(self, extension: Extension, parent: QObject = None):
        super().__init__(parent)

        self.__extension = extension
        self.__source = SourceBridge.load_source(self.__extension)

    @staticmethod
    def load_source(ext: Extension):
        if AppPaths().EXTENSIONS_PATH not in sys.path:
            sys.path.append(AppPaths().EXTENSIONS_PATH)
        module_name = f"{ext.lang}.{ext.pkg}"
        logging.debug(f"{AppPaths().EXTENSIONS_PATH}, {module_name}")
        module = importlib.import_module(module_name)
        klass = module.load_extension()
        return klass

    @property
    def source_methods(self):
        if not self.__source:
            # TODO: Custom Exception
            raise Exception("Source not available")

        return [method_name for method_name in self.__source.__dir__() if not method_name.startswith('_')]

    @property
    def source_fields(self):
        if not self.__source:
            # TODO: Custom Exception
            raise Exception("Source not available")

        return {
            field
            for c in self.__source.__class__.mro() if hasattr(c, '__annotations__')
            for field in c.__annotations__
        }

    def wrap_with_runner(self, method):
        def wrapper(*args, on_result: Callable = None, on_error: Callable = None, **kwargs):
            worker = FunctionRunner(self, method, *args, **kwargs)
            if on_result:
                worker.on_result(on_result)
            if on_error:
                worker.on_error(on_error)
            self.start(worker)
        return wrapper

    def __getattr__(self, item):
        if item in self.source_fields:
            print(f"returning field {item}")
            field = getattr(self.__source, item)
            return field

        elif item in self.source_methods:
            method = getattr(self.__source, item)
            return self.wrap_with_runner(method)


class BrowseController(QObject):
    def __init__(self, model):
        super().__init__()
        self.__model = model

        self.__nam = QNetworkAccessManager(self)

    def open_source(self, ext: Extension):
        self.__model.extension = ext

    def load_source(self, ext: Extension):
        self.__model.source = SourceBridge(ext, self)
        self.__model.set_latest_supported(self.__model.source.support_latest)

    def load_thumbnail(self, url, title, index):
        reply = self.__nam.get(QNetworkRequest(url))
        reply.setProperty('title', title)
        reply.setProperty('list-index', index)
        reply.finished.connect(lambda: self.__model.repaint_list.emit(reply))
        reply.errorOccurred.connect(lambda error: logging.debug(error))

    def load_popular_medias(self, page: int = None):
        if page:
            self.__nam.autoDeleteReplies()
            self.__model.popular_page = page
        else:
            if not self.__model.popular_has_next:
                return

            self.__model.popular_page += 1
            page = self.__model.popular_page

        logging.debug(f"loading popular {page}")
        self.__model.set_loading(True)
        self.__model.source.fetch_popular_media(page=page, filters=None,
                                                on_result=self.__model.popular_medias,
                                                on_error=lambda error: logging.error(error))

    def load_latest_medias(self, page: int = None, filters = None):
        if page:
            self.__nam.autoDeleteReplies()
            self.__model.latest_page = page
        else:
            if not self.__model.latest_has_next:
                return

            self.__model.latest_page += 1
            page = self.__model.latest_page

        self.__model.set_loading(True)
        self.__model.source.fetch_latest_media(page=page, filters=filters,
                                                on_result=self.__model.latest_medias,
                                                on_error=lambda error: logging.error(error))


    def load_search_medias(self, page: int = None, filters = None):
        if page:
            self.__nam.autoDeleteReplies()
            self.__model.search_page = page
        else:
            if not self.__model.search_has_next:
                return

            self.__model.search_page += 1
            page = self.__model.search_page

        query = self.__model.search_query
        self.__model.set_loading(True)
        self.__model.source.fetch_search_media(query=query, page=page, filters=filters,
                                                on_result=self.__model.search_medias,
                                                on_error=lambda error: logging.error(error))

    def set_search_query(self, query: str):
        self.__model.search_query = query