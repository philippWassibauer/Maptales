from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from photos.models import Image
import os
from django.core.files.base import ContentFile

def iphone_post(request):
    import base64
    data = base64.b64decode(request.POST.get("imageData"))
    image = Image()
    image.member = User.objects.get(username="admin")
    image.image.save(os.path.basename("IphoneUpload.jpg"), ContentFile(data))
    image.save()
    # now rotate it according to exif data
    try:
        image.rotate_to_exif()
    except:
        pass
    return HttpResponse(status=200, content="sdf")

