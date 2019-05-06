import operator
import collections
cnt = collections.Counter()
import json
import pandas as pd
from os import listdir
from os.path import join, isfile
import gzip
from datetime import datetime
import time

#Q1 : Top 100 subreddits based on number of unique users

inputfile = '/l/research/social-media-mining/public/RC_2015-01-random-sample-1000000.jsonlines'
split = '/l/research/social-media-mining/public/comments-2015-split'
com_path = '/l/research/social-media-mining/public/reddit/comments'
sub_path = '/l/research/social-media-mining/public/reddit/submissions'
comments = [f for f in listdir(com_path) if isfile(join(com_path, f))]
submissions = [f for f in listdir(sub_path) if isfile(join(sub_path, f))]
outputfile = "reddit-statistics.csv"

posts = []
with open(inputfile) as fh:
    for line in fh:
        line_dict = json.loads(line)
        posts.append(line_dict)

top = {}
user = {}
for i in posts:
    if i['subreddit'] in top:
        user[i['subreddit']] = []
        if i['author'] not in user[i['subreddit']]:
            user[i['subreddit']].append(i['author'])
            top[i['subreddit']] += 1
    else:
        top[i['subreddit']] = 1

sort = sorted(top.items(), key = operator.itemgetter(1), reverse = True)
top_100 = sort[:100]

top_100_dict = {i[0]:i[1] for i in top_100}
dt = pd.DataFrame(list(top_100_dict.items()), columns = ['Top 100 Subreddits', 'Unique Users'])
dt.to_csv(outputfile, sep = ' ')

#Q2 Percentage of content for each subreddit in the top 100

content = {}
total = 0
for i in posts:
    if i['subreddit'] in top_100_dict:
        if i['subreddit'] in content:
                content[i['subreddit']] += 1
        else:
                content[i['subreddit']] = 1
        total += 1

for key, value in content.items():
    value = value / total
    content[key] = value

dt = pd.DataFrame(list(content.items()), columns = ['Top 100 Subreddits', 'Percentage of Content'])
dt.to_csv(outputfile, sep = ' ', mode = 'a')

#Q4 CR20

top_20 = sort[:20]
top20 = 0
for i in top_20:
    top20 += i[1]
cr20 = top20/total

"""#Q5 Churn

churn = {}
for i in posts:
    if i['subreddit'] in churn:
        churn[i['subreddit']].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['created_utc'])))
    else:
        churn[i['subreddit']] = int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['created_utc'])))
print(churn)
thing = listdir(split)
thing = sorted(thing)
month = []
for i in thing:
    month.append(i)

jan = []
feb = []
for i in month:
    url = split + '/' + i
    with gzip.open(url) as fh:
        for line in fh:
            line_dict = json.loads(line)
            if '2015-01' in time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(line_dict['created_utc'])):
                jan.append(line_dict)
            elif '2015-02' in time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(line_dict['created_utc'])):
                feb.append(line_dict)
print(jan[0], feb[0])"""
