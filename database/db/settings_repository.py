from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository


class SettingRepository(BaseRepository):
    def __init__(self):
        super().__init__("settings")

    def get_all(self):
        query = f"SELECT * FROM {self.table_name}"
        with DBConnection() as (conn, cursor):
            cursor.execute(query)
            return cursor.fetchall()