from PySide6.QtCore import QObject


class MediaController(QObject):
    def __init__(self, model):
        super().__init__()
        self.__model = model