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
    comments: dict


def _init_db():
    posts = connect()
    posts.create_index([('post_id', pymongo.ASCENDING)])


def connect():
    client = pm.MongoClient(f'mongodb://{URL}:{PORT}')
    return client['post_db']['posts']


def get_one_post(criteria: list):
    pass


def get_posts(params: dict=None):
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


print(get_posts({'player':'Tony'}))