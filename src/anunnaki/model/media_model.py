import logging

from PySide6.QtCore import QObject, Signal, QByteArray
from PySide6.QtNetwork import QNetworkReply
from anunnaki.controller.browse_ctrl import SourceBridge
from anunnaki_source.models import Media, Season, Episode, Video, Subtitle


class MediaModel(QObject):
    ready = Signal()
    detail_loaded = Signal(Media)
    poster_loaded = Signal(QByteArray)
    seasons_loaded = Signal(list)
    videos_and_subtitles_loaded = Signal(list, list)
    current_episode_changed = Signal(Episode)

    videos: list[Video] = None
    subtitles: list[Subtitle] = None
    seasons: list[Season] = None
    episodes: list[Episode] = None

    __media: Media = None
    __source: SourceBridge = None
    __seasons_iter: enumerate[Season] = None
    __episodes_iter: enumerate[Episode] = None
    __current_episode: Episode = None

    def __init__(self):
        super().__init__()

    @property
    def media(self) -> Media:
        return self.__media

    @media.setter
    def media(self, media: Media):
        self.__media = media
        if self.media and self.source:
            self.ready.emit()

    @property
    def source(self) -> SourceBridge:
        return self.__source

    @source.setter
    def source(self, source: SourceBridge):
        self.__source = source
        if self.media and self.source:
            self.ready.emit()

    @property
    def current_episode(self):
        if self.__current_episode is None:
            self.set_next_episode()
        return self.__current_episode

    @current_episode.setter
    def current_episode(self, episode: Episode):
        self.__current_episode = episode
        self.current_episode_changed.emit(self.current_episode)

    def set_current_episode_with_index(self, season, episode):
        self.__seasons_iter = enumerate(self.seasons)
        self.__episodes_iter = None
        con = True
        while con:
            season_val = self.next_season()
            if season_val is None:
                break
            season_index, _ = season_val
            if season_index == season:
                con = False
                while True:
                    episode_val = self.next_episode()
                    if episode_val is None:
                        break
                    episode_index, eps = episode_val
                    if episode_index == episode:
                        self.current_episode = eps
                        break

    def set_next_episode(self):
        eps_val = self.next_episode()
        if eps_val is None:
            if self.next_season() is not None:
                eps_val = self.next_episode()
        if eps_val is not None:
            index, episode = eps_val
            self.current_episode = episode

    def next_season(self) -> tuple[int, Season]:
        next_val = next(self.__seasons_iter, None)
        if next_val is not None:
            self.__episodes_iter = enumerate(next_val[1].episodes)
        return next_val

    def next_episode(self) -> tuple[int, Episode]:
        next_val = next(self.__episodes_iter, None)
        return next_val

    def set_next_season_episodes(self):
        season_val = self.next_season()
        if season_val:
            index, season = season_val
            self.episodes = season.episodes
            self.__episodes_iter = enumerate(self.episodes)

    def set_detail(self, media: Media):
        self.__media = self.media + media
        self.detail_loaded.emit(self.media)

    def set_seasons(self, seasons: list[Season]):
        self.seasons = seasons
        self.__seasons_iter = enumerate(self.seasons)
        self.seasons_loaded.emit(self.seasons)
        self.set_next_season_episodes()
        self.set_next_episode()

    def set_poster(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            self.poster_loaded.emit(data)

    def set_videos(self, videos: list[Video]):
        if videos is not None:
            self.videos = videos

        # logging.debug(videos)
        if self.videos is not None and self.subtitles is not None:
            self.videos_and_subtitles_loaded.emit(self.videos, self.subtitles)

    def set_subtitles(self, subtitles: list[Subtitle]):
        if subtitles is not None:
            self.subtitles = subtitles
        else:
            self.subtitles = []

        if self.videos is not None and self.subtitles is not None:
            self.videos_and_subtitles_loaded.emit(self.videos, self.subtitles)