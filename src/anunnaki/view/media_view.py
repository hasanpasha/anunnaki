import logging

from PySide6.QtWidgets import (
    QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QByteArray, Qt

from anunnaki.view.media_ui import Ui_media_widget
from anunnaki_source.models import Media, Kind, Season, Episode, Video, Subtitle
from anunnaki.controller.browse_ctrl import SourceBridge

class MediaView(QWidget):
    def __init__(self, controller, model, parent) -> None:
        super().__init__(parent)

        self.video: Video = None
        self.subtitles: list[Subtitle] = None

        self.__ui = Ui_media_widget()
        self.__ui.setupUi(self)
        self.__controller = controller
        self.__model = model

        self.__ui.play_btn.clicked.connect(self.on_play_btn_clicked)
        self.__ui.videos.currentIndexChanged.connect(self.on_video_reso_changed)

        self.__model.ready.connect(self.on_ready)
        self.__model.detail_loaded.connect(self.on_media_detail_loaded)
        self.__model.poster_loaded.connect(self.on_poster_loaded)
        self.__model.seasons_loaded.connect(self.on_seasons_loaded)
        self.__model.videos_and_subtitles_loaded.connect(self.on_videos_and_subtitles_loaded)
        self.__model.current_episode_changed.connect(self.on_current_episode_changed)


    def on_current_episode_changed(self, episode: Episode):
        self.__ui.play_btn.setEnabled(True)
        self.__controller.load_videos()
        self.__controller.load_subtitles()

    def on_videos_and_subtitles_loaded(self, videos: list[Video], subtitles: list[Subtitle]):
        self.video = None
        self.subtitles = subtitles
        self.__ui.videos.clear()
        for video in videos:
            self.__ui.videos.addItem(video.resolution.value, video)

    def on_video_reso_changed(self, index: int):
        self.video = self.__ui.videos.currentData()

    def on_play_btn_clicked(self):
        import subprocess
        args = ['mpv']
        args.append(self.video.url)

        for subtitle in self.subtitles:
            logging.debug(subtitle)
            args.append(f"--sub-file={subtitle.url}")

        subprocess.run(args)

    def on_ready(self):
        self.__controller.load_detail()

    def on_poster_loaded(self, data: QByteArray):
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.__ui.poster.setPixmap(pixmap.scaled(self.__ui.poster.size(),
                                                 Qt.AspectRatioMode.KeepAspectRatio))

    def on_episode_changed(self, row: int):
        season = self.__ui.seasons_tabs.currentIndex()
        self.__controller.set_current_episode_playing(season, row)

    def on_seasons_loaded(self, seasons: list[Season]):
        for season in seasons:
            tab = QListWidget()
            tab.currentRowChanged.connect(self.on_episode_changed)
            for epi_indx, episode in enumerate(season.episodes):
                item = QListWidgetItem(str(epi_indx))
                item.setData(Qt.ItemDataRole.UserRole, episode)
                tab.addItem(item)
            self.__ui.seasons_tabs.addTab(tab, season.season)

    def on_media_detail_loaded(self, media: Media):
        self.__ui.seasons_tabs.setVisible(media.kind == Kind.SERIES)

        if media.thumbnail_url:
            self.__controller.load_poster(media.thumbnail_url)
        self.__ui.info_layout.addRow("title", QLabel(media.title if media.title else "N/A"))
        self.__ui.info_layout.addRow("kind", QLabel(media.kind.value if media.kind else "N/A"))
        self.__ui.info_layout.addRow("year", QLabel(media.year if media.year else "N/A"))
        desc_label = QLabel(media.description if media.description else "N/A")
        desc_label.setWordWrap(True)
        self.__ui.info_layout.addRow("description", desc_label)
        if media.tags:
            tags = QHBoxLayout()
            for tag in media.tags:
                tags.addWidget(QLabel(tag))
            self.__ui.info_layout.addRow("tags", tags)

        self.__controller.load_seasons()

    def open_media(self, media: Media, source: SourceBridge):
        self.__controller.set_media(media)
        self.__controller.set_source(source)