# -*- coding: utf-8 -*-

import re
from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('article_content.html')
def render_content(article, content_attr='content', markup_attr='markup'):
    return {
        'content': getattr(article, content_attr),
        'markup': getattr(article, markup_attr)
    }


@register.inclusion_tag('article_teaser.html')
def show_teaser(article):
    """ Show a teaser box for the summary of the article.
    """
    return {'article': article}


