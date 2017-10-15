from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """subtracts arg from value"""
    return int(value) - int(arg)

@register.filter
def multiply(value, arg):
    """multiplies value and arg"""
    return int(value) * int(arg)
