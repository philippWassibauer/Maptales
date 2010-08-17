from django.core.management.base import NoArgsCommand
from brabeion import badges
from django.contrib.auth.models import User
import re

class Command(NoArgsCommand):
    help = "Veteran Badge"
    
    def handle_noargs(self, **options):
        for user in User.objects.all():
            p = re.compile( '([^a-zA-Z_0-9])')
            oldname = user.username
            user.username = p.sub("_", oldname)
            user.save()
            if oldname != user.username:
                print "Replaced username: %s with username: %s"%(oldname,user.username)
            

        