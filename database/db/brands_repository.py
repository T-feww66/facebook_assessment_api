from database.db.db_connection import DBConnection
from database.db.base_repository import BaseRepository

class BrandsRepository(BaseRepository):
    def __init__(self):
        super().__init__("brands")  # tên bảng trong MySQL

    def get_brand_by_brand_name(self, brand_name: str, word_search: str, user_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE user_id = %s and brand_name = %s and word_search=%s"
        with DBConnection() as (conn, cursor):
            cursor.execute(query, (user_id, brand_name, word_search))
            result = cursor.fetchone()
            return result
        
    def get_data_visualization(self, brand_name: str, word_search: str, user_id: int):
        with DBConnection() as (conn, cursor):
            # 1. Lấy tất cả crawl_url của brand_name, sắp xếp theo updated_at DESC
            cursor.execute("""
                SELECT * FROM crawl_url
                WHERE brand_name = %s
                ORDER BY updated_at DESC
            """, (brand_name,))
            urls = cursor.fetchall()
            urls = list(urls)[::-1]  # Đảo ngược để idx 0 là URL đầu tiên được tạo


            # 2. Lấy tất cả comments liên quan
            cursor.execute(f"""
                SELECT 
                    brands.brand_name, 
                    brands.word_search,
                    brands.data_llm AS brand_data_llm, 
                    crawl_comments.is_group, 
                    crawl_comments.is_fanpage, 
                    crawl_comments.date_comment, 
                    crawl_comments.comment, 
                    crawl_comments.data_llm AS comment_data_llm,
                    crawl_comments.idx
                FROM {self.table_name} AS brands
                INNER JOIN crawl_comments 
                    ON brands.brand_name = crawl_comments.brand_name
                    AND brands.word_search = crawl_comments.word_search
                    AND brands.user_id = crawl_comments.user_id
                WHERE brands.brand_name = %s 
                AND brands.word_search = %s 
                AND brands.user_id = %s
            """, (brand_name, word_search, user_id))

            raw_data = cursor.fetchall()
            result = []

            for row in raw_data:
                idx = row.get("idx")
                matched_url = urls[idx] if idx is not None and idx < len(urls) else None

                row["link"] = matched_url["link"] if matched_url else None
                row["name"] = matched_url["name"] if matched_url else None
                result.append(row)

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