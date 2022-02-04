from platform import python_branch
import auth
import praw

class RedditBot:
    def __init__(self, client_id: str, secret: str, refresh_token: str = None) -> None:
        self._client_id = client_id
        self._secret = secret
        self._refresh_token = refresh_token

    def refresh_auth_token(self) -> None:
        return auth.get_refresh_token(self._client_id, self._secret)

    def get_reddit(self) -> praw.Reddit:
        return praw.Reddit(
            client_id = self._client_id,
            client_secret = self._secret,
            refresh_token = self._refresh_token,
            # redirect_uri = 'http://localhost:8080',
            user_agent = 'test by u/pytesterbot'
        )

    def get_posts(self, subreddit_name: str, number: int = 5) -> list:
        reddit = self.get_reddit()
        subreddit = reddit.subreddit('all').top('hour')

        posts_of_interest = []

        for submission in subreddit:
            #print(submission.title)
            if submission.score > 100:
                posts_of_interest.append(submission)
                print(submission.score, ":", submission.author, ":", submission.title)
        print(len(posts_of_interest))

class Post:
    """
    Class representing a post on Reddit.
    """
    def __init__(self, author, subreddit, id, stats: dict) -> None:
        self.author = author
        self.subreddit = subreddit
        self.id = id
        self.stats = stats


class User:
    """
    Class representing a Reddit User.
    """
    def __init__(self, username, id) -> None:
        self._username
        self._id
        self._posts = {}

    def add_post(self, post: Post) -> None:
        if post.id not in self._posts:
            self._posts.update({post.id: post})



py_bot = PyTesterBot('ehR39skBNNOdtRnTQIk3pw', 'uZ0M43AxH0TF_z6j6jVkXpXIMsqsJw', '1512276763749-lHJIeRUXXuWz4Dtz6YcC4wAS2YPW-Q')
py_bot.get_posts('wallstreetbets')