# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 6/8/2022
# Description:

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
    pass


def connect():
    client = pm.MongoClient(f'mongodb://{URL}:{PORT}')
    return client['post_db']['posts']


def get_one_post(criteria: dict=None):
    posts = connect()
    result = posts.insert_one({'team': 'Tigers',
                               'player': 'Tony'})
    print(result.inserted_id)


def get_posts(criteria: dict):
    pass


def insert_posts(post_list: list):
    pass


def mark_post_processed(post_id: str, marked=True):
    pass


get_one_post()