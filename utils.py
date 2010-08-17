import os 
import datetime
from django.conf import settings

def get_image_path(instance, filename):
    today = datetime.date.today()
    dirname = today.strftime("%Y/%m/%d")
    if not os.path.isdir(settings.MEDIA_ROOT + "/photologue/" + dirname + "/"):
        os.makedirs(settings.MEDIA_ROOT + "/photologue/" + dirname + "/")
    finaldir = "photologue/" + dirname
    return os.path.join(finaldir, filename) 



