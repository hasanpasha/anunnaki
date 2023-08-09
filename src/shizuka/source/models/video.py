from dataclasses import dataclass
from enum import Enum


class Resolution(Enum):
    P240 = "240p"
    P360 = "360p"
    P480 = "480p"
    P720 = "720p"
    P1080 = "1080p"
    P1440 = "1440p"
    P2160 = "2160p"
    P4320 = "4320p"


@dataclass
class Video:
    url: str
    resolution: Resolution
