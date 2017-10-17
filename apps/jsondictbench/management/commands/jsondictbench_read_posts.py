import json, math, random

from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.conf import settings

from apps.jsondictbench.models import Post, ForumUser

from ._base_command import _BaseCommand


class Command(_BaseCommand):
    help = 'Randomly read a percentage of posts in the jsondictbench forum.'
    
    def get_first_post_pk(self):
        try:
            return Post.objects.order_by('id')[0].id
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
                  '"jsondictbench_generate" command, followed by "jsondictbench_load" command). '
                  'Note: setting ORDER to "random" makes this option useless. '
                  'Default is {}.'.format(default_post_start_pk))
        )
    
    def handle(self, *args, **options):
        username = options.get('username')
        percent = options.get('percent')
        order = options.get('order')
        post_start_pk = options.get('post_start_pk')
        
        chunk_range = 500
        jsondictbench_num_posts = Post.objects.count()
        jsondictbench_ids = []
        jdict = {}
        
        if (order == "sequential") and (post_start_pk > jsondictbench_num_posts):
            raise CommandError('POST_START_PK value of {} cannot be greater than the number of '
                               'posts in the database (number of posts = {})'
                               .format(post_start_pk, jsondictbench_num_posts))
        
        self.write_notice('==> username = {}'.format(username))
        self.write_notice('==> percent of posts to read = {}'.format(percent))
        self.write_notice('==> order = {}'.format(order))
        self.write_notice('==> post start pk = {}'.format(post_start_pk))
        self.write_notice('==> chunk range = {}'.format(chunk_range))
        self.write_notice('==> jsondictbench num posts = {}'.format(jsondictbench_num_posts))
        
        try:
            jsondictbench_user = ForumUser.objects.get(user__username=username)
        except ForumUser.DoesNotExist as e:
            try:
                user = User.objects.get(username=username)
                user.save() # in case the User exists, but not an instance of ForumUser
                jsondictbench_user = ForumUser.objects.get(user__username=username)
            except:
                raise CommandError('could not get or initialize user `{}`, does the user exist?'
                                   .format(username))
        
        self.write_notice('deleting read jsondictbench posts ... ', ending='', flush=True)
        jsondictbench_user.posts_read = None
        jsondictbench_user.save()
        self.write_success('success!')
        
        self.write_notice('generating {} ids for jsondictbench ... '.format(order),
                          ending='', flush=True)
        if order == 'random':
            # caveat: this will still randomly mark posts as read according to the json dictionary
            #         even if that post does not exist. see options for "jsondictbench_generate"
            #         to see how this is normally possible. TODO: fix?
            for i in range(1, jsondictbench_num_posts+1):
                if math.floor(random.random()*100) <= percent:
                    if (len(jsondictbench_ids) / jsondictbench_num_posts)*100 >= percent:
                        break
                    jsondictbench_ids.append(i)
                    if i % 1000 == 0:
                        self.write_notice(str(i)+'.', ending='', flush=True)
                    elif i % 100 == 0:
                        self.write_notice('.', ending='', flush=True)
        elif order == 'sequential':
            # caveat: this will still sequentially mark posts as read according to the json
            #         dictionary even if that post does not exist. see options for
            #         "jsondictbench_generate" to see how this is normally possible. TODO: fix?
            for i in range(post_start_pk, jsondictbench_num_posts+1):
                if (len(jsondictbench_ids) / jsondictbench_num_posts)*100 >= percent:
                    break
                jsondictbench_ids.append(i)
                if i % 1000 == 0:
                    self.write_notice(str(i)+'.', ending='', flush=True)
                elif i % 100 == 0:
                    self.write_notice('.', ending='', flush=True)
        self.write_success(' ... success!')
        self.write_notice('generated {} jsondictbench ids'.format(len(jsondictbench_ids)))
        
        count = 0
        self.write_notice('building jsondictbench dict ... ', ending='', flush=True)
        for i in range(0, len(jsondictbench_ids), chunk_range):
            chunk = jsondictbench_ids[i:i+chunk_range]
            len_chunk = len(chunk)
            count += len_chunk
            if count % (chunk_range*10) == 0:
                self.write_notice(str(count)+'.', ending='', flush=True)
            elif count % chunk_range == 0:
                self.write_notice('.', ending='', flush=True)
            jsondictbench_posts = Post.objects.filter(pk__in=chunk)
            for jsondictbench_post in jsondictbench_posts:
                if jsondictbench_post.thread.id not in jdict:
                    jdict.update({jsondictbench_post.thread.id: []})
                jdict.get(jsondictbench_post.thread.id).append(jsondictbench_post.id)
        self.write_success(' success!')
        
        self.write_notice('reading posts for jsondictbench ... ', ending='', flush=True)
        jsondictbench_user.posts_read = json.dumps(jdict, indent=4)
        jsondictbench_user.save()
        self.write_success(' success!')
        self.write_success('~~ finished! ~~ ')
