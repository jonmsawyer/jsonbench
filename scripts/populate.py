#!/usr/bin/env python

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jsonbench.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from apps import jsonbench
from apps import m2mbench


jsonbench.models.Board.objects.all().delete()
jsonbench.models.Thread.objects.all().delete()
jsonbench.models.Post.objects.all().delete()
m2mbench.models.Board.objects.all().delete()
m2mbench.models.Thread.objects.all().delete()
m2mbench.models.Post.objects.all().delete()

num_boards = 10
num_threads = 100
num_posts = 1000

for i in range(1, num_boards+1):
    jb = jsonbench.models.Board(name='jsonbench Board {}'.format(i))
    mb = m2mbench.models.Board(name='m2mbench Board {}'.format(i))
    jb.save()
    mb.save()
    print('==> Board {}'.format(i))
    sys.stdout.flush()
    for j in range(1, num_threads+1):
        jt = jsonbench.models.Thread(name='jsonbench Thread {} of {}'.format(j, jb.name), board=jb)
        mt = m2mbench.models.Thread(name='m2mbench Thread {} of {}'.format(j, mb.name), board=mb)
        jt.save()
        mt.save()
        print('    `--> Thread {} '.format(j), end='')
        sys.stdout.flush()
        for k in range(1, num_threads+1):
            jp = jsonbench.models.Post(name='jsonbench Post {} of {} of {}'.format(k, jt.name, jb.name), thread=jt)
            mp = m2mbench.models.Post(name='m2mbench Post {} of {} of {}'.format(k, mt.name, mb.name), thread=mt)
            jp.save()
            mp.save()
            if k % 10:
                print('.', end='')
                sys.stdout.flush()
        print('')
        sys.stdout.flush()
