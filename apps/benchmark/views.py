from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.apps import apps

@login_required
def index(request):
    cd = {'apps': []}
    for app in settings.JSONBENCH_APPS:
        _app = apps.get_app_config(app)
        cd['apps'].append(('{}:index'.format(_app.label), _app.label))
    cd['prof'] = 'prof' if 'prof' in request.GET else ''
    cd['request_dict'] = dict(request)
    return render(request, 'benchmark/index.html', cd)
