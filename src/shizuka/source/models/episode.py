from dataclasses import dataclass


@dataclass
class Episode:
    episode: str
    slang: str
    has_next: bool
    is_special: bool = False
