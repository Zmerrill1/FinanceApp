import locale
from decimal import Decimal

from django import template

register = template.Library()

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


@register.filter
def usd(value):
    """Formats a number as USD"""
    try:
        if isinstance(value, Decimal):
            value = float(value)
            return locale.currency(value, grouping=True)
    except (ValueError, TypeError):
        return "$0.00"
