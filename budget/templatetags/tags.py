import locale
from decimal import Decimal

from django import template

register = template.Library()

try:
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")


@register.filter
def usd(value):
    """Formats a number as USD"""
    try:
        value = Decimal(value)
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError, locale.Error):
        return "$0.00"
