import logging

from PySide6.QtWidgets import QWidget
from anunnaki.view.media_ui import Ui_media_widget
from anunnaki_source.models import Media

class MediaView(QWidget):
    def __init__(self, controller, model, parent) -> None:
        super().__init__(parent)

        self.__ui = Ui_media_widget()
        self.__ui.setupUi(self)
        self.__controller = controller
        self.__model = model

    def open_media(self, media: Media):
        logging.info(f"media_view {media}")