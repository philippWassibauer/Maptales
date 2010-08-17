from django.template import Library
from django.core import urlresolvers
from native_tags.decorators import function, comparison, filter

register = Library()

import datetime
import time


def admin_url(app, model, action, id=None):
    try:
        if(id):
            return urlresolvers.reverse('admin:%s_%s_%s'%(app, model, action), args=(id,))
        else:
            return urlresolvers.reverse('admin:%s_%s_%s'%(app, model, action))
    except:
        return "";

admin_url = function(admin_url)

def main_admin_url():
    try:
        return urlresolvers.reverse('admin:index')
    except:
        return "";
main_admin_url = function(main_admin_url)