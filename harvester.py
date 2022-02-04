from platform import python_branch
from os.path import exists
import auth
import praw
import json
import pickle

class RedditBot:
    def __init__(self, credentials_file:str=None, data_file:str=None) -> None:
        self._default_save_file = 'data.p'
        self._users = {}
        if credentials_file is None:
            credentials_file = "credentials.txt"

        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            self._credentials = credentials
            self._client_id = credentials.get('client_id')
            self._secret = credentials.get('secret')
            self._refresh_token = credentials.get('refresh_token')

        # handle default better
        self._data = self.load_data(data_file)
        if self._data is not None:
            self._users = self._data.get('users')
            print("loaded users")
        

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

    def get_reddit(self, agent_text:str) -> praw.Reddit:
        return praw.Reddit(
            client_id = self._client_id,
            client_secret = self._secret,
            user_agent = agent_text
        )

    def get_posts(self, subreddit_name: str, number: int = 25) -> list:
        reddit = self.get_reddit('test getting posts by u/pytesterbot')
        subreddit = reddit.subreddit('all').top('hour', limit=number)

        for submission in subreddit:
            if submission.score > 100:
                author = submission.author.name
                id = submission.author.id
                new_post = Post(author, submission.subreddit.name, submission.id, {})

                if id not in self._users:
                    new_user = User(author, id)
                    new_user.add_post(new_post)
                    self._users.update({id: new_user})
                else:
                    self._users.get(id).add_post(new_post)
        
        print("Finished.")

    def get_comments(self, post_url: str):
        reddit = self.get_reddit('test getting comments by u/pytesterbot')
        post = reddit.submission(url=post_url)
        print("success?", post.title)
    
    def save_data(self, filename: str = None):
        if filename is None:
            filename = self._default_save_file
        print(filename)
        data = {
            'users': self._users,
            'credentials': self._credentials
            }
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)


    def load_data(self, filename: str = None):
        if filename is None:
            filename = self._default_save_file
        if exists(filename):
            with open(filename, 'rb') as infile:
                return pickle.load(infile)


    def dump_to_csv(self):
        with open('raw_data.csv', 'w') as file:
            print("writing to csv")
            header = "username, user_id, # posts, subreddit, post_id \n"
            file.write(header)
            for user in self._users.values():
                for post in user.get_posts().values():
                    print(user.get_name())
                    file.write(user.get_name() + ",")
                    file.write(user.get_id() + ",")
                    file.write(str(len(user.get_posts())) + ",")
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


class Comment:
    def __init__(self) -> None:
        pass


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


def main():
    py_bot = RedditBot()
    py_bot.get_posts('wallstreetbets')
    py_bot.save_data()
    py_bot.dump_to_csv()
    py_bot.get_posts('politics')
    py_bot.save_data()
    py_bot.dump_to_csv()


if __name__ == "__main__":
    main()