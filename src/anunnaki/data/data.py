import sqlite3
import logging

from anunnaki import DATA_DB
from anunnaki.extensions.models import RepoType, Extension
from anunnaki.data.sql_result import SQLResult


class Data:
    data_db = DATA_DB
    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.data_db)
        self.cursor = self.conn.cursor()

        self.create_extension_table()

        return self

    def __exit__(self, *args):
        self.conn.close()

    def create_extension_table(self):
        extension_table_query = '''
        CREATE TABLE extensions(
            id STRING NOT NULL,
            name STRING NOT NULL,
            language CHAR(2) NOT NULL,
            version STRING NOT NULL,
            source_url STRING,
            base_url STRING,
            local_path STRING,
            repo_type CHAR(3),
            installed BOOLEAN NOT NULL,
            UNIQUE(id)
        );'''
        return self.execute(extension_table_query)

    def update_extension(self, ext: Extension) -> SQLResult:
        sql = '''UPDATE extensions SET
            name = ?, language = ?, version = ?, source_url = ?, base_url = ?,
            local_path = ?, repo_type = ?, installed = ?
            WHERE id = ?;  
        '''
        params = (
            ext.name, ext.lang, ext.version, ext.source_url, ext.base_url,
            ext.local_path, ext.repo_type.value, ext.installed, ext.id
        )
        return self.execute(sql, params)

    def get_extension(self, id: str) -> Extension:
        sql = '''SELECT id, name, language, version, repo_type,
          installed, source_url, base_url, local_path FROM extensions WHERE id = ?'''
        result = self.execute(sql, (id, ))
        if result:
            ext_db = result.result.fetchone()
            logging.debug(ext_db)
            if ext_db:
                return self.__db_to_extension(ext_db)

    def list_extensions(self) -> list[Extension]:
        sql = '''SELECT id, name, language, version, repo_type,
          installed, source_url, base_url, local_path FROM extensions'''
        result = self.execute(sql)
        if not bool(result):
            return []
        return list(map(lambda e: self.__db_to_extension(e), result.result.fetchall()))

    def __db_to_extension(self, data: tuple) -> Extension:
        ext = Extension(*data)
        logging.debug("serializing ext")
        ext.installed = ext.installed == 1
        ext.repo_type = RepoType(ext.repo_type)

        logging.debug(f"after serializing\n{ext}")
        return ext

    def insert_extension(self, ext: Extension) -> SQLResult:
        sql = '''INSERT INTO extensions(
            id, name, language, version, source_url, base_url, local_path, repo_type, installed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)    
        '''
        params = (
            ext.id, ext.name, ext.lang, ext.version, ext.source_url,
            ext.base_url, ext.local_path, ext.repo_type.value, ext.installed
        )
        return self.execute(sql, params)

    def execute(self, sql_query, sql_parameters=()) -> SQLResult:
        logging.debug(f"{sql_query}, {sql_parameters}")
        try:
            result = self.cursor.execute(sql_query, sql_parameters)
            self.conn.commit()

        except sqlite3.Error as error:
            logging.debug(f"fail {error}")
            return SQLResult(succeed=False, error=error)

        else:
            logging.debug("succeed")
            return SQLResult(succeed=True, result=result)
