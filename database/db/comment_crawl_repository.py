from database.db.base_repository import BaseRepository
from database.db.db_connection import DBConnection

class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__("crawl_comments")

    def insert_crawl_comments_with_data_llm(self, data, brand_name, is_group, is_fanpage,comment_file, comment, date_comment, date_crawled, created_at, updated_at):
        query = """
            INSERT INTO crawl_comments (
                brand_name,
                is_group,
                is_fanpage,
                comment_file,
                comment,
                date_comment,
                date_crawled,
                data_llm,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            brand_name,
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

    def insert_brands_with_data_llm(self, data, brand_name,comment_file, created_at, updated_at):
        query = """
            INSERT INTO brands (
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