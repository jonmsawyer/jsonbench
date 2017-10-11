#!/usr/bin/env python

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from apps import jsonbench
from apps import m2mbench


jsonbench_list = []
m2mbench_list = []
num_boards = 10
num_threads = 100
num_posts = 1000
board_pk = 0
thread_pk = 0
post_pk = 0

for i in range(1, num_boards+1):
    board_pk += 1
    jsonbench_list.append({
        "model": "jsonbench.board",
        "pk": board_pk,
        "fields": {
            "name": 'jsonbench Board {}'.format(i)
        }
    })
    m2mbench_list.append({
        "model": "m2mbench.board",
        "pk": board_pk,
        "fields": {
            "name": 'm2mbench Board {}'.format(i)
        }
    })
    print('==> Board {}'.format(i))
    sys.stdout.flush()
    for j in range(1, num_threads+1):
        thread_pk += 1
        jsonbench_list.append({
            "model": "jsonbench.thread",
            "pk": thread_pk,
            "fields": {
                "name": 'jsonbench Thread {} of Board {}'.format(j, i),
                "board": board_pk
            }
        })
        m2mbench_list.append({
            "model": "m2mbench.thread",
            "pk": thread_pk,
            "fields": {
                "name": 'm2mbench Thread {} of Board {}'.format(j, i),
                "board": board_pk
            }
        })
        if j % 10 == 0:
            print('    `--> Thread {} '.format(j), end='')
            sys.stdout.flush()
        for k in range(1, num_posts+1):
            post_pk += 1
            jsonbench_list.append({
                "model": "jsonbench.post",
                "pk": post_pk,
                "fields": {
                    "name": 'jsonbench Post {} of Thread {} of Board {}'.format(k, j, i),
                    "thread": thread_pk
                }
            })
            m2mbench_list.append({
                "model": "m2mbench.post",
                "pk": post_pk,
                "fields": {
                    "name": 'm2mbench Post {} of Thread {} of Board {}'.format(k, j, i),
                    "thread": thread_pk
                }
            })
            if j % 10 == 0 and k % 100 == 0:
                print('.', end='')
                sys.stdout.flush()
        if j % 10 == 0:
            print('')
        
    print('writing to file jsonbench.board{:02d}.json ... '.format(i), end='')
    sys.stdout.flush()
    with open('jsonbench.board{:02d}.json'.format(i), 'w') as fh:
        fh.write(json.dumps(jsonbench_list, indent=4))
    print('success!')
    jsonbench_list.clear()
    
    print('writing to file m2mbench.board{:02d}.json ... '.format(i), end='')
    sys.stdout.flush()
    with open('m2mbench.board{:02d}.json'.format(i), 'w') as fh:
        fh.write(json.dumps(m2mbench_list, indent=4))
    print('success!')
    m2mbench_list.clear()

print('~~ Finished! ~~')
