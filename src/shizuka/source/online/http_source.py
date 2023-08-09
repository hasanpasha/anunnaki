from requests import Session, Request, Response
from abc import abstractmethod
from typing import Union

from source.source import Source
from source.models import MediasPage, Media, Kind, Season, Episode, Video, Subtitle


class HttpSource(Source):
    name: str
    id: str
    lang: str

    base_url: str
    headers: dict[str, str]
    session: Session

    def fetch_popular_media(self, page: int) -> MediasPage:
        resp = self.session.send(
            self.popular_media_request(page=page).prepare())
        if not resp.ok:
            return MediasPage(medias=[], has_next=False)
        return self.popular_media_parse(response=resp)

    @abstractmethod
    def popular_media_request(self, page: int) -> Request:
        pass

    @abstractmethod
    def popular_media_parse(self, response: Response) -> MediasPage:
        pass

    def get_detail(self, media: Media) -> Media:
        return self.fetch_media_detail(media=media)

    def fetch_media_detail(self, media: Media) -> Media:
        resp = self.session.send(
            self.media_detail_request(media=media).prepare())
        if not resp.ok:
            return media

        return self.media_detail_parse(response=resp)

    @abstractmethod
    def media_detail_request(self, media: Media) -> Request:
        pass

    @abstractmethod
    def media_detail_parse(self, response: Response) -> Media:
        pass

    def get_season_list(self, media: Media) -> Union[list[Season], Episode]:
        if media.is_movie:
            return Episode(episode='0', slang=media.slang, has_next=False)

        return self.fetch_season_list(media=media)

    def fetch_season_list(self, media: Media) -> list[Season]:
        resp = self.session.send(
            self.season_list_request(media=media).prepare())
        if not resp.ok:
            return media

        return self.season_list_parse(response=resp)

    @abstractmethod
    def season_list_request(self, media: Media) -> Request:
        pass

    @abstractmethod
    def season_list_parse(self, response: Response) -> list[Season]:
        pass

    def get_video_list(self, episode: Episode) -> list[Video]:
        return self.fetch_video_list(episode=episode)

    def fetch_video_list(self, episode: Episode) -> list[Video]:
        resp = self.session.send(
            self.video_list_request(episode=episode).prepare())
        if not resp.ok:
            return []

        return self.video_list_parse(response=resp)

    @abstractmethod
    def video_list_request(self, episode: Episode) -> Request:
        pass

    @abstractmethod
    def video_list_parse(self, response: Response) -> list[Video]:
        pass

    def get_subtitle_list(self, episode: Episode) -> list[Subtitle]:
        return self.fetch_subtitle_list(episode=episode)

    def fetch_subtitle_list(self, episode: Episode) -> list[Subtitle]:
        resp = self.session.send(
            self.subtitle_list_request(episode=episode).prepare())
        if not resp.ok:
            return []
        subs = self.subtitle_list_parse(response=resp)
        return subs

    @abstractmethod
    def subtitle_list_request(self, episode: Episode) -> Request:
        pass

    @abstractmethod
    def subtitle_list_parse(self, response: Response) -> list[Subtitle]:
        pass
