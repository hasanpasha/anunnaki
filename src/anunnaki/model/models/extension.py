from dataclasses import dataclass
import logging


@dataclass
class Extension:
    id: int   # hash(lang_pkg)
    pkg: str
    name: str
    version: str
    lang: str
    base_url: str = None
    installed: bool = False
    has_new_update: bool = False
    zip_file: str = None
    zip_url: str = None
    icon_file: str = None
    icon_url: str = None

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

        return str(self.id) == str(other.id)
