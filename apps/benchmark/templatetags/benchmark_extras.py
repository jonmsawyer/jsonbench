import collections # For an OrderedDict[ionary]

from django import template
from django import forms
from django.utils.safestring import mark_safe
from django.db import models

register = template.Library()

def to_dict(ob):
    attrs = dir(ob)
    dict_list = []
    for attr in attrs:
        if attr.startswith('__') and attr.endswith('__'):
            continue
        try:
            dict_list.append((attr, getattr(ob, attr)))
        except Exception as e:
            dict_list.append((attr, 'Exception: {}'.format(e)))
    return dict(dict_list)

@register.filter
def pretty(ob, indent=0):
    if isinstance(ob, dict):
        d = ob
    else:
        d = to_dict(ob)
    od = collections.OrderedDict(sorted(d.items()))
    txt = ''
    t = '  ' * (indent+1)
    for key, value in od.items():
        txt = txt + t + str(key) + ": "
        if isinstance(value, dict):
            txt = txt + '{\n' + pretty(value, indent+1) + t + '}\n'
        elif value == None:
            txt = txt + '&lt;None&gt;' + ',\n'
        elif isinstance(value, bool):
            if value:
                txt = txt + 'True,\n'
            else:
                txt = txt + 'False,\n'
        else:
            txt = txt + repr(value).replace('<', '&lt;').replace('>', '&gt;') + ',\n'
    return mark_safe(txt)

@register.filter
def dir_list(obj):
    return str(obj.__class__) + "\n" + str(dir(obj))

@register.filter
def value(string, value):
    return string.format(value)
