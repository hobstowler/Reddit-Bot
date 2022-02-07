# Author: Hobs Towler
# Date: 2/4/2022
# Description:

from harvester import *
import pickle


class KeyWordAnalyzer:
    def __init__(self) -> None:
        self._bot = RedditBot()
        self.set_threshold(5)
        self._keyword_lists = self.load_keyword_lists()
        if self._keyword_lists is None:
            self._keyword_lists = {
                'keyword': set(),
                'keyword_except': set(),
                'special': set(),
                'special_except': set()
            }

    def load_keyword_lists(self, filename: str = None) -> dict:
        """
        Loads a dictionary of keyword and exception lists from a pickled file. Default file name of 'keydata.p' in the
        'keyword data' directory.
        :param filename: The file name.
        :return: A dictionary object containing lists of keywords.
        """
        if filename is None:
            filename = "keyword data\\keydata.p"
        if exists(filename):
            try:
                return pickle.load(open(filename, "rb"))
            except FileNotFoundError:
                print("no file.")
        return None

    # TODO handle more intelligently
    def save_keywords(self, filename: str = None):
        if filename is None:
            filename = "keyword data\\keydata.p"
        with open(filename, 'wb') as outfile:
            pickle.dump(self._keyword_lists, outfile)

    # TODO merge methods
    def create_exception(self, key_exception: str, except_type: str = 'keyword'):
        if except_type not in self._keyword_lists:
            return
        if except_type == 'keyword':
            keyword_list = self._keyword_lists.get('keyword')
            exception_list = self._keyword_lists.get('keyword_except')
        elif except_type == 'special':
            keyword_list = self._keyword_lists.get('special')
            exception_list = self._keyword_lists.get('special_except')

        if key_exception in keyword_list:
            keyword_list.remove(key_exception)
        exception_list.add(key_exception)

    def create_keyword(self, keyword: str, keyword_type):
        if keyword_type not in self._keyword_lists:
            return
        if keyword_type == 'keyword':
            keyword_list = self._keyword_lists.get('keyword')
            exception_list = self._keyword_lists.get('keyword_except')
        elif keyword_type == 'special':
            keyword_list = self._keyword_lists.get('special')
            exception_list = self._keyword_lists.get('special_except')

        if keyword in exception_list:
            exception_list.remove(keyword)
        keyword_list.add(keyword)


    def set_threshold(self, new_threshold: int = 5):
        """

        :param new_threshold:
        :return:
        """
        self._threshold = new_threshold

    def train(self, keyword_type: str = 'keyword', word_list: list = None):
        if word_list is None or keyword_type not in self._keyword_lists:
            return
        for word in word_list:
            self.create_keyword(word, keyword_type)
        self.save_keywords()

    def training_montage(self, keyword_type: str = 'keyword'):
        keyword = None
        while keyword != '-1':
            if keyword is not None:
                self.create_keyword(keyword, keyword_type)
            keyword = input(f"Teach me a new {keyword_type}")
        self.save_keywords()

    def regurgitate(self, keyword_type: str = 'keyword'):
        if keyword_type not in self._keyword_lists:
            return
        for word in self._keyword_lists.get(keyword_type):
            print(word, end=", ")
        print()

    def get_post_from_url(self, post_url: str):
        self._bot.get_posts(post_url)

    def get_stickied_posts_from_subreddit(self, subreddit: str, number: int = 2):
        posts = self._bot.get_posts(subreddit_name='wallstreetbets', stickied=number)
        for post in posts:
            print(post.title)

    def parse_comment(self, comment_text: str):
        pass

keybot = KeyWordAnalyzer()
#keybot.extract_comments_from_post('https://old.reddit.com/r/Virginia/comments/skdtww/glenn_youngkin_set_up_a_tip_line_to_snitch_on/')
#keybot.get_stickied_posts_from_subreddit('wallstreetbets')
#keybot.training_montage()
keybot.regurgitate()
#keybot.save_keywords()