# Author: Hobs Towler
# Date: 2/5/2022
# Description:

from platform import python_branch
from os.path import exists
import auth
import praw, prawcore
import json
import pickle

class RedditBot:
    """
    A generic reddit bot to pull posts and comments
    """
    def __init__(self, credentials_file: str = None, data_file: str = None) -> None:
        """
        Initializes the Reddit Bot.
        :param credentials_file: file containing credentials to connect to Reddit's API
        :param data_file: file containing data from previous runs.
        """
        self._users = {}
        if credentials_file is None:
            credentials_file = "credentials\\credentials.txt"
        if data_file is None:
            data_file = 'data\\data.p'
        self._data_file = data_file
        self._credentials_file = credentials_file
        self._credentials = {}

        try:
            with open(self._credentials_file, 'r') as file:
                self._credentials = json.load(file)
        except FileNotFoundError:
            print("No credentials found. Creating new file...")
            open(self._credentials_file, 'w')
            self.prompt_credentials()

        try:
            self._data = self.load_data(self._data_file)
            if self._data is not None:
                self._users = self._data.get('users')
                print("Loaded users.")
        except FileNotFoundError:
            print("No data file found. Creating new file...")
            open(self._data_file, 'w')

    def refresh_credentials(self) -> None:
        """
        To be used later. Will update credentials file if tokens change. Need to detect the change.
        :return: Nothing.
        """
        with open(self._credentials_file, 'w') as file:
            json.dump(self._credentials, file)

    def prompt_credentials(self):
        client_id = input("Enter a client ID:")
        client_secret = input("Enter client secret:")
        print("Launching web page to get token...")
        self.refresh_auth_token(client_id, client_secret)
        
    def refresh_auth_token(self, client_id, client_secret) -> None:
        """
        Gets a new refresh token.
        :return: Nothing.
        """
        self._credentials.update({'client_id': client_id})
        self._credentials.update({'secret': client_secret})
        self._credentials.update({'refresh_token': auth.get_refresh_token(client_id, client_secret)})
        self.refresh_credentials()

    def get_reddit(self, agent_text: str) -> praw.Reddit:
        """
        Gets an instance of a Reddit object.
        :param agent_text: Text of the user agent to be sent in the request.
        :return: The Reddit object.
        """
        return praw.Reddit(
            client_id=self._credentials.get('client_id'),
            client_secret=self._credentials.get('secret'),
            user_agent=agent_text
        )

    def get_posts(self, subreddit_name: str = 'all',
                  post_url: str = None,
                  stickied: int = 0,
                  number: int = 100,
                  timeframe: str = 'hour',
                  score: int = 100) -> list:
        """
        Returns a post from Reddit. Optional parameters can be used to pull a specific post, stickied posts in a
        certain subreddit, or a specific number of posts.
        :param timeframe: The time frame for submissions.
        :param subreddit_name: The name of the subreddit to pull a post from.
        :param post_url: The url of a specific post.
        :param stickied: The number of stickied posts to pull from a specified subreddit.
        :param number: The number of non-stickied posts to pull from a subreddit.
        :return: A post from Reddit.
        """
        reddit = self.get_reddit('test getting posts by u/pytesterbot')
        posts = []
        if post_url is not None:
            posts.append(reddit.submission(url=post_url))
        elif subreddit_name != 'all' and stickied > 0:
            for i in range(1, stickied+1):
                try:
                    post = reddit.subreddit(subreddit_name).sticky(i)
                    if post not in posts:
                        posts.append(post)
                except prawcore.NotFound:
                    print("Could not find sticked post #", i)
        else:
            subreddit = reddit.subreddit(subreddit_name).top(timeframe, limit=number)
            for submission in subreddit:
                if submission.score >= score:
                    author = submission.author.name
                    id = submission.author.id
                    new_post = Post(author, submission.subreddit.name, submission.id, {})

                    if id not in self._users:
                        new_user = User(author, id)
                        new_user.add_post(new_post)
                        self._users.update({id: new_user})
                    else:
                        self._users.get(id).add_post(new_post)
        
        return posts

    def save_data(self, filename: str = None) -> None:
        """
        Pickles data to a specified file. Will overwrite existing file.
        :param filename: The file name.
        :return: Nothing.
        """
        if filename is None:
            filename = self._data_file
        data = {
            'users': self._users,
            'credentials': self._credentials
            }
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)


    def load_data(self, filename: str = None) -> dict:
        """
        Loads data from a specified file.
        :param filename: The file name.
        :return: Nothing.
        """
        if filename is None:
            filename = self._data_file
        if exists(filename):
            try:
                with open(filename, 'rb') as infile:
                    return pickle.load(infile)
            except FileNotFoundError:
                print("no file.")
        return None

    def dump_to_csv(self, file_name: str = None) -> None:
        """
        Writes collected users and posts to a .csv file.
        :param file_name: The file name.
        :return: Nothing.
        """
        if file_name is None:
            file_name = 'raw_data.csv'
        with open(file_name, 'w') as file:
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
    def __init__(self, author, subreddit, stats: dict) -> None:
        """
        Initializes a Post class.
        :param author: Author of the post on Reddit.
        :param subreddit: The subreddit posted to.
        :param reddit_id: The id of the post.
        :param stats: additional post information as a dictionary object.
        """
        self.author = author
        self.subreddit = subreddit
        self._stats = stats
        self._comments = {}

    def get_comments(self) -> dict:
        return self._comments

    def get_stats(self) -> dict:
        return self._stats


class Comment:
    """
    Class representing a comment on Reddit.
    """
    def __init__(self) -> None:
        pass


class User:
    """
    Class representing a Reddit User.
    """
    def __init__(self, username, id) -> None:
        """
        Initializes the User with a name and id.
        :param username: The user's name from Reddit.
        :param id: Reddit-assigned ID. Assumed unique?
        """
        self._username = username
        self._id = id
        self._posts = {}

    def add_post(self, post: Post) -> None:
        """
        Adds a post to the user. User here is the author of the post.
        :param post: A post from Reddit.
        :return: Nothing.
        """
        if post.id not in self._posts:
            self._posts.update({post.id: post})
    
    def get_name(self) -> str:
        """
        Returns the user's name.
        :return: Username as string.
        """
        return self._username

    def get_id(self) -> str:
        """
        Returns the user's ID.
        :return: ID as string.
        """
        return self._id

    def get_posts(self) -> dict:
        """
        Returns the user's posts. The post's reddit-assigned ID will be the key and Post object is the value.
        :return: A dictionary object containing the user's posts.
        """
        return self._posts


def main():
    print("starting")
    py_bot = RedditBot()
    py_bot.get_posts(subreddit_name='wallstreetbets')
    py_bot.get_posts(subreddit_name='politics')
    py_bot.save_data()
    py_bot.dump_to_csv()


if __name__ == "__main__":
    main()