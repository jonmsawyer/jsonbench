import os, argparse
from io import TextIOWrapper

from django.core import management
from django.core.management.base import CommandError
from django.conf import settings

from ._base_command import _BaseCommand

class Command(_BaseCommand):
    help = 'Load jsondictbench fixtures.'
    
    def add_arguments(self, parser):
        from_file_default = os.path.join(
            settings.BASE_DIR, 'apps', 'jsondictbench', 'fixtures', 'jsondictbench.json'
        )
        parser.add_argument(
            '-ff', '--from-file',
            dest='fixtures_file',
            metavar='FIXTURES_FILE',
            type=argparse.FileType('r'),
            default=from_file_default,
            help=('A path to the file to load jsondictbench fixture data. '
                  'Default is "{}".'.format(from_file_default))
        )
    
    def handle(self, *args, **options):
        fixtures_file = options.get('fixtures_file')
        if isinstance(fixtures_file, TextIOWrapper):
            fname = fixtures_file.name
            fixtures_file.close() # we'll read from this file later
        elif isinstance(fixtures_file, str):
            fname = fixtures_file
        else:
            raise CommandError('{} is not of type str or of type io.TextWrapper'
                               .format(fixtures_file))
        self.write_notice('==> please wait while we load fixture data from "{}" ... '.format(fname),
                          ending='', flush=True)
        management.call_command('loaddata', fname)
        self.write_success('success!')
        self.write_success('~~ finished! ~~')
