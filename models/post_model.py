class PostModel:
    def __init__(self, post_id: str, title: str, content: str, origin: str, score: int, created_date: str, scope: str):
        self.post_id: str = self.get_id(score, post_id)
        self.title: str = title
        self.content: str = content
        self.origin: str = origin
        self.score: int = score
        self.created_date: str = created_date

    @staticmethod
    def get_id(scope, post_id):
        return f'{scope}{post_id}'
