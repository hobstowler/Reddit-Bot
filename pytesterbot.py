from platform import python_branch
import auth
import praw
import json

class RedditBot:
    def __init__(self, credentials_file=None) -> None:
        if credentials_file is None:
            credentials_file = "credentials.txt"
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            self._client_id = credentials.get('client_id')
            self._secret = credentials.get('secret')
            self._refresh_token = credentials.get('refresh_token')

    def refresh_credentials(self) -> None:
        credentials = {}
        if self._client_id is not None:
            credentials.update({'client_id': self._client_id})
        if self._secret is not None:
            credentials.update({'secret': self._secret})
        if self._refresh_token is not None:
            credentials.update({'refresh_token': self._refresh_token})

        with open('credentials.txt', 'w') as file:
            json.dump(credentials, file)
        

    def refresh_auth_token(self) -> None:
        return auth.get_refresh_token(self._client_id, self._secret)

    def get_reddit(self) -> praw.Reddit:
        return praw.Reddit(
            client_id = self._client_id,
            client_secret = self._secret,
            refresh_token = self._refresh_token,
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



py_bot = RedditBot()
py_bot.get_posts('wallstreetbets')
#py_bot.refresh_credentials()