"""Templatetags for the active_users app."""
from django import template

register = template.Library()

# @register.filter
# def lower(value):
#     """
#     Converts a string into all lowercase
#
#     """
#     return value.lower()
