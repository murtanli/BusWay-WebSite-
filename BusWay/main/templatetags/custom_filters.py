from django import template
import locale

register = template.Library()

@register.filter(name='spacecomma')
def spacecomma(value):
    """
    Фильтр для добавления пробелов в числовое значение.
    Например, 2490 станет 2 490.
    """
    try:
        # Устанавливаем локаль
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        # Преобразуем числовое значение в строку с добавлением разделителей тысяч
        return locale.format_string("%d", value, grouping=True)
    except (ValueError, TypeError):
        return value

