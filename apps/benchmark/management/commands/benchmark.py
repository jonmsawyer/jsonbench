from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from apps.jsonbench.models import Board as jBoard
from apps.jsonbench.models import Thread as jThread
from apps.jsonbench.models import Post as jPost
from apps.jsonbench.models import ForumUser
from apps.m2mbench.models import Board as mBoard
from apps.m2mbench.models import Thread as mThread
from apps.m2mbench.models import Post as mPost


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        # do stuff
