from typing import Callable
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject
import sqlite3

import logging

class SQLException(Exception):
    def __init__(self, error: sqlite3.Error, message: str = None) -> None:
        self.error = error
        self.message = message

    def __str__(self) -> str:
        return f"SQLException<{self.error}>: {self.message}"

class SQLWorkerSignals(QObject):
    result = Signal(list)
    error_occured = Signal(SQLException)

class SQLWorker(QRunnable):
    """
    Execute the query on the passed database and emit the result 
    as a list[dict] object or emits error_occured signal on error
    """
    def __init__(self, db_name: str, query: str) -> None:
        super(SQLWorker, self).__init__()

        self.db_name = db_name
        self.query = query

        self.__signals = SQLWorkerSignals()
        self.result = self.__signals.result
        self.error_occured = self.__signals.error_occured

    def run(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            logging.error(f"{e}: failed to connect to the database")
            self.error_occured.emit(SQLException(e, "Failed to connect to the database"))
            return
    
        try:
            cursor = conn.cursor()
        except sqlite3.Error as e:
            logging.error(f"{e}: failed to create a cursor")
            self.error_occured.emit(SQLException(e, "Failed to create a cursor"))
            conn.close()
            return
        
        try:
            result = cursor.execute(self.query)
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"{e}: failed to execute the query <{self.query}>")
            self.error_occured.emit(SQLException(e, f"Failed to execute the query <{self.query}>"))
        else:
            rows = result.fetchall()
            data = [dict(row) for row in rows]
            self.result.emit(data)
        finally:
            conn.close()
   
class SQLThread(QThreadPool):
    """Execute SQL queries in parallel"""
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def execute(self, db_path: str, query: str, on_result: Callable, on_error: Callable):
        """Execute a SQL Query"""
        worker = SQLWorker(db_path, query)
        worker.result.connect(on_result)
        worker.error_occured.connect(on_error)

        logging.debug(f"starting new sqlworker:\ndb: {db_path}\nquery: {query}")
        self.start(worker)