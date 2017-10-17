import json
from io import TextIOWrapper

from django.core.management.base import BaseCommand, CommandError


class _BaseCommand(BaseCommand):
    ##################################################################
    # Style objects reference from django.core.management.color.Style:
    #
    #     self.style.ERROR
    #     self.style.ERROR_OUTPUT
    #     self.style.HTTP_BAD_REQUEST
    #     self.style.HTTP_INFO
    #     self.style.HTTP_NOT_FOUND
    #     self.style.HTTP_NOT_MODIFIED
    #     self.style.HTTP_REDIRECT
    #     self.style.HTTP_SERVER_ERROR
    #     self.style.HTTP_SUCCESS
    #     self.style.MIGRATE_HEADING
    #     self.style.MIGRATE_LABEL
    #     self.style.NOTICE
    #     self.style.SQL_COLTYPE
    #     self.style.SQL_FIELD
    #     self.style.SQL_KEYWORD
    #     self.style.SQL_TABLE
    #     self.style.SUCCESS
    #     self.style.WARNING
    #
    ##################################################################
    
    def write(self, *args, **kwargs):
        try:
            flush = kwargs.pop('flush')
        except KeyError:
            flush = False
        self.stdout.write(*args, **kwargs)
        if flush:
            self.stdout.flush()
    
    def write_success(self, *args, **kwargs):
        self.write(self.style.SUCCESS(*args), **kwargs)
    
    def write_notice(self, *args, **kwargs):
        self.write(self.style.NOTICE(*args), **kwargs)
    
    def write_warning(self, *args, **kwargs):
        self.write(self.style.WARNING(*args), **kwargs)
    
    def write_error(self, *args, **kwargs):
        self.write(self.style.ERROR(*args), **kwargs)
    
    def write_to_json_file(self, filename, content, json_indent=4):
        self.write_to_file(filename, content, to_json=True, json_indent=json_indent)
    
    def write_to_file(self, filename, content, to_json=False, json_indent=4):
        if isinstance(filename, str):
            fname = filename
            ftype = 'string'
        elif isinstance(filename, TextIOWrapper):
            fname = filename.name
            ftype = 'file'
        else:
            raise CommandError('{} is not of type str or of type io.TextIOWrapper'.format(filename))
        self.write_notice('writing to file "{}" ... '.format(fname), ending='', flush=True)
        if ftype == 'string':
            with open(filename, 'a') as fh:
                if to_json:
                    fh.write(json.dumps(content, indent=json_indent))
                else:
                    fh.write(str(content))
        elif ftype == 'file':
            if to_json:
                filename.write(json.dumps(content, indent=json_indent))
            else:
                filename.write(str(content))
        self.write_success('success!')
    
    def positive_int(self, string):
        value = int(string)
        if value <= 0:
            raise CommandError('{} is not a positive integer'.format(string))
        return value
