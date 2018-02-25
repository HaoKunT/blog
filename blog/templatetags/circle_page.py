from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def circle_page(current_page, compare_page):
    offset = abs(current_page-compare_page)

    if offset < 4:
        if current_page == compare_page:
            page_html = """<li><a href="/blog/home/{}" class="pure-button:active">{}</a></li>""".format(compare_page,compare_page)
        else:
            page_html = """<li><a href="/blog/home/{}" class="pure-button">{}</a></li>""".format(compare_page,compare_page)
        return format_html(page_html)
    else:
        return ''

