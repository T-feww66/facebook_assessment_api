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
        
    def get_status(self, brand_name: str, word_search: str):
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

    def insert_request(self, id: str, user_id: int, brand_name: str, word_search: str, status: int = 0):
        check_query = f"""
            SELECT id FROM {self.table_name}
            WHERE user_id = %s AND brand_name = %s AND word_search = %s
        """

        update_query = f"""
            UPDATE {self.table_name}
            SET id = %s, status = %s, updated_at = NOW()
            WHERE user_id = %s AND brand_name = %s AND word_search = %s
        """

        insert_query = f"""
            INSERT INTO {self.table_name} (id, user_id, brand_name, word_search, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """

        with DBConnection() as (conn, cursor):
            # Kiểm tra xem bản ghi đã tồn tại chưa
            cursor.execute(check_query, (user_id, brand_name, word_search))
            result = cursor.fetchone()

            if result:
                # Nếu tồn tại thì update
                cursor.execute(update_query, (id, status, user_id, brand_name, word_search))
            else:
                # Nếu chưa thì insert
                cursor.execute(insert_query, (id, user_id, brand_name, word_search, status))

            conn.commit()

