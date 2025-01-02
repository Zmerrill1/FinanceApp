import locale
from decimal import Decimal

from django import template

register = template.Library()

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


@register.filter
def usd(value):
    """Formats a number as USD"""
    try:
        value = Decimal(value)
    except (ValueError, TypeError, locale.Error):
        return locale.currency(value, grouping=True)
