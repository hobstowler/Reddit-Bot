# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 6/8/2022
# Description:
import pymongo
import pymongo as pm
from typing import TypedDict

PORT = '27017'
URL = 'localhost'


class Post(TypedDict):
    post_id: str
    author: str
    title: str
    subreddit: str
    link: str
    text: str
    comments: dict


class Comment(TypedDict):
    comment_id: str
    author: str
    post_id: str
    text: str


def _init_db(init_override=False):
    posts = connect()
    comments = connect('comments')

    post_indices = posts.index_information()
    comment_indices = comments.index_information()
    if (len(post_indices) > 1 or len(comment_indices) > 1) and not init_override:
        print("Has already been run and not being overridden.")
        return

    if 'post_id_1' not in post_indices:
        posts.create_index([('post_id', pymongo.ASCENDING)], unique=True)

    if 'comment_id_1' not in comment_indices:
        comments.create_index([('comment_id', pymongo.ASCENDING)], unique=True)


def connect(db: str = 'posts'):
    client = pm.MongoClient(f'mongodb://{URL}:{PORT}')
    return client['post_db'][db]


def get_one_post(params: dict):
    posts = connect()


def get_posts(params: dict = None):
    if not params:
        params = {}
    posts = connect()

    result = []
    for post in posts.find(params):
        result.append(post)

    return result


def insert_posts(post_list: list):
    posts = connect()
    result = posts.insert_many(post_list)
    return result.inserted_ids


def mark_post_processed(post_id: str, marked=True):
    pass


print(get_posts({'player': 'Tony'}))
#connect().drop_indexes()
print(connect().index_information())
print(connect('comments').index_information())
#print(connect('comments').insert_one({'comment_id': '1uzxy',
 #                               'author': 'Vecna'}).inserted_id)
