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