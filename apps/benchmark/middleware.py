import sys
import cProfile
from io import StringIO

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ProfilerMiddleware(MiddlewareMixin):
    #def __init__(self, get_response):
    #    self.get_response = get_response
    #    # One-time configuration and initialization.
    #
    #def __call__(self, request):
    #    # Code to be executed for each request before
    #    # the view (and later middleware) are called.
    #
    #    response = self.get_response(request)
    #
    #    # Code to be executed for each request/response after
    #    # the view is called.
    #
    #    return response
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)
    
    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            response.content += bytes('<pre>%s</pre>' % out.getvalue(), 'utf-8')
        return response
