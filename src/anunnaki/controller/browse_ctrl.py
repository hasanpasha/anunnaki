from PySide6.QtCore import QObject

from anunnaki.model.models import Extension
from anunnaki import EXTS_DIR

import logging

class BrowseController(QObject):
    def __init__(self, model):
        super().__init__()

        self.__model = model

    def open_source(self, ext: Extension):
        logging.debug(f"in browse controller {ext.name}")
        