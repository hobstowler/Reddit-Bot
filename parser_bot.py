# Author: Hobs Towler
# Date: 2/4/2022
# Description:

from reddit_bot import *
import praw.models
import pickle


class KeyWordAnalyzer(RedditBot):
    """
    An extension of the RedditBot for analyzing keywords from posts and comments.
    """
    def __init__(self) -> None:
        """
        Initializes the KeyWordAnalyzer
        """
        super().__init__(data_file=r"data\keyword_data.p")
        self._words = {}
        self.set_threshold(25)
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
    def save_keyword_lists(self, filename: str = None) -> None:
        """
        Saves the lists of keywords to file. Defaults to 'keyword data\keydata.p'
        :param filename: The file name. Optional.
        :return: Nothing.
        """
        print("saving keywords lists")
        if filename is None:
            filename = "keyword data\\keydata.p"
        with open(filename, 'wb') as outfile:
            pickle.dump(self._keyword_lists, outfile)

    # TODO rework how keywords are stored
    def create_keyword(self, keyword: str, keyword_type) -> None:
        """
        Adds a keyword to the list of keywords/exceptions. If keyword is present as an exception or keyword already, it
        is removed from that list to prevent conflict.
        :param keyword: The keyword or exception to be added
        :param keyword_type: The list name to which the keyword is to be added.
        :return: Nothing.
        """
        keyword = keyword.lower()
        if keyword_type not in self._keyword_lists:
            return
        if keyword_type in ['keyword', 'keyword_except']:
            keyword_list = self._keyword_lists.get('keyword')
            exception_list = self._keyword_lists.get('keyword_except')
        elif keyword_type in ['special', 'special_except']:
            keyword_list = self._keyword_lists.get('special')
            exception_list = self._keyword_lists.get('special_except')

        if keyword_type in ['keyword', 'special']:
            if keyword in exception_list:
                exception_list.remove(keyword)
            keyword_list.add(keyword)
        else:
            if keyword in keyword_list:
                keyword_list.remove(keyword)
            exception_list.add(keyword)

    # TODO implement thresholds
    def set_threshold(self, new_threshold: int = 5) -> None:
        """
        Sets the threshold for which the occurrence of a keyword becomes significant.
        :param new_threshold: The new threshold
        :return: Nothing.
        """
        self._threshold = new_threshold

    def train(self, keyword_type: str = 'keyword', word_list: list = None):
        if word_list is None or keyword_type not in self._keyword_lists:
            return
        for word in word_list:
            self.create_keyword(word, keyword_type)
        self.save_keyword_lists()

    def training_montage(self, keyword_type: str = 'keyword'):
        keyword = None
        while keyword != '-1':
            if keyword is not None:
                self.create_keyword(keyword, keyword_type)
            keyword = input(f"Teach me a new {keyword_type}")
        self.save_keyword_lists()

    def regurgitate(self, keyword_type: str = 'keyword'):
        if keyword_type not in self._keyword_lists:
            return
        for word in self._keyword_lists.get(keyword_type):
            print(word, end=", ")
        print()

    def forget(self, keyword: str, keyword_type: str = 'keyword'):
        if keyword in self._keyword_lists.get(keyword_type):
            self._keyword_lists.get(keyword_type).remove(keyword)
        else:
            print("word not in list")

    def forget_everything(self, keyword_type: str = 'keyword'):
        self._keyword_lists.update({keyword_type: set()})

    def get_stickied_posts_from_subreddit(self, subreddit: str, number: int = 3):
        posts = self.get_posts(subreddit_name='wallstreetbets', stickied=number)
        print("Posts retrieved.")
        for post in posts:
            if post.id not in self._posts:
                post_obj = ParsedPost(post)
                self._posts.update({post.id: post_obj})
            else:
                post_obj = self._posts.get(post.id)
            post_comments = post_obj.get_comments()
            post.comments.replace_more(threshold=5)
            for comment in post.comments.list():
                #if not isinstance(comment, praw.models.MoreComments):
                if comment.id not in post_comments:
                    print("found a new post")
                    new_comment = Comment(comment)
                    post_comments.update({comment.id: new_comment})
            print(len(post_comments))

    def process_comments(self, strict: bool = False) -> None:
        print("processing")
        for post in self._posts.values():
            comments = [comment.body for comment in post.get_comments().values()]
            for comment in comments:
                # TODO clean up comments a bit
                for word in comment.split():
                    word = word.lower()
                    if word in self._words:
                        self._words.update({word: self._words.get(word) + 1})
                    elif word not in self._keyword_lists.get('keyword_except') and \
                            ((strict and word in self._keyword_lists.get('keyword')) or not strict):
                        self._words.update({word.lower(): 1})

    def spit_it_out(self):
        print("spitting", len(self._words), "words")
        sorted_words = sorted(self._words.items(), key=lambda x: x[1], reverse=True)
        for word in sorted_words:
            if word[1] > self._threshold:
                print(word[0],":",word[1], end=", ")


    def parse_comment(self, comment_text: str):
        pass


class ParsedPost(Post):
    def __init__(self, post: praw.models.Submission):
        super().__init__(post)


def main():
    keybot = KeyWordAnalyzer()
    #keybot.extract_comments_from_post('https://old.reddit.com/r/Virginia/comments/skdtww/glenn_youngkin_set_up_a_tip_line_to_snitch_on/')
    keybot.get_stickied_posts_from_subreddit('wallstreetbets')
    #keybot.save_data()
    #keybot.training_montage('keyword_except')
    #keybot.forget_everything()
    #keybot.regurgitate('keyword_except')
    #keybot.save_keyword_lists()
    keybot.process_comments()
    #keybot.spit_it_out()


if __name__ == "__main__":
    main()
