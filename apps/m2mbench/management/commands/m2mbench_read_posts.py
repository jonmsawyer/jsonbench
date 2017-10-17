import json, math, random

from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.conf import settings

from apps.m2mbench.models import Post

from ._base_command import _BaseCommand


class Command(_BaseCommand):
    help = 'Randomly read a percentage of posts in the m2mbench forum.'
    
    def get_first_post_pk(self):
        try:
            return Post.objects.order_by('id')[0].id
        except IndexError:
            return 1
        except Post.DoesNotExist:
            return -1
    
    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            metavar='USERNAME',
            help='The username of the user that will read the posts'
        )
        parser.add_argument(
            '-p', '--percent',
            dest='percent',
            metavar='PERCENT',
            type=int,
            default=settings.JSONBENCH_PERCENT_POSTS_TO_READ,
            choices=range(0, 101),
            help=('An integer of the percent of posts to read in the domain of [0, 100]. '
                  'Default is {}.'.format(settings.JSONBENCH_PERCENT_POSTS_TO_READ))
        )
        parser.add_argument(
            '-o', '--order',
            dest='order',
            metavar='ORDER',
            default='random',
            choices=['random', 'sequential'],
            help=('If "random", randomly read PERCENT of posts. If "sequential", sequentially read '
                  'PERCENT of post starting at POST_START_PK. '
                  'Default is "{}".'.format('random'))
        )
        default_post_start_pk = self.get_first_post_pk()
        parser.add_argument(
            '-pspk', '--post-start-pk',
            dest='post_start_pk',
            metavar='POST_START_PK',
            type=int,
            default=default_post_start_pk,
            help=('If ORDER is set to "sequential", then start sequentially reading posts ' 
                  'beginning at POST_START_PK. If the default shown next is -1, '
                  'then there are no posts to read yet (you might want to first start with '
                  '"m2mbench_generate" command, followed by "m2mbench_load" command). '
                  'Note: setting ORDER to "random" makes this option useless. '
                  'Default is {}.'.format(default_post_start_pk))
        )
    
    def handle(self, *args, **options):
        username = options.get('username')
        percent = options.get('percent')
        order = options.get('order')
        post_start_pk = options.get('post_start_pk')
        
        chunk_range = 500
        m2mbench_num_posts = Post.objects.count()
        m2mbench_ids = []
        jdict = {}
        
        if (order == "sequential") and (post_start_pk > m2mbench_num_posts):
            raise CommandError('POST_START_PK value of {} cannot be greater than the number of '
                               'posts in the database (number of posts = {})'
                               .format(post_start_pk, m2mbench_num_posts))
        
        self.write_notice('==> username = {}'.format(username))
        self.write_notice('==> percent of posts to read = {}'.format(percent))
        self.write_notice('==> order = {}'.format(order))
        self.write_notice('==> post start pk = {}'.format(post_start_pk))
        self.write_notice('==> chunk range = {}'.format(chunk_range))
        self.write_notice('==> m2mbench num posts = {}'.format(m2mbench_num_posts))
        
        try:
            m2mbench_user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise CommandError('could not get or initialize user `{}`, does the user exist?'
                               .format(username))
        
        count = 0
        m2mbench_read_posts = Post.objects.filter(readers__username=username)
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
        
        self.write_notice('generating {} ids for m2mbench ... '.format(order),
                          ending='', flush=True)
        if order == 'random':
            # caveat: this will still randomly mark posts as read according to the json dictionary
            #         even if that post does not exist. see options for "m2mbench_generate"
            #         to see how this is normally possible. TODO: fix?
            for i in range(1, m2mbench_num_posts+1):
                if math.floor(random.random()*100) <= percent:
                    if (len(m2mbench_ids) / m2mbench_num_posts)*100 >= percent:
                        break
                    m2mbench_ids.append(i)
                    if i % 1000 == 0:
                        self.write_notice(str(i)+'.', ending='', flush=True)
                    elif i % 100 == 0:
                        self.write_notice('.', ending='', flush=True)
        elif order == 'sequential':
            # caveat: this will still sequentially mark posts as read according to the json
            #         dictionary even if that post does not exist. see options for
            #         "m2mbench_generate" to see how this is normally possible. TODO: fix?
            for i in range(post_start_pk, m2mbench_num_posts+1):
                if (len(m2mbench_ids) / m2mbench_num_posts)*100 >= percent:
                    break
                m2mbench_ids.append(i)
                if i % 1000 == 0:
                    self.write_notice(str(i)+'.', ending='', flush=True)
                elif i % 100 == 0:
                    self.write_notice('.', ending='', flush=True)
        self.write_success(' ... success!')
        self.write_notice('generated {} m2mbench ids'.format(len(m2mbench_ids)))
        
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
            m2mbench_posts = Post.objects.filter(pk__in=chunk)
            for m2mbench_post in m2mbench_posts:
                m2mbench_post.readers.add(m2mbench_user)
        print(' ... success!')
        self.write_success('~~ finished! ~~ ')
