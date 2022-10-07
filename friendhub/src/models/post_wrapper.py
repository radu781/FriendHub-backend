from dataclasses import dataclass
from models.post_model import Post
from models.user_model import User

@dataclass
class PostWrapper():
    post: Post
    user: User
