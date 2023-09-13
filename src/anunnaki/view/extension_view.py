from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import QModelIndex, Qt, Signal

from anunnaki.view.extensions_ui import Ui_ext_widget
from anunnaki.model.models import Extension
from anunnaki.view.spinnerwidget import QtWaitingSpinner

import enum
import logging

class ExtensionRoles(enum.IntEnum):
    ExtensionDataRole = 1

class ExtensionsView(QWidget):
    open_source = Signal(Extension)

    __operating = []

    def __init__(self, controller, model, parent: QWidget = None):
        super().__init__(parent)

        self.__ui = Ui_ext_widget()
        self.__ui.setupUi(self)

        self.__controller = controller
        self.__model = model

        self.spinner = QtWaitingSpinner(parent, True, True, Qt.ApplicationModal)
        
        # Ext Ui
        self.__ui.ext_tabs.currentChanged.connect(self.on_ext_tabs_switch)
        self.__ui.extensions_list.clicked.connect(self.on_extension_click)
        self.__ui.extensions_list.currentRowChanged.connect(self.on_extension_row_changed)

        self.__ui.sources_list.clicked.connect(self.on_source_clicked)

        self.__ui.ext_install.clicked.connect(self.install_extension)
        self.__ui.ext_uninstall.clicked.connect(self.uninstall_extension)
        self.__ui.ext_update.clicked.connect(self.update_extension)
        self.__ui.ext_refresh.clicked.connect(self.refresh_extensions)

        self.__model.sources_changed.connect(self.on_sources_update)
        self.__model.extensions_changed.connect(self.on_extensions_update)
        self.__model.operation_ended.connect(self.on_operation_end)
        self.__model.error_occured.connect(self.on_error)
        self.__model.loading.connect(self.update_loading)

    def update_loading(self, loading: bool):
        if loading:
            self.spinner.start()
        else:
            self.spinner.stop()

    def on_error(self, error):
        logging.error(error)
        QMessageBox.critical(self, "error", error)

    def on_extension_row_changed(self, row):
        item = self.__ui.extensions_list.item(row)
        if item:
            data: Extension = item.data(ExtensionRoles.ExtensionDataRole)
            logging.debug(data)
            installing = False
            for op in self.__operating:
                if op[1].row() == row:
                    installing = True
                    break
            
            self.update_loading(installing)
            self.__ui.ext_install.setEnabled((not data.installed) & (not installing))
            self.__ui.ext_uninstall.setEnabled(data.installed & (not installing))
            self.__ui.ext_update.setEnabled(data.has_new_update & (not installing))

    def on_extension_click(self, index: QModelIndex):
        data = index.data(ExtensionRoles.ExtensionDataRole)
        installing = False
        for ext, indx in self.__operating:
            if ext == data:
                installing = True
                break
        
        self.update_loading(installing)
        self.__ui.ext_install.setEnabled((not data.installed) & (not installing))
        self.__ui.ext_uninstall.setEnabled(data.installed & (not installing))
        self.__ui.ext_update.setEnabled(data.has_new_update & (not installing))

    def on_source_clicked(self, index: QModelIndex):
        extension = index.data(ExtensionRoles.ExtensionDataRole)
        if extension:
            self.open_source.emit(extension)

    def on_operation_end(self, ext: Extension):
        for op in self.__operating:
            ext, indx = op
            if ext == ext:
                self.__operating.remove(op)
                break

    def set_extension_buttons_enable(self, enabled: bool = False):
        self.__ui.ext_install.setEnabled(enabled)
        self.__ui.ext_uninstall.setEnabled(enabled)
        self.__ui.ext_update.setEnabled(enabled)
    
    def install_extension(self):
        indx = self.__ui.extensions_list.currentIndex()
        if indx:
            self.set_extension_buttons_enable()
            ext = indx.data(ExtensionRoles.ExtensionDataRole)
            self.__operating.append((ext, indx))
            self.__controller.install_extension(ext)

    def uninstall_extension(self):
        indx = self.__ui.extensions_list.currentIndex()
        if indx:
            self.set_extension_buttons_enable(False)
            ext = indx.data(ExtensionRoles.ExtensionDataRole)
            self.__operating.append((ext, indx))
            self.__controller.uninstall_extension(ext)

    def update_extension(self):
        indx = self.__ui.extensions_list.currentIndex()
        if indx:
            self.set_extension_buttons_enable(False)
            ext = indx.data(ExtensionRoles.ExtensionDataRole)
            self.__operating.append((ext, indx))
            self.__controller.update_extension(ext)

    def refresh_extensions(self):
        self.__controller.load_extensions(True)

    def on_extensions_update(self, exts: list[Extension]):
        self.__ui.extensions_list.clear()

        for ext in exts:
            item = QListWidgetItem(ext.name)
            item.setData(ExtensionRoles.ExtensionDataRole, ext)
            self.__ui.extensions_list.addItem(item)  

    def on_sources_update(self, sources: list[Extension]):
        self.__ui.sources_list.clear()

        for source in sources:
            item = QListWidgetItem(source.name)
            item.setData(ExtensionRoles.ExtensionDataRole, source)
            self.__ui.sources_list.addItem(item)

    def on_ext_tabs_switch(self, tab_indx: int):
        EXT_TAB_SOURCES = 0
        EXT_TAB_EXTENSIONS = 1

        if tab_indx == EXT_TAB_SOURCES:
            self.__controller.load_sources()

        elif tab_indx == EXT_TAB_EXTENSIONS:
            self.__controller.load_extensions()

        else:
            raise NotImplemented("tab's functionality is not implemented yet")
