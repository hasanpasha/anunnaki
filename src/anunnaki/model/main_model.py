from PySide6.QtCore import QObject, Signal

class MainModel(QObject):
    def __init__(self):
        super().__init__()