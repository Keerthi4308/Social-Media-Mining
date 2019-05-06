'''Assignment 4 (Version 1.2)

Please add your code where indicated. You may conduct a superficial test of
your code by executing this file in a python interpreter.

The documentation strings ("docstrings") for each function tells you what the
function should accomplish. If docstrings are unfamiliar to you, consult the
Python Tutorial section on "Documentation Strings".

This assignment requires the following packages:

- numpy
- pandas
- requests

You must not use any packages which are not available on the Linux server.

'''

import os
import unittest

import numpy as np
import pandas as pd
import requests
import re
from requests_oauthlib import OAuth1
# for the Twitter API, you can use
#import requests_oauthlib

TWITTER_DATA_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'united-states-congress-house-twitter-2016-grouped-tweets-train.csv')
WIKIPEDIA_API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'


def count_user_mentions(tweet_list):
    """Count the number of user mentions (aka at-mentions, @-mentions) in each tweet in a list.

    This function operates on a list of tweets rather than one tweet at a time.
    This exercise is intended to provide more practice with lists, functions,
    and regular expressions.

    Arguments:
        tweet_list (list of str): List of Tweets.

    Returns:
        list of int: List of user mention counts.

    """
    # YOUR CODE HERE
    string=''.join(tweet_list)
    match=re.findall(r"@(\w+)",string)
    result=[]
    for string in tweet_list:
        match=re.findall(r"@(\w+)",string)
        result.append(len(match))
    return result
    	

# you may wish to skip this function until we cover using the Wikipedia API
def page_ids(titles):
    """Look up the Wikipedia page ids by title.

    For example, the Wikipedia page id of "Albert Einstein" is 736. (This page
    has a small page id because it is one of the very first pages on
    Wikipedia.)

    A useful reference for the Mediawiki API is this page:
    https://www.mediawiki.org/wiki/API:Info

    Arguments:
        titles (list of str): List of Wikipedia page titles.

    Returns:
        list of int: List of Wikipedia page ids.

    """
    # The following lines of code (before `YOUR CODE HERE`) are suggestions
    params = {
        'action': 'query',
        'titles': '|'.join(titles),
        'indexpageids': 1,
        'format': 'json',
        'formatversion': 2,  # version 2 is easier to work with
    }
    payload = requests.get(WIKIPEDIA_API_ENDPOINT, params=params).json()
    # YOUR CODE HERE
    if 'error' in payload:
        raise Error(payload['error'])
    if 'query' in payload:
        result=[]
        for x in payload['query']['pageids']:
            result.append(int(x))
        return result

# you may wish to skip this function until we cover using the Wikipedia API
def page_lengths(ids):
    """Find the length of a page according to the Mediawiki API.

    A page's length is measured in bytes which, for English-language pages, is
    approximately equal to the number of characters in the page's source.

    A useful reference for the Mediawiki API is this page:
    https://www.mediawiki.org/wiki/API:Info

    Arguments:
        ids (list of str): List of Wikipedia page ids.

    Returns:
        list of int: List of page lengths.

    """
    # YOUR CODE HERE
    params = {
        'action': 'query',
        'prop': 'revisions',
        'pageids': '|'.join(str(id) for id in ids),
        'rvprop' : 'size',
        'format': 'json',
        'formatversion': 2,  # version 2 is easier to work with
    }
    payloadt = requests.get(WIKIPEDIA_API_ENDPOINT, params=params).json()
    payload=payloadt['query']['pages']
    if 'error' in payload:
        raise Error(payload['error'])
    if 'query' in payload:
        kresult=[]
        for page in payload:
            kresult.extend(payload['query']['pages']['page']['revisions'][0]['size'])
        return kresult

# you may wish to skip this function until we cover using the Twitter API
def tweet_text_by_id(id, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    """Get the text of a tweet by its id.

    You may assume that valid credentials (``consumer_key``,
    ``consumer_secret``, ``access_token``, ``access_token_secret``) are passed.
    You are, however, free to ignore them and retrieve the full text of the
    tweet by some other means. It is possible to retrieve a tweet without using
    the API. You could parse the HTML of a normal HTTP response, for instance.

    Feel free to use ``requests_oauth``. You may assume it is installed.

    Arguments:
        id (int): Tweet id.
        consumer_key (str): Twitter API Consumer Key
        consumer_secret (str): Twitter API Consumer Secret
        access_token (str): Twitter API Access Token
        access_token_secret (str): Twitter API Access Token Secret

    Returns:
        str: The text of the specified tweet.

    """
    # YOUR CODE HERE

    url = "https://api.twitter.com/1.1/statuses/show.json?id="+str(id)
    auth = OAuth1(consumer_key, consumer_secret, access_token,access_token_secret)
    response=requests.get(url, auth=auth)
    return response['text']
  
# additional practice with two-mode networks / bipartite graphs

def incidence_matrix_from_user_mentions(user_mentions_list):
    """Construct an incidence matrix from user mentions.

    Given user mentions (aka "@-mentions" or "at-mentions") associated with users,
    `user_mentions_list`, construct an incidence matrix.

    Recall from Newman 6.6 that an incidence matrix is the equivalent of an
    adjacency matrix for a bipartite network. It's a rectangular matrix with
    shape `g` x `n`, where `g` is the number of groups and `n` is the the
    number of participants in the network. Here `g` is the number of unique
    targets of user mentions and `n` is the number of elements (lists) in the
    list, `user_mentions_list`.

    An incidence matrix is different from an adjacency matrix. For example,
    suppose `user_mentions_list` is a list of the following lists:

    - [@nytimes]
    - [@nytimes, @washtimes]
    - [@foxandfriends]
    - [@foxandfriends]

    One would expect as a result the following incidence matrix:

        [[ 0.,  0.,  1.,  1.],
         [ 1.,  1.,  0.,  0.],
         [ 0.,  1.,  0.,  0.]]

    (The first row corresponds to '@foxandfriends', the second row corresponds
    to '@nytimes', and the third row corresponds to '@washtimes'.)

    This exercise should be easier than ``mentions_adjacency_matrix`` (from a
    previous assignment).  If you encountered difficulty with that problem,
    give this one a try.

    Arguments:

        user_mentions_list (list of list of str): List of user mentions

    Returns:
        array: Incidence matrix. Groups should be sorted name.

    """
    # YOUR CODE HERE
    # make unique list users
    newuserlist=[]
    
    for userlist in user_mentions_list:
        newuserlist.extend(userlist)
    uniquelist=set(newuserlist)
    users=list(uniquelist)
    
    c=0
    r=0
    rows=len(users)
    columns=len(user_mentions_list)
    imatrix=[[0 for p in range(columns)] for q in range(rows)]

    for user in users:
        for userlist in user_mentions_list:
            if user in userlist:
               imatrix[r][c]=1
            else:
               imatrix[r][c]=0
            c=c+1
        r=r+1
    return imatrix

# challenging problems


# `load_twitter_corpus` is a data loading function; do not modify
def load_twitter_corpus():
    """Load US Congress Twitter corpus.

    Returns a pandas DataFrame with the following columns:

    - ``screen_name`` Member of Congress' Twitter handle (unused)
    - ``party`` Party affiliation. 0 is Democratic, 1 is Republican
    - ``tweets`` Text of five tweets concatenated together.

    Each record contains multiple tweets connected by a space. Grouping tweets
    together is not strictly necessary.

    Returns:

        pandas.DataFrame: DataFrame with tweets.

    """
    # data loading function; do not modify
    return pd.read_csv(TWITTER_DATA_FILENAME)

def get_user_mentions(tweet_list):
    # YOUR CODE HERE
    string=''.join(tweet_list)
    match=re.findall(r"@(\w+)",string)
    result=[]
    for string in tweet_list:
        match=re.findall(r"@(\w+)",string)
        result.append(len(match))
    return result


def predict_party(tweet, twitter_corpus):
    """Predict the party affiliation given the text of a tweet.

    ``tweet`` may be a group of tweets concatenated together. ``twitter_corpus``
    is passed as an argument to avoid having to load it over and over again
    when `predict_party` is called repeatedly.

    The precise strategy used for prediction is left entirely up to you.
    Nearest neighbors is a perfectly valid strategy. You might also consider
    the @-mentions in the tweet as a possible input to your model.

    Since members of US Congress tweet in very distinctive ways depending on
    party affiliation, a predictive model might be expected to achieve
    out-of-sample accuracy as high as 90% or even 95%. Not all classification
    tasks will be this easy.

    Arguments:

        tweet (str): a tweet (or more than one tweet) from a member of Congress as a Python string.
        twitter_corpus (pandas.DataFrame): DataFrame returned by ``load_twitter_corpus``.

    Returns:
        int: 0 is Democratic, 1 is Republican.

    """
    # YOUR CODE HERE
    mentions_tweet=get_user_mentions(tweet)
    l2=len(mentions_tweet)
    min=l2
    for index,rows in twitter_corpus.iterrows():
        mentions_tweetlist=get_user_mentions(rows['tweets'])
        l1=len(mentions_tweetlist)
        comparelist=list(set(mentions_tweetlist)-set(mentions_tweet))
        l3=len(comparelist)
     #calculation of lists    
        lt=l1-l2
        temp=l3-lt
     #finding max nearest party with min distance       
        if min>temp :
           min=temp
           party=rows['party']
    return party       


def predict_party_proba(tweet, twitter_corpus):
    """Predict the probability of Republican party affiliation given the text of a tweet.

    See ``predict_party`` for details. This function differs from ``predict_party`` in
    that it returns the probability of a tweet being from a Republican member of congress.

    Arguments:

        tweet (str): a tweet (or more than one tweet) from a member of Congress as a Python string.
        twitter_corpus (pandas.DataFrame): DataFrame returned by ``load_twitter_corpus``.

    Returns:
        float: probability between 0 and 1 of tweet being authored by a Republican.

    """
    # YOUR CODE HERE
    mentions_tweet=get_user_mentions(tweet)
    l2=len(mentions_tweet)
    repubparty=0
    maxprob=0
    for index,rows in twitter_corpus.iterrows():
        mentions_tweetlist=get_user_mentions(rows['tweets'])
        l1=len(mentions_tweetlist)
        comparelist=list(set(mentions_tweetlist)-set(mentions_tweet))
        l3=len(comparelist)
        #calculation of no.of mentions matched   
        lt=l1-l2
        temp=l3-lt
        if rows['party']==1:
           #no.of mentions matched by total no.of mentions
           prob=temp/l1
           if prob>maxprob:
              maxprob=prob
    return maxprob


# DO NOT EDIT CODE BELOW THIS LINE


class TestAssignment4(unittest.TestCase):

    def test_count_user_mentions1(self):
        tweets = [
          """RT @HouseGOP: The #StateOfTheUnion isn't strong for the 8.7 million Americans out of work.""",
          """@HouseGOP Good morning.""",
        ]
        self.assertEqual(count_user_mentions(tweets), [1, 1])


    def test_page_ids1(self):
        titles = ['Albert Einstein']
        ids = [736]
        self.assertEqual(page_ids(titles), ids)


    def test_page_lengths1(self):
        ids = [736]
        expected = [137000]  # NOTE: this number changes over time
        lengths = page_lengths(ids)
        self.assertEqual(len(lengths), 1)
        self.assertGreater(lengths[0], 0)
        self.assertGreater(lengths[0], expected[0] >> 3)
        self.assertLess(lengths[0], expected[0] << 3)

    def test_tweet_text_by_id1(self):
        id = 685423981671936001
        expected = """Getting ready to go live"""
        text = tweet_text_by_id(
            id,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
        )
        # NOTE: skipping this test here since it will fail without
        # the appropriate values. If you understand what is happening
        # here, feel free to uncomment the following line:
        # self.assertEqual(text[:len(expected)], expected)


    def test_incidence_matrix_from_user_mentions1(self):
        user_mentions = [
            ['@nytimes'],
            ['@nytimes', '@washtimes'],
            ['@foxandfriends'],
            ['@foxandfriends'],
        ]
        B = incidence_matrix_from_user_mentions(user_mentions)
        self.assertEqual(B.shape, (3, 4))


    def test_load_twitter_corpus1(self):
        df = load_twitter_corpus()
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 100)


    def test_predict_party1(self):
        df = load_twitter_corpus()
        party = predict_party("""RT @HouseGOP: The #StateOfTheUnion is strong.""", df)
        self.assertIn(party, {0, 1})


    def test_predict_party_proba1(self):
        df = load_twitter_corpus()
        party_proba = predict_party_proba("""RT @HouseGOP: The #StateOfTheUnion is strong.""", df)
        self.assertGreaterEqual(party_proba, 0)
        self.assertLessEqual(party_proba, 1)



if __name__ == '__main__':
    unittest.main()
