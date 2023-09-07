from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot
from anunnaki.view.main_view_ui import Ui_MainWindow
from anunnaki.view.extension_view import ExtensionsView
from anunnaki.controller.extension_ctrl import ExtensionsController
from anunnaki.model.extension_model import ExtensionsModel

class MainView(QMainWindow):
    def __init__(self, controller, model) -> None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.controller = controller
        self.model = model

        self.build_ui()
        self.connect_signals()

    def build_ui(self):
        self.ext_model = ExtensionsModel()
        self.ext_ctrl = ExtensionsController(self.ext_model)
        self.ext_view = ExtensionsView(self.ext_ctrl, self.ext_model, self)

        self.ui.main.addTab(self.ext_view, "Extensions")
    
    def connect_signals(self):

        # UI signals
        # self.ui.load_extensions.clicked.connect(self.controller.load_extensions)


        # model signals
        self.model.extensions_changed.connect(self.print_exts)

    def print_exts(self, exts):
        print(exts)