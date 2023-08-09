from dataclasses import dataclass
from .file_extensions import FileExtension


@dataclass
class Subtitle:
    url: str
    language: str
    extension: FileExtension
