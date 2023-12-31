from anunnaki.view.main_view import MainView
from anunnaki.controller.main_ctrl import MainController
from anunnaki.model.main_model import MainModel
from anunnaki.constants import AppStrings

from PySide6.QtWidgets import QApplication

class MainApp(QApplication):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setApplicationName(AppStrings.APP_NAME)
        self.setApplicationVersion(AppStrings.APP_VERSION)
        self.model = MainModel()
        self.controller = MainController(self.model)
        self.view = MainView(self.controller, self.model)
        self.view.show()

if __name__ == '__main__':
    app = MainApp()
    app.exec()
    


