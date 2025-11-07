from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def readable_number(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    if value < 1000:
        return f"{int(value)}"  # setki, dziesiątki
    elif value < 100_000:
        # tysiące z separatorem
        return f"{int(value):,}".replace(",", " ")
    elif value < 1_000_000:
        # setki tysięcy → 100K
        return f"{int(value/1000)}K"
    elif value < 1_000_000_000:
        # miliony → 1.4M
        return f"{value/1_000_000:.1f}M"
    else:
        # miliardy → 1.4B
        return f"{value/1_000_000_000:.1f}B"

@register.filter
def readable_data(value):
    """
    Formatuje liczby z separatorami tysięcy jako spacja.
    Obsługuje Decimal, float i string.
    """
    try:
        # konwersja Decimal na float
        if isinstance(value, Decimal):
            value = float(value)
        else:
            value = float(str(value).replace(" ", "").replace(",", "."))
    except (ValueError, TypeError):
        return value

    # liczba całkowita
    if value.is_integer():
        return f"{int(value):,}".replace(",", " ")
    else:
        # liczba zmiennoprzecinkowa z dwoma miejscami po przecinku
        return f"{value:,.2f}".replace(",", " ")

