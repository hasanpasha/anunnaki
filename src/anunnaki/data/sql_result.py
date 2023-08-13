from dataclasses import dataclass
from sqlite3 import Cursor, Error


@dataclass
class SQLResult:
    succeed: bool
    result: Cursor = None
    error: Error = None

    def __bool__(self) -> bool:
        return self.succeed
