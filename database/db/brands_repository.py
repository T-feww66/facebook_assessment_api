from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository

class BrandsRepository(BaseRepository):
    def __init__(self):
        super().__init__("brands")  # tên bảng trong MySQL

    def get_id_by_url(self, link: str):
        query = f"SELECT id FROM {self.table_name} WHERE link = %s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (link,))
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_brand_by_brand_name(self, brand_name: str, word_search: str, user_id: int):
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE user_id = %s AND brand_name = %s AND word_search = %s
        """
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (user_id, brand_name, word_search))
            return cursor.fetchone()



        
    def get_data_visualization(self, brand_name: str, word_search: str, user_id: int):
        with DBConnection() as (conn, cursor):
            # Truy vấn duy nhất, join thẳng crawl_url với crawl_comments thông qua id = idx
            cursor.execute(f"""
                SELECT 
                b.brand_name, 
                b.word_search,
                b.data_llm AS brand_data_llm, 
                c.is_group, 
                c.is_fanpage, 
                c.post_content, 
                c.post_data,
                c.comment, 
                c.date_comment, 
                c.data_llm AS comment_data_llm,
                u.link,
                u.name
            FROM brands AS b
            INNER JOIN crawl_comments AS c
                ON b.brand_name = c.brand_name
            AND b.word_search = c.word_search
            AND b.user_id = c.user_id
            LEFT JOIN crawl_url AS u
                ON u.id = c.idx
            WHERE b.brand_name = %s 
            AND b.user_id = %s
            AND b.word_search = %s
            """, (brand_name, user_id, word_search))

            result = cursor.fetchall()
            return result
    def get_data_brands_visualization(self, brand_name: str, user_id: int):
        with DBConnection() as (conn, cursor):
            # Truy vấn duy nhất, join thẳng crawl_url với crawl_comments thông qua id = idx
            cursor.execute(f"""
                SELECT 
                b.brand_name, 
                b.word_search,
                b.data_llm AS brand_data_llm, 
                c.is_group, 
                c.is_fanpage, 
                c.post_content, 
                c.post_data,
                c.comment, 
                c.date_comment, 
                c.data_llm AS comment_data_llm,
                u.link,
                u.name
            FROM brands AS b
            INNER JOIN crawl_comments AS c
                ON b.brand_name = c.brand_name
            AND b.word_search = c.word_search
            AND b.user_id = c.user_id
            LEFT JOIN crawl_url AS u
                ON u.id = c.idx
            WHERE b.brand_name = %s 
            AND b.user_id = %s
            """, (brand_name, user_id))

            result = cursor.fetchall()
            return result

    
        
    def update_data_llm_by_id(self, brand_id:int, data_llm: str):
        query = f"""
            UPDATE {self.table_name}
            SET data_llm = %s,
                updated_at = NOW()
            WHERE id = %s
        """

        values = (
            data_llm,
            brand_id,
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()

    def insert_brands_with_data_llm(self, user_id, data, word_search, brand_name,comment_file, created_at, updated_at):
        query = f"""
            INSERT INTO {self.table_name} (
                user_id,
                word_search,
                brand_name,
                comment_file,
                data_llm,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            word_search,
            brand_name,
            comment_file,
            data,
            created_at,
            updated_at
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()