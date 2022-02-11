# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 2/11/2022
# Description:

from reddit_bot import *


class ThisBot(RedditBot):
    def __init__(self) -> None:
        super().__init__(data_file=r"data\this.p")

    def this(self) -> None:
        """
        Gets comments from the top 10 posts on reddit and checks to see if anyone started a sentence with "This.".
        Prints out a sarcastic message if it finds a comment that matches.
        :return: Nothing.
        """
        posts = self.get_posts(subreddit_name='all', timeframe='day', number=10)
        for post in posts:
            print(f"{post.id} | {post.score} | {post.title}")
            print(f"{post.subreddit} | {post.permalink}")
            post.comments.replace_more(threshold=5)
            for comment in post.comments.list():
                if comment.body.split()[0].lower() in ["this.", "this!"]:
                    print(f"{comment.id} | {comment.score} | {comment.author.name}")
                    print(f"{comment.body}")
                    print("Reply: This! This right here!")


def main():
    this_bot = ThisBot()
    this_bot.this()


if __name__ == "__main__":
    main()