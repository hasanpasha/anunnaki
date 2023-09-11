from PySide6.QtCore import QObject

from anunnaki.model.models import Extension
from anunnaki import EXTS_DIR

from anunnaki_source.source import Source

import importlib
import sys
import os
import logging


class BrowseController(QObject):
    def __init__(self, model):
        super().__init__()

        self.__model = model

    def load_source(self, ext: Extension) -> Source:
        if EXTS_DIR not in sys.path:
            sys.path.append(EXTS_DIR)

        module_name = f"{ext.lang}.{ext.pkg}"

        logging.debug(f"loading {module_name}")
        module = importlib.import_module(module_name)
        klass: Source = module.load_extension()
        logging.debug(f"loaded {klass}")

        self.__model.klass = klass

    def open_source(self, ext: Extension):
        self.__model.source = ext

        logging.debug(f"in browse controller {ext.name}")
        