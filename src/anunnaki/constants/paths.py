from PySide6.QtCore import QDir, QStandardPaths
from enum import Enum
import os
import logging


class Paths(Enum):
    DATA_PATH = "data"
    DOWNLOAD_PATH = "download"
    EXTENSIONS_PATH = "extensions"

def get_path(type: Paths) -> str:
    if type == Paths.DATA_PATH:
        path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    elif type == Paths.DOWNLOAD_PATH:
        path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
    elif type == Paths.EXTENSIONS_PATH:
        path = os.path.join(QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation), type.value)
    else:
        path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericDataLocation)

    # make path if not exist
    dir = QDir(path)
    if not dir.exists():
        logging.debug(f"making path: {dir.absolutePath()}")
        dir.mkpath(dir.absolutePath())

    print(path)
    return path

class AppPaths:
    def __init__(self) -> None:
        self.DATA_PATH = get_path(Paths.DATA_PATH)
        self.EXTENSIONS_PATH = get_path(Paths.EXTENSIONS_PATH)
        self.DOWNLOAD_PATH = get_path(Paths.DOWNLOAD_PATH)

        