from typing import Optional
from PySide6.QtCore import QObject

class BrowseModel(QObject):
    def __init__(self):
        super().__init__()