from dataclasses import dataclass
from .kind import Kind


@dataclass
class Media:
    title: str = None
    kind: Kind = None
    slang: str = None
    url: str = None
    thumbnail_url: str = None
    description: str = None
    tags: list[str] = None

    @property
    def is_movie(self) -> bool:
        return self.kind == Kind.MOVIES
