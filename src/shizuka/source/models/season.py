from dataclasses import dataclass
from .episode import Episode


@dataclass
class Season:
    season: str
    episodes: list[Episode]
    has_next: bool
