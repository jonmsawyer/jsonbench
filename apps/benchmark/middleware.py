import sys
import cProfile
from io import StringIO
from pprint import pprint

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from apps.benchmark.models import BenchmarkSuite


class ProfilerMiddleware(MiddlewareMixin):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.latest_exception = ''
            try:
                self.benchmarksuite = BenchmarkSuite.NewWebBenchmarkSuite(request, 'ProfilerMiddleware')
                self.benchmarksuite.start()
                self.benchmarksuite.next_step(request, 'ProfilerMiddleware')
            except Exception as e:
                self.benchmarksuite = None
                self.latest_exception = str(e)
            self.profiler = cProfile.Profile()
            request.benchmarksuite = self.benchmarksuite
            args = (request,) + callback_args
            ret =  self.profiler.runcall(callback, *args, **callback_kwargs)
            self.profiler.create_stats()
            try:
                self.benchmarksuite.stop()
            except:
                pass
            return ret
        else:
            request.benchmarksuite = None
    
    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            if self.latest_exception:
                exception_string = '<pre>{}</pre>'.format(self.latest_exception)
            else:
                exception_string = ''
            response.content += bytes('%s<pre>%s</pre>' % (
                exception_string, out.getvalue()
            ), 'utf-8')
            try:
                self.benchmarksuite.log(out.getvalue())
            except:
                pass
        return response
