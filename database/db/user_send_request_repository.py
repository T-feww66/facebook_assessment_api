from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository

class UserSendRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__("user_send_request")  # tên bảng trong MySQL

    def get_user_send_request_by_brand_name(self, brand_name: str, word_search: str):
        query = f"SELECT * FROM {self.table_name} WHERE brand_name = %s AND word_search = %s AND status = 0"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (brand_name, word_search))
            result = cursor.fetchone()
            return result

    def get_user_send_request_by_status(self, status: int):
        query = f"SELECT * FROM {self.table_name} WHERE status = %s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (status,))
            result = cursor.fetchone()
            return result  
        
    def update_status_by_id(self, id:int, status: int):
        query = f"""
            UPDATE {self.table_name}
            SET status = %s,
                updated_at = NOW()
            WHERE id = %s
        """

        values = (
            status,
            id
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()