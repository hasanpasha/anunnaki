from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QNetworkReply

from anunnaki.model.models import Extension
from anunnaki.controller.browse_ctrl import SourceBridge


class BrowseModel(QObject):
    extension_changed = Signal(Extension)
    source_loaded = Signal(SourceBridge)
    medias_fetched = Signal(object, int)
    repaint_list = Signal(QNetworkReply)
    latest_supported = Signal(bool)
    loading = Signal(bool)

    __extension: Extension
    __source: SourceBridge


    popular_page: int = 1
    search_page: int = 1
    latest_page: int = 1

    popular_has_next: bool = False
    search_has_next: bool = False
    latest_has_next: bool = False

    search_query: str = None

    def __init__(self):
        super().__init__()

    @property
    def source(self) -> SourceBridge:
        return self.__source

    @source.setter
    def source(self, source: SourceBridge):
        self.__source = source

        self.source_loaded.emit(self.source)

    @property
    def extension(self) -> Extension:
        return self.__extension
    
    @extension.setter
    def extension(self, extension: Extension):
        self.__extension = extension

        self.extension_changed.emit(self.extension)

    def popular_medias(self, medias):
        self.popular_has_next = medias.has_next
        self.medias_fetched.emit(medias, 0)

    def search_medias(self, medias):
        self.search_has_next = medias.has_next
        self.medias_fetched.emit(medias, 1)

    def latest_medias(self, medias):
        self.latest_has_next = medias.has_next
        self.medias_fetched.emit(medias, 2)

    def set_loading(self, loading: bool):
        self.loading.emit(loading)

    def set_latest_supported(self, supported: bool):
        self.latest_supported.emit(supported)