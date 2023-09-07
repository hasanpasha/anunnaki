from PySide6.QtCore import QObject


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self.__model = model

    def load_extensions(self):
        print("loading")
        self.__ext_manager.load_local_extensions()
        self.__ext_manager.load_online_extensions()
        self.__ext_manager.check_for_updates()