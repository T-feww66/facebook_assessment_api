from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository


class CrawlUrlRepository(BaseRepository):
    def __init__(self):
        super().__init__("crawl_url")

    def get_all(self):
        query = f"SELECT * FROM {self.table_name}"
        with DBConnection() as (conn, cursor):
            cursor.execute(query)
            return cursor.fetchall()
        
    def get_id_by_url(self, link: str):
        query = f"SELECT id FROM {self.table_name} WHERE link = %s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (link,))
            result = cursor.fetchone()
            return result["id"] if result else None


    
        
    def insert_or_update_many(self, link: list, name: list, brand_name: list, created_at: list, updated_at: list):
        query = f"""
            INSERT INTO {self.table_name} (
                link,
                name,
                brand_name,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                link = VALUES(link),
                name = VALUES(name),
                brand_name = VALUES(brand_name),
                created_at = VALUES(created_at),
                updated_at = VALUES(updated_at)
        """

        # Ghép 4 list thành danh sách các tuple
        values = list(zip(link, name, brand_name, created_at, updated_at))

        with DBConnection() as (conn, cursor):
            cursor.executemany(query, values)
            conn.commit()
