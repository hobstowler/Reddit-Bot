# Author: Hobs Towler
# Date: 2/4/2022
# Description:

from harvester import *
import pickle


class KeyWordAnalyzer:
    def __init__(self) -> None:
        self._bot = RedditBot()
        self._threshold = self.set_threshold()
        self._keyword_lists = self.load_lists()
        if self._keyword_lists is None:
            self._keyword_lists = {
                'keyword': set(),
                'keyword_except': set(),
                'special': set(),
                'special_except': set()
            }

    def load_lists(self, filename:str = None):
        if filename is None:
            filename = "keyword data\\keydata.p"
        if exists(filename):
            try:
                return pickle.load(open(filename, "rb"))
            except FileNotFoundError:
                print("no file.")
        return None

    def save_keywords(self):
        pass

    def create_exception(self, key_exception: str, except_type: str = 'keyword'):
        if except_type == 'keyword':
            keyword_list = self._keyword_lists.get('keyword')
            exception_list = self._keyword_lists.get('keyword_except')
        elif except_type == 'special':
            keyword_list = self._keyword_lists.get('special')
            exception_list = self._keyword_lists.get('special_except')

        if key_exception in keyword_list:
            keyword_list.remove(key_exception)
        exception_list.add(key_exception)

    def set_threshold(self, threshold: int = 5):
        """

        :param threshold:
        :return:
        """
        self._threshold = threshold

    def get_post_from_url(self, post_url: str):
        self._bot.get_posts(post_url)

    def get_stickied_posts_from_subreddit(self, subreddit: str, number: int = 2):
        posts = self._bot.get_posts(subreddit='wallstreetbets', stickied=number)
        for post in posts:
            print(post.title)

keybot = KeyWordAnalyzer()
#keybot.extract_comments_from_post('https://old.reddit.com/r/Virginia/comments/skdtww/glenn_youngkin_set_up_a_tip_line_to_snitch_on/')
keybot.get_stickied_posts_from_subreddit('wallstreetbets')