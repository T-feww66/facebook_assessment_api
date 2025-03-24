class CommentProcessor:
    def __init__(self, df=None):
        """
        Khởi tạo đối tượng CommentProcessor.
        :param df: DataFrame chứa dữ liệu ban đầu (nếu có).
        """
        self.df = df

    def split_comments(self):
        comments = self.df.comment
        split_comments = []
        split_usernames = []
        for comment in comments:
            #tach usename bang \n dau tien
            split_usernames.append(comment.split('\n')[0].strip())
            # phan con lai la comment
            split_comments.append('\n'.join(comment.split('\n')[1:]).strip())

        #xoá cột comments ban đâu
        self.df.drop('comment', axis=1, inplace=True)
        #them cot username
        self.df['username'] = split_usernames
        #them cot comment
        self.df['comment'] = split_comments

        return self.df

    def save_comments_to_txt_by_post_content(self, comments_file, output_file):
        """ Save the comments grouped by post_content to a txt file """
        # Tạo dictionary để nhóm các comment theo post_content
        grouped_comments = {}
        
        for comment_data in comments_file:
            post_content = comment_data["post_content"]
            user = comment_data["username"]
            comment = comment_data["comment"]
            
            if post_content not in grouped_comments:
                grouped_comments[post_content] = []
            grouped_comments[post_content].append(f"{user}: {comment}")  # Thêm user vào comment
        
        # Ghi vào file theo cấu trúc mong muốn
        with open(output_file, "w", encoding="utf-8") as f:
            for post_content, comments in grouped_comments.items():
                f.write(f"{post_content}\n\n")  # Dòng "postcontent" riêng biệt
                for comment in comments:
                    f.write(f"{comment}\n")  # Ghi user: comment, cách dòng
                f.write("\n")  # Cách dòng giữa các post_content
