from PySide6.QtCore import Qt, QModelIndex, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QListWidgetItem, QListWidget
from PySide6.QtNetwork import QNetworkReply

from anunnaki.view.browse_ui import Ui_Form
from anunnaki.view.browse_list import BrowseList
from anunnaki.controller.browse_ctrl import SourceBridge
from anunnaki.view.spinnerwidget import QtWaitingSpinner

from anunnaki_source.models import MediasPage, Media

import logging


class BrowseView(QWidget):
    open_media = Signal(Media)

    def __init__(self, controller, model, parent) -> None:
        super().__init__(parent)

        self.TAB_BROWSE_POPULAR = 0
        self.TAB_BROWSE_SEARCH = 1
        self.TAB_BROWSE_LATEST = 2

        self.__ui = Ui_Form()
        self.__controller = controller
        self.__model = model

        self.spinner = QtWaitingSpinner(parent, True, True, Qt.ApplicationModal)

        self.__ui.setupUi(self)

        self.popular_list = BrowseList(self.__ui.popular)
        self.__ui.popular_layout.addWidget(self.popular_list)
        self.latest_list = BrowseList(self.__ui.latest)
        self.__ui.latest_layout.addWidget(self.latest_list)
        self.search_list = BrowseList(self.__ui.search)
        self.__ui.search_layout.addWidget(self.search_list)

        self.popular_list.list_end_reached.connect(lambda: self.load_popular_medias(load_next=True))
        self.latest_list.list_end_reached.connect(lambda: self.load_latest_medias(load_next=True))
        self.search_list.list_end_reached.connect(lambda: self.load_search_medias(load_next=True))

        self.popular_list.clicked.connect(self.on_media_clicked)
        self.latest_list.clicked.connect(self.on_media_clicked)
        self.search_list.clicked.connect(self.on_media_clicked)

        self.__ui.browse_tabs.currentChanged.connect(self.load_medias)
        self.__ui.search_btn.clicked.connect(self.search_query)

        self.__model.extension_changed.connect(self.on_extension_changed)
        self.__model.source_loaded.connect(self.on_source_loaded)
        self.__model.medias_fetched.connect(self.on_medias_fetched)
        self.__model.repaint_list.connect(self.repaint_list)
        self.__model.loading.connect(self.update_loading)
        self.__model.latest_supported.connect(self.update_latest_supported)

    def on_media_clicked(self, index: QModelIndex):
        media: Media = index.data(Qt.ItemDataRole.UserRole)
        if media:
            self.open_media.emit(media)

    def update_latest_supported(self, show: bool):
        logging.debug(f"SHOWING {show}")
        self.__ui.browse_tabs.setTabVisible(self.TAB_BROWSE_LATEST, show)

    def update_loading(self, loading: bool):
        if loading:
            self.spinner.start()
        else:
            self.spinner.stop()

    def list_widget_by_index(self, index: int):
        if index == self.TAB_BROWSE_POPULAR:
            return self.popular_list
        elif index == self.TAB_BROWSE_LATEST:
            return self.latest_list
        elif index == self.TAB_BROWSE_SEARCH:
            return self.search_list
        else:
            raise NotImplementedError()

    def current_list(self):
        return self.list_widget_by_index(self.__ui.browse_tabs.currentIndex())

    def repaint_list(self, reply: QNetworkReply):
        try:
            # TODO: RETRY ON FAILURE
            readable = reply.isReadable()
            if not readable:
                return
            data = reply.readAll()
            if not data:
                return
            title = reply.property('title')
            list_index: int = reply.property('list-index')
            list_widget: QListWidget = self.list_widget_by_index(list_index)
            item: QListWidgetItem = None

            items: list[QListWidgetItem] = list_widget.findItems(title, Qt.MatchFlag.MatchExactly)
            if items:
                item = items[0]
            else:
                logging.error(f"can't find {title}'s item")
            if not item or not list_widget:
                return
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            item.setData(Qt.ItemDataRole.DecorationRole, pixmap)
            list_widget.repaint()
        except Exception as e:
            logging.error(f"error repaint {e}")

    def search_query(self):
        query = self.__ui.search_line.text()
        if query:
            self.__controller.set_search_query(query)
            self.__ui.browse_tabs.setCurrentIndex(self.TAB_BROWSE_SEARCH)
            self.load_search_medias(load_next=False)

    def on_medias_fetched(self, medias_page: MediasPage, index: int):
        current_list = self.list_widget_by_index(index)
        for media in medias_page.medias:
            item = QListWidgetItem(media.title)
            item.setData(Qt.ItemDataRole.UserRole, media)
            self.__controller.load_thumbnail(media.thumbnail_url, media.title, index)
            current_list.addItem(item)

        self.update_loading(False)

    def load_medias(self, load_next: bool = False):
        current = self.__ui.browse_tabs.currentIndex()
        if current == self.TAB_BROWSE_POPULAR:
            self.load_popular_medias(load_next)
        elif current == self.TAB_BROWSE_LATEST:
            self.load_latest_medias(load_next)

    def load_search_medias(self, load_next: bool = False):
        if load_next:
            self.__controller.load_search_medias()
        else:
            self.search_list.clear()
            self.__controller.load_search_medias(page=1)

    def load_popular_medias(self, load_next: bool = False):
        if load_next:
            self.__controller.load_popular_medias()
        else:
            self.popular_list.clear()
            self.__controller.load_popular_medias(page=1)

    def load_latest_medias(self, load_next: bool = False):
        if load_next:
            self.__controller.load_latest_medias()
        else:
            self.latest_list.clear()
            self.__controller.load_latest_medias(page=1)

    def on_extension_changed(self, ext):
        self.__controller.load_source(ext)

    def on_source_loaded(self, source: SourceBridge):
        logging.info(f"loaded {source.name}")

        self.load_medias()