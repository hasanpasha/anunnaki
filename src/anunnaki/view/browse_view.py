from PySide6.QtWidgets import QWidget

from anunnaki.view.browser_ui  import  Ui_Form

from anunnaki_source.source import Source

import logging

class BrowseView(QWidget):
    def __init__(self, controller, model, parent) -> None:
        super().__init__(parent)

        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__controller = controller
        self.__model = model

        self.__model.source_changed.connect(self.on_source_change)
        self.__model.klass_loaded.connect(self.on_klass_loaded)

    def on_source_change(self, ext):
        self.__controller.load_source(ext)

    def on_klass_loaded(self, klass: Source):
        logging.debug(f"loaded {klass.fetch_search_media('hello', 1)}")