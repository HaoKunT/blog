from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def circle_page(current_page, compare_page, mode, params=None):
    offset = abs(current_page-compare_page)


    if offset < 4:
        if current_page == compare_page:
            if mode == "home":
                page_html = """<li><a href="/blog/home/{}/" class="pure-button:active">{}</a></li>""".format(compare_page,compare_page)
            elif mode == "search":
                params_html = "/blog/{}/{}?".format(mode, compare_page)
                for key, item in params.items():
                    params_html += "{}={}&".format(key, item)
                page_html = """<li><a href="{}" class="pure-button:active">{}</a></li>""".format(params_html, compare_page)
            else:
                page_html = ''
        else:
            if mode == "home":
                page_html = """<li><a href="/blog/home/{}/" class="pure-button">{}</a></li>""".format(compare_page,compare_page)
            elif mode == "search":
                params_html = "/blog/{}/{}?".format(mode, compare_page)
                for key, item in params.items():
                    params_html += "{}={}&".format(key, item)
                page_html = """<li><a href="{}" class="pure-button">{}</a></li>""".format(params_html, compare_page)
            else:
                page_html = ''
        return format_html(page_html)
    else:
        return ''

