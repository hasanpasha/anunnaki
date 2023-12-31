from PySide6.QtCore import QObject, Signal
from anunnaki.model.models import Extension

import logging

class ExtensionsModel(QObject):
    sources_changed = Signal(list)
    extensions_changed = Signal(list)
    operation_ended = Signal(Extension)
    error_occured = Signal(str)
    loading = Signal(bool)

    __sources: list[Extension] = []
    __extensions: list[Extension] = []
    __table_exist: bool = False

    def __init__(self):
        super().__init__()

    @property
    def sources(self):
        return self.__sources if self.__sources != None else []
    
    @sources.setter
    def sources(self, sources: list[Extension]):
        self.__sources = sources
        self.sources_changed.emit(self.sources)
        self.loading.emit(False)

    @property
    def extensions(self):
        return self.__extensions
    
    @extensions.setter
    def extensions(self, exts: list[Extension]):
        self.__extensions = exts
        
        # notify the change
        self.extensions_changed.emit(self.extensions)
        self.loading.emit(False)

    def update_extensions(self, exts: list[Extension]):
        # merge new entry with the current extensions
        current_exts = self.extensions
        for newext in exts:
            for i, ext in enumerate(current_exts):
                if newext == ext:
                    current_exts[i] = newext
                    break
            else:
                current_exts.append(newext)
                
        self.extensions = current_exts
        self.loading.emit(False)

    def mark_extension(self, ext: Extension, installed: bool = None, has_update: bool = None):
        if installed != None:
            ext.installed = installed
        if has_update != None:
            ext.has_new_update = has_update
        self.update_extensions([ext])

    def add_source(self, ext: Extension):
        self.sources.append(ext)
        self.sources_changed.emit(self.sources)

        self.mark_extension(ext, installed=True)
        self.operation_ended.emit(ext)
        self.loading.emit(False)

    def remove_source(self, ext: Extension):
        self.sources.remove(ext)
        self.sources_changed.emit(self.sources)

        self.mark_extension(ext, installed=False)
        self.operation_ended.emit(ext)
        self.loading.emit(False)

    def update_source(self, ext: Extension):
        for i, localext in enumerate(self.sources):
            if localext == ext:
                self.sources[i] = ext
                break
        self.sources_changed.emit(self.sources)

        self.mark_extension(ext, has_update=False)
        self.operation_ended.emit(ext)
        self.loading.emit(False)

    def start_loading(self):
        self.loading.emit(True)

    def emit_error(self, error, ext: Extension = None):
        self.loading.emit(False)
        if ext:
            self.operation_ended.emit(ext)
        self.error_occured.emit(str(error))