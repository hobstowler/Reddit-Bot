# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 6/8/2022
# Description:

import pymongo
import pymongo as pm
from typing import TypedDict

from pymongo import ReturnDocument

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
    processed: bool


class Comment(TypedDict):
    comment_id: str
    author: str
    post_id: str
    text: str
    processed: bool


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


def get_posts(params: dict = None):
    if not params:
        params = {}
    posts = connect()

    result = []
    for post in posts.find(params):
        result.append(post)

    return result


def get_unprocessed_posts():
    return get_posts({'processed': True})


def insert_posts(*new_posts):
    posts = connect()
    result = posts.insert_many(new_posts)
    return result.inserted_ids


def update_post(post_id: str, **updates):
    if not updates:
        print('No updates passed. Exiting...')
        return

    posts = connect()
    result = posts.find_one({'post_id': post_id})
    if not result:
        print('No documents found to update. Exiting...')

    return posts.find_one_and_update({'_id': result['_id']},
                                     {'$set': updates},
                                     return_document=ReturnDocument.AFTER)



def mark_post_processed(post_id: str, marked=True):
    posts = connect()

    result = posts.find_one({'post_id': post_id})
    if not result:
        print('not found')
        return

    return posts.find_one_and_update({'_id': result['_id']},
                                     {'$set': {'processed': True}},
                                     return_document=ReturnDocument.AFTER)


def get_comments(params: dict = None):
    if not params:
        params = {}
    comments = connect('comments')
    result = []
    for comment in comments.find(params):
        result.append(comment)
    return result


def get_comments_from_post(post_id: str, params: dict = None, unprocessed_only=True):
    if not post_id:
        return

    if not params:
        params = {}
    params['post_id'] = post_id
    if unprocessed_only:
        params['processed'] = True

    return get_comments(params)


def insert_comments(*new_comments):
    comments = connect('connect')
    result = comments.insert_many(new_comments)
    return result.inserted_ids


#print(get_posts())
#connect().drop_indexes()
#print(connect().index_information())
#print(connect('comments').index_information())
#print(connect().insert_one({'post_id': '1uzxyz',
#                                'author': 'Vecna'}).inserted_id)
#print(get_posts()[0]['_id'])
#print(connect().find_one())
#print('processed:',mark_post_processed('1uzxyz')).
posts = [{'post_id':'1hsdf'}, {'post_id': 'trhe23'}]
insert_posts(*posts)
print(get_posts())

#update_post('12gsd')