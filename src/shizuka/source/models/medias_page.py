from dataclasses import dataclass
from .media import Media


@dataclass
class MediasPage:
    medias: list[Media]
    has_next: bool
