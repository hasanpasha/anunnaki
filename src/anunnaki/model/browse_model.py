from PySide6.QtCore import QObject, Signal

from anunnaki.model.models import Extension
from anunnaki_source.source import Source

class BrowseModel(QObject):
    source_changed = Signal(Extension)
    klass_loaded = Signal(Source)
    
    __source: Extension
    __klass: Source
    
    def __init__(self):
        super().__init__()

    @property
    def source(self) -> Extension:
        return self.__source

    @source.setter
    def source(self, ext: Extension):
        self.__source = ext

        self.source_changed.emit(ext)

    @property
    def klass(self) -> Source:
        return self.__klass
    
    @klass.setter
    def klass(self, klass: Source):
        self.__klass = klass

        self.klass_loaded.emit(self.klass)