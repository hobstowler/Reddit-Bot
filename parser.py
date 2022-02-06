# Author: Hobs Towler
# Date: 2/4/2022
# Description:

from harvester import *
import pickle


class KeyWordAnalyzer:
    def __init__(self) -> None:
        self._bot = RedditBot()
        self._threshold = self.set_threshold()
        keyword_lists = self.load_lists()
        if keyword_lists is None:
            keyword_lists = {
                'keywords': set(),
                'keywords_except': set(),
                'special_words': set(),
                'special_except': set()
            }

    def load_lists(self, filename:str = None):
        if filename is None:
            filename = "keyword data\\keydata.p"
        if exists(filename):
            return pickle.load(open(filename, "rb"))
        return None

    def save_keywords(self):
        pass

    def set_threshold(self, threshold: int = 5):
        """[summary]
        Sets the count threshold under which a key word is not considered relevant.
        Args:
            val (int): [description]
        """
        self._threshold = threshold

    def get_post_from_url(self, post_url: str):
        self._bot.get_posts(post_url)

    def get_stickied_posts_from_subreddit(self, subreddit: str, number:int=2):
        posts = self._bot.get_posts(subreddit='wallstreetbets', stickied=number)
        for post in posts:
            print(post.title)

keybot = KeyWordAnalyzer()
#keybot.extract_comments_from_post('https://old.reddit.com/r/Virginia/comments/skdtww/glenn_youngkin_set_up_a_tip_line_to_snitch_on/')
keybot.get_stickied_posts_from_subreddit('wallstreetbets')