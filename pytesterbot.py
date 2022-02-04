from platform import python_branch
import auth
import praw
import json

class RedditBot:
    def __init__(self, credentials_file:str=None) -> None:
        self._users = {}
        if credentials_file is None:
            self._credentials_file = "credentials.txt"
        else:
            self._credentials_file = credentials_file

        with open(self._credentials_file, 'r') as file:
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

        with open(self._credentials_file, 'w') as file:
            json.dump(credentials, file)
        
    def refresh_auth_token(self) -> None:
        return auth.get_refresh_token(self._client_id, self._secret)

    def get_reddit(self) -> praw.Reddit:
        return praw.Reddit(
            client_id = self._client_id,
            client_secret = self._secret,
            user_agent = 'test by u/pytesterbot'
        )

    def get_posts(self, subreddit_name: str, number: int = 5) -> list:
        reddit = self.get_reddit()
        subreddit = reddit.subreddit('all').top('hour')

        for submission in subreddit:
            #print(submission.title)
            if submission.score > 200:
                print("found post.")
                author = submission.author.name
                id = submission.author.id
                new_post = Post(author, submission.subreddit.name, submission.id, {})

                if id not in self._users:
                    new_user = User(author, id)
                    new_user.add_post(new_post)
                    self._users.update({id: new_user})
                else:
                    self._users.get(id).add_post(new_post)
        
        for id,user in self._users.items():
            print(id, ":", user.get_name())
        print("Finished.")

    def dump_to_csv(self):
        with open('raw_data.csv', 'w') as file:
            header = "user, user_id, subreddit, post_id \n"
            file.write(header)
            for user in self._users.values():
                for post in user.get_posts().values():
                    print(user.get_name())
                    file.write(user.get_name() + ",")
                    file.write(user.get_id() + ",")
                    file.write(post.subreddit + ",")
                    file.write(post.id + "\n")


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
        self._username = username
        self._id = id
        self._posts = {}

    def add_post(self, post: Post) -> None:
        if post.id not in self._posts:
            self._posts.update({post.id: post})
    
    def get_name(self) -> str:
        return self._username

    def get_id(self) -> str:
        return self._id

    def get_posts(self) -> dict:
        return self._posts



py_bot = RedditBot()
py_bot.get_posts('wallstreetbets')
py_bot.dump_to_csv()