from harvester import *


class KeyWordAnalyzer:
    def __init__(self) -> None:
        self._bot = RedditBot()
        self._threshold = self.set_threshold()
        keyword_lists = self.load_lists()

    def load_lists(self):
        # load keywords
        # load exceptions
        # load special words
        pass

    def save_keywords(self):
        pass

    def set_threshold(self, threshold: int = 5):
        """[summary]
        Sets the count threshold under which a key word is not considered relevant.
        Args:
            val (int): [description]
        """
        self._threshold = threshold

    def extract_comments_from_post(self, post_url: str):
        self._bot.get_comments(post_url)

keybot = KeyWordAnalyzer()
keybot.extract_comments_from_post('https://old.reddit.com/r/Virginia/comments/skdtww/glenn_youngkin_set_up_a_tip_line_to_snitch_on/')