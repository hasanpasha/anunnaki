from PySide6.QtCore import QObject, Signal

class MainModel(QObject):
    extensions_changed = Signal(list)
    
    __extensions: list = []

    def __init__(self):
        super().__init__()

    @property
    def extensions(self) -> list:
        return self.__extensions
    
    @extensions.setter
    def extensions(self, extensions: list):
        self.__extensions = extensions
        self.extensions_changed.emit(self.extensions)