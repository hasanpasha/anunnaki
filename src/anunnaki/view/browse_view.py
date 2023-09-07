from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QWidget

from anunnaki.view.browser_ui  import  Ui_Form

class BrowseView(QWidget):
    def __init__(self, controller, model, parent) -> None:
        super().__init__(parent)

        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__controller = controller
        self.__model = model