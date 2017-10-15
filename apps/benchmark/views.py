from django.shortcuts import render
from django.conf import settings
from django.apps import apps

def index(request):
    cd = {'apps': []}
    for app in settings.JSONBENCH_APPS:
        _app = apps.get_app_config(app)
        cd['apps'].append(('{}:index'.format(_app.label), _app.label))
    return render(request, 'benchmark/index.html', cd)
