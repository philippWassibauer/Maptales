from featured.models import FeaturedItem
from featured.forms import FeaturedItemForm

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def list(request, user=None):
    """
    renders a list of featured items grouped by model
    """
    if user is None:
        user = request.user
    list_of_content_types = FeaturedItem.objects.content_types_of_featured_items(user)
    
    dict_of_featured_items = {}
    for content_type in list_of_content_types:
        dict_of_featured_items[content_type] = FeaturedItem.objects.filter(content_type=content_type)
        
    return render_to_response('list.html', { 'dict_of_featured_items': dict_of_featured_items }, context_instance=RequestContext(request))

@login_required
def add_or_edit(request, content_type_id, content_object_id):
    """
    mark object with content_object_id of some model (identified by content_type_id) as featured
    """

    target_object = get_target_object(content_type_id, content_object_id)
    # try to fetch already existing object
    try:
        featured_object = FeaturedItem.objects.get(object_id=target_object.id, content_type=content_type_id, user=request.user)
    except FeaturedItem.DoesNotExist:
        featured_object = None

    if featured_object is None:
        featured_object = FeaturedItem(content_object=target_object, title='', body='', user=request.user)
        
    if request.method == 'POST':
        # update featured_object from post data
        form = FeaturedItemForm(request.POST, request.FILES, instance=featured_object)

        if form.is_valid():
            featured_object = form.save()
            return HttpResponseRedirect(target_object.get_absolute_url())
    else:
        # update featured_object from post data
        form = FeaturedItemForm(request.GET, request.FILES, instance=featured_object)
        
        if request.REQUEST.has_key('predefined') and form.is_valid():
            featured_object = form.save()
            return HttpResponseRedirect(target_object.get_absolute_url())

    return render_to_response("featured_item_form.html", { "form": form }, context_instance=RequestContext(request))

@login_required
def remove(request, content_type_id, content_object_id):
    """
    remove object from featured list
    """
    target_object = get_target_object(content_type_id, content_object_id)
    featured_object = FeaturedItem.objects.filter(object_id=target_object.id, content_type=content_type_id, user=request.user)
    featured_object.delete()

    if request.META.has_key('HTTP_REFERER'):
        referer = request.META['HTTP_REFERER']
        return HttpResponseRedirect(referer)
    else:
        return HttpResponseRedirect('/')

def get_target_object(content_type_id, content_object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    # get object of type "content_type_id" with given content_object_id
    target_object = content_type.get_object_for_this_type (pk=content_object_id)
    return target_object