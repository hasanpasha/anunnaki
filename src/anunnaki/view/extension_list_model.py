from typing import Any, Union
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from anunnaki.model.models import Extension

import enum

class ExtensionDataRole(enum.IntEnum):
    ExtensionRole = -1

class ExtensionsModel(QAbstractListModel):
    def __init__(self, extensions: list[Extension] = [], parent = None) -> None:
        QAbstractListModel.__init__(self, parent)

        self.__extensions = extensions

    def rowCount(self, parent = None) -> int:
        return len(self.__extensions)
    
    def data(self, index: QModelIndex, role: int):
        row = index.row()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self.__extensions[row].name
        
        elif role == ExtensionDataRole.ExtensionRole:
            return self.__extensions[row]
        
    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        return super().setData(index, value, role)

    def insertRow(self, row: int, parent: QModelIndex = QModelIndex()) -> bool:
        self.beginInsertRows(parent)