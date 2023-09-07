from dataclasses import dataclass
from sqlite3 import Error
from typing import Any


@dataclass
class SQLResult:
    succeed: bool
    result: Any = None
    error: Error = None

    def __bool__(self) -> bool:
        return self.succeed
