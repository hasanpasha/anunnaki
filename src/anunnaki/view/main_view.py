from PySide6.QtWidgets import QMainWindow

from anunnaki.view.main_ui import Ui_MainWindow
from anunnaki.view.extension_view import ExtensionsView
from anunnaki.controller.extension_ctrl import ExtensionsController
from anunnaki.model.extension_model import ExtensionsModel
from anunnaki.view.browse_view import BrowseView
from anunnaki.controller.browse_ctrl import BrowseController, SourceBridge
from anunnaki.model.browse_model import BrowseModel
from anunnaki.view.media_view import MediaView
from anunnaki.controller.media_ctrl import MediaController
from anunnaki.model.media_model import MediaModel
from anunnaki_source.models import Media


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
        self.ui.main.addWidget(self.ext_view)
        
        self.browse_model = BrowseModel()
        self.browse_ctrl = BrowseController(self.browse_model)
        self.browse_view = BrowseView(self.browse_ctrl, self.browse_model, self)
        self.ui.main.addWidget(self.browse_view)

    def on_extensions_clicked(self):
        self.ui.main.setCurrentWidget(self.ext_view)

    def connect_signals(self):
        self.ui.extension_action.triggered.connect(self.on_extensions_clicked)
        self.ui.quit_action.triggered.connect(self.close)

        self.ext_view.open_source.connect(self.on_source_open)

        self.browse_view.open_media.connect(self.on_media_open)

    def on_source_open(self, ext):
        self.ui.main.setCurrentWidget(self.browse_view)
        self.browse_ctrl.open_source(ext)

    def new_media_view(self):
        media_model = MediaModel()
        media_ctrl = MediaController(media_model)
        media_view = MediaView(media_ctrl, media_model, self)
        return media_view

    def on_media_open(self, media: Media, source: SourceBridge):
        media_view = self.new_media_view()
        self.ui.main.addWidget(media_view)
        self.ui.main.setCurrentWidget(media_view)
        media_view.open_media(media, source)