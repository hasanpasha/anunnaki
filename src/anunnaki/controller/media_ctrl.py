from PySide6.QtCore import QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from anunnaki.controller.browse_ctrl import SourceBridge

import logging


class MediaController(QObject):
    def __init__(self, model):
        super().__init__()
        self.__model = model

        self.__nam = QNetworkAccessManager(self)

    def set_media(self, media):
        self.__model.media = media

    def set_source(self, source: SourceBridge):
        self.__model.source = source

    def load_detail(self):
        self.__model.source.get_detail(self.__model.media,
                                       on_result=self.__model.set_detail,
                                       on_error=lambda error: logging.error(error))

    def load_seasons(self):
        self.__model.source.get_season_list(self.__model.media,
                                            on_result=self.__model.set_seasons,
                                            on_error=lambda error: logging.error(error))

    def load_videos(self):
        self.__model.source.get_video_list(self.__model.current_episode,
                                           on_result=self.__model.set_videos,
                                           on_error=lambda error: logging.error(error))

    def load_subtitles(self):
        self.__model.source.get_subtitle_list(self.__model.current_episode,
                                              on_result=self.__model.set_subtitles,
                                              on_error=lambda error: logging.error(error))

    def load_poster(self, url: str):
        request = QNetworkRequest(url)
        reply = self.__nam.get(request)
        reply.finished.connect(lambda: self.__model.set_poster(reply))
        reply.errorOccurred.connect(lambda error: logging.debug(error))

    def set_current_episode_playing(self, season: int, episode: int):
        self.__model.set_current_episode_with_index(season, episode)
