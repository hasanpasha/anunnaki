from dataclasses import dataclass
from enum import Enum
import logging


class RepoType(Enum):
    GIT = 'git'
    HTTP = 'htp'


@dataclass
class Extension:
    id: str
    name: str
    lang: str
    version: str
    repo_type: RepoType
    installed: bool = False
    source_url: str = None
    base_url: str = None
    local_path: str = None
    new_update: 'Extension' = None

    @property
    def has_updates(self) -> bool:
        return self.new_update != None

    def is_same_version(self, other: 'Extension') -> bool:
        this_version = Extension.serialize_version(self.version)
        other_version = Extension.serialize_version(other.version)

        for i in range(0, len(this_version)):
            if this_version[i] != other_version[i]:
                return False
        else:
            return True

    def is_older_version(self, other: 'Extension') -> bool:
        this_version = Extension.serialize_version(self.version)
        other_version = Extension.serialize_version(other.version)

        for i in range(0, len(this_version)):
            if this_version[i] > other_version[i]:
                return False
        else:
            return not self.is_same_version(other)

    @staticmethod
    def serialize_version(version: str) -> tuple[int, int, int]:
        logging.debug(f"serializing {version}")
        return tuple(map(lambda e: int(e), version.split('.')))

    def __eq__(self, other: 'Extension') -> bool:
        if other == None:
            return False

        return self.id == other.id
