from dataclasses import dataclass

from models.post_model import Post
from models.user_model import User
from models.vote_model import Vote


@dataclass
class PostWrapper:
    post: Post
    user: User
    vote: Vote | None
