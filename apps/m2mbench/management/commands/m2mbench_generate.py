import os, argparse

from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.conf import settings

from apps.m2mbench.models import Board, Thread, Post

from ._base_command import _BaseCommand


class Command(_BaseCommand):
    help = 'Generate m2mbench fixtures according to command line arguments or settings.'
    
    def get_next_board_pk(self):
        try:
            return Board.objects.order_by('-id')[0].id + 1
        except IndexError:
            return 1
        except Board.DoesNotExist:
            return 1
    
    def get_next_thread_pk(self):
        try:
            return Thread.objects.order_by('-id')[0].id + 1
        except IndexError:
            return 1
        except Thread.DoesNotExist:
            return 1
    
    def get_next_post_pk(self):
        try:
            return Post.objects.order_by('-id')[0].id + 1
        except IndexError:
            return 1
        except Post.DoesNotExist:
            return 1
    
    def add_arguments(self, parser):
        parser.add_argument(
            '-nb', '--num-boards',
            dest='num_boards',
            metavar='NUM_BOARDS',
            type=self.positive_int,
            default=settings.JSONBENCH_NUM_BOARDS,
            help=('A positive integer representing the number of boards to generate. '
                  'Default is {}.'.format(settings.JSONBENCH_NUM_BOARDS))
        )
        parser.add_argument(
            '-nt', '--num-threads',
            dest='num_threads',
            metavar='NUM_THREADS',
            type=self.positive_int,
            default=settings.JSONBENCH_NUM_THREADS,
            help=('A positive integer representing the number of threads per board to generate. '
                  'Default is {}.'.format(settings.JSONBENCH_NUM_THREADS))
        )
        parser.add_argument(
            '-np', '--num-posts',
            dest='num_posts',
            metavar='NUM_POSTS',
            type=self.positive_int,
            default=settings.JSONBENCH_NUM_POSTS,
            help=('A positive integer representing the number of posts per thread to generate. '
                  'Default is {}.'.format(settings.JSONBENCH_NUM_POSTS))
        )
        default_board_pk = self.get_next_board_pk()
        parser.add_argument(
            '-bpk', '--board-pk',
            dest='board_pk',
            metavar='BOARD_PK',
            type=self.positive_int,
            default=default_board_pk,
            help=('A positive integer representing the starting board primary key. '
                  'Default is {}.'.format(default_board_pk))
        )
        default_thread_pk = self.get_next_thread_pk()
        parser.add_argument(
            '-tpk', '--thread-pk',
            dest='thread_pk',
            metavar='THREAD_PK',
            type=self.positive_int,
            default=default_thread_pk,
            help=('A positive integer representing the starting thread primary key. '
                  'Default is {}.'.format(default_thread_pk))
        )
        default_post_pk = self.get_next_post_pk()
        parser.add_argument(
            '-ppk', '--post-pk',
            dest='post_pk',
            metavar='POST_PK',
            type=self.positive_int,
            default=default_post_pk,
            help=('A positive integer representing the starting post primary key. '
                  'Default is {}.'.format(default_post_pk))
        )
        to_file_default = os.path.join(
            settings.BASE_DIR, 'apps', 'm2mbench', 'fixtures', 'm2mbench.json'
        )
        parser.add_argument(
            '-tf', '--to-file',
            dest='fixtures_file',
            metavar='FIXTURES_FILE',
            type=argparse.FileType('w'),
            default=to_file_default,
            help=('A path to the file to write out m2mbench fixture data. '
                  'Default is "{}".'.format(to_file_default))
        )
    
    def handle(self, *args, **options):
        num_boards = options.get('num_boards')
        num_threads = options.get('num_threads')
        num_posts = options.get('num_posts')
        board_pk = options.get('board_pk')
        thread_pk = options.get('thread_pk')
        post_pk = options.get('post_pk')
        fixtures_file = options.get('fixtures_file')
        
        m2mbench_list = []
        
        self.write_notice('==> num boards = {}'.format(num_boards))
        self.write_notice('==> num threads = {}'.format(num_threads))
        self.write_notice('==> num posts = {}'.format(num_posts))
        self.write_notice('==> start board pk = {}'.format(board_pk))
        self.write_notice('==> start thread pk = {}'.format(thread_pk))
        self.write_notice('==> start post pk = {}'.format(post_pk))
        self.write_notice('==> fixtures file = {}'.format(fixtures_file))
        
        for i in range(1, num_boards+1):
            m2mbench_list.append({
                "model": "m2mbench.board",
                "pk": board_pk,
                "fields": {
                    "name": 'm2mbench Board {}'.format(board_pk)
                }
            })
            self.write_notice('==> Board {}'.format(board_pk))
            for j in range(1, num_threads+1):
                m2mbench_list.append({
                    "model": "m2mbench.thread",
                    "pk": thread_pk,
                    "fields": {
                        "name": 'm2mbench Thread {} of Board {}'.format(thread_pk, board_pk),
                        "board": board_pk
                    }
                })
                if j % 10 == 0:
                    self.write_notice('    `--> Thread {} '.format(thread_pk), ending='', flush=True)
                for k in range(1, num_posts+1):
                    m2mbench_list.append({
                        "model": "m2mbench.post",
                        "pk": post_pk,
                        "fields": {
                            "name": 'm2mbench Post {} of Thread {} of Board {}'.format(
                                post_pk, thread_pk, board_pk
                            ),
                            "thread": thread_pk
                        }
                    })
                    if j % 10 == 0 and k % 100 == 0:
                        self.write_notice('.', ending='', flush=True)
                    post_pk += 1
                if j % 10 == 0:
                    self.write('')
                thread_pk += 1
            board_pk += 1
        
        self.write_to_json_file(fixtures_file, m2mbench_list, json_indent=4)
        self.write_success('~~ finished! ~~')
