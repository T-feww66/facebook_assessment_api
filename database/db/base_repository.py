from database.db.db_connection import DBConnection

class BaseRepository:
    def __init__(self, table_name):
        self.table_name = table_name

    def insert(self, data: dict):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {self.table_name} ({keys}) VALUES ({placeholders})"

        with DBConnection() as cursor:
            cursor.execute(query, values)
            cursor.connection.commit()

    def get_all(self):
        query = f"SELECT * FROM {self.table_name}"
        with DBConnection() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id):
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        with DBConnection() as cursor:
            cursor.execute(query, (record_id,))
            return cursor.fetchone()
