from database.db.base_repository import BaseRepository
from database.db.db_connection import DBConnection

class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__("crawl_comments")


    def get_comment_by_unique_keys(self, comment, brand_name):
        query = """
            SELECT * FROM crawl_comments
            WHERE comment = %s AND brand_name = %s
            LIMIT 1
        """
        values = (comment, brand_name)

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result  # Trả về None nếu không có, hoặc {'id': ...} nếu có


    def insert_crawl_comments_with_data_llm(self, data, brand_name, post_content, is_group, is_fanpage,comment_file, comment, date_comment, date_crawled, created_at, updated_at):
        query = """
            INSERT INTO crawl_comments (
                brand_name,
                post_content,
                is_group,
                is_fanpage,
                comment_file,
                comment,
                date_comment,
                date_crawled,
                data_llm,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            brand_name,
            post_content,
            is_group,
            is_fanpage,
            comment_file,
            comment,
            date_comment,
            date_crawled,
            data,
            created_at,
            updated_at
        )

        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()

    def update_crawl_comment_by_id(self, comment_id, data, is_group, is_fanpage, comment_file, date_crawled, updated_at):
        query = """
            UPDATE crawl_comments
            SET
                data_llm = %s,
                is_group = %s,
                is_fanpage = %s,
                comment_file = %s,
                date_crawled = %s,
                updated_at = %s
            WHERE id = %s
        """
        values = (
            data,
            is_group,
            is_fanpage,
            comment_file,
            date_crawled,
            updated_at,
            comment_id
        )
        with DBConnection() as (conn, cursor):
            cursor.execute(query, values)
            conn.commit()



    def get_crawl_comment_by_name(self, brand_name: str):
        query = f"SELECT * FROM {self.table_name} WHERE brand_name = %s"

        with DBConnection() as (conn, cursor):
            cursor.execute(query, (brand_name,))
            result = cursor.fetchall()
            return result

