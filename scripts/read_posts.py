#!/usr/bin/env python

import sys, os, json, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jsonbench.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User

from apps.jsonbench.models import Post as jPost, ForumUser
from apps.m2mbench.models import Post as mPost


try:
    username = str(sys.argv[1]).strip()
except Exception as e:
    os_user = os.environ.get('USERNAME') or os.environ.get('USER', '')
    try:
        username = input('Please enter a username to read posts as ({}): '.format(os_user))
        if username.strip() is '':
            username = os_user
        if username is None or username is '':
            raise Exception('invalid username: {}'.format(username))
    except Exception as e2:
        print('Error! could not obtain proper username: {}'.format(e2))
        print('Usage: read_posts.py {username}')
        sys.exit(1)

try:
    jsonbench_user = ForumUser.objects.get(user__username=username)
    m2mbench_user = User.objects.get(username=username)
except Exception as e:
    print('Error! argument required: username')
    print('Usage: read_posts.py {username}')
    sys.exit(1)

print('deleting read jsonbench posts ... ', end='', flush=True)
jsonbench_user.posts_read = None
jsonbench_user.save()
print('success!')

count = 0
m2mbench_read_posts = mPost.objects.filter(readers__username=username)
print('deleting {} m2mbench posts ...'.format(m2mbench_read_posts.count()), end='', flush=True)
for m2mbench_read_post in m2mbench_read_posts:
    count += 1
    if count % 1000 == 0:
        print(count, end='', flush=True)
    elif count % 100 == 0:
        print('.', end='', flush=True)
    m2mbench_read_post.readers.clear()
print(' ... success!')
print('deleted {} m2mbench readers'.format(count))

# Integer in the domain on [0, 100]
percent_of_posts_to_read = 40
print('reading {}% of posts'.format(percent_of_posts_to_read))

jsonbench_num_posts = jPost.objects.count()
m2mbench_num_posts = mPost.objects.count()
print('jsonbench has {} posts'.format(jsonbench_num_posts))
print('m2mbench has {} posts'.format(m2mbench_num_posts))

jsonbench_ids = []
m2mbench_ids = []

print('generating random ids for jsonbench ... ', end='', flush=True)
for i in range(1, jsonbench_num_posts+1):
    if math.floor(random.random()*100) <= percent_of_posts_to_read:
        if (len(jsonbench_ids) / jsonbench_num_posts)*100 >= percent_of_posts_to_read:
            break
        jsonbench_ids.append(i)
        if i % 1000 == 0:
            print(i, end='', flush=True)
        elif i % 100 == 0:
            print('.', end='', flush=True)
print(' ... success!')
print('generated {} jsonbench ids'.format(len(jsonbench_ids)))

print('generating random ids for m2mbench ... ', end='', flush=True)
for i in range(1, m2mbench_num_posts+1):
    if math.floor(random.random()*100) <= percent_of_posts_to_read:
        if (len(m2mbench_ids) / m2mbench_num_posts)*100 >= percent_of_posts_to_read:
            break
        m2mbench_ids.append(i)
        if i % 1000 == 0:
            print(i, end='', flush=True)
        elif i % 100 == 0:
            print('.', end='', flush=True)
print(' ... success!')
print('generated {} m2mbench ids'.format(len(m2mbench_ids)))

jdict = {}
chunk_range = 500

count = 0
print('building jsonbench dict ... ', end='', flush=True)
for i in range(0, len(jsonbench_ids), chunk_range):
    chunk = jsonbench_ids[i:i+chunk_range]
    len_chunk = len(chunk)
    count += len_chunk
    if count % (chunk_range*10) == 0:
        print(count, end='', flush=True)
    elif count % chunk_range == 0:
        print('.', end='', flush=True)
    jsonbench_posts = jPost.objects.filter(pk__in=chunk)
    for jsonbench_post in jsonbench_posts:
        if jsonbench_post.thread.id not in jdict:
            jdict.update({jsonbench_post.thread.id: []})
        jdict.get(jsonbench_post.thread.id).append(jsonbench_post.id)
print(' ... success!')

print('reading posts for jsonbench ... ', end='', flush=True)
jsonbench_user = ForumUser.objects.get(user__username=username)
jsonbench_user.posts_read = json.dumps(jdict, indent=4)
jsonbench_user.save()
print(' ... success!')

count = 0
print('reading posts for m2mbench ... ', end='', flush=True)
for i in range(0, len(m2mbench_ids), chunk_range):
    chunk = m2mbench_ids[i:i+chunk_range]
    len_chunk = len(chunk)
    count += len_chunk
    if count % (chunk_range*10) == 0:
        print(count, end='', flush=True)
    elif count % chunk_range == 0:
        print('.', end='', flush=True)
    m2mbench_posts = mPost.objects.filter(pk__in=chunk)
    for m2mbench_post in m2mbench_posts:
        m2mbench_post.readers.add(m2mbench_user)
print(' ... success!')
