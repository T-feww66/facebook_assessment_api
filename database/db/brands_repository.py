from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository

class BrandsRepository(BaseRepository):
    def __init__(self):
        super().__init__("brands")  # tên bảng trong MySQL

    def get_data_llm_by_brand_name(self, brand_name: str):
        query = f"SELECT data_llm FROM {self.table_name} WHERE brand_name = %s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (brand_name,))
            result = cursor.fetchone()
            return result