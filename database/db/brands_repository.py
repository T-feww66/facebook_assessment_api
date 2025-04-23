from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository

class BrandsRepository(BaseRepository):
    def __init__(self):
        super().__init__("brands")  # tên bảng trong MySQL

    def get_brand_by_brand_name(self, brand_name: str):
        query = f"SELECT * FROM {self.table_name} WHERE brand_name = %s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (brand_name,))
            result = cursor.fetchone()
            return result
        
    def get_data_brands_crawl_comments(self, brand_name: str):  
        query = query = f"""
                        SELECT 
                            brands.brand_name, 
                            brands.data_llm AS brand_data_llm, 
                            crawl_comments.is_group, 
                            crawl_comments.is_fanpage, 
                            crawl_comments.date_comment, 
                            crawl_comments.comment, 
                            crawl_comments.data_llm AS comment_data_llm
                        FROM {self.table_name} AS brands
                        INNER JOIN crawl_comments 
                            ON brands.brand_name = crawl_comments.brand_name
                            AND brands.brand_name = %s;
                    """
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (brand_name,))
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
            brand_id
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()

    def insert_brands_with_data_llm(self, data, brand_name,comment_file, created_at, updated_at):
        query = f"""
            INSERT INTO {self.table_name} (
                brand_name,
                comment_file,
                data_llm,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            brand_name,
            comment_file,
            data,
            created_at,
            updated_at
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()