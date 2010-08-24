from django.core.management.base import NoArgsCommand
from brabeion import badges
from django.contrib.auth.models import User
from emailconfirmation.models import EmailAddress
import re

class Command(NoArgsCommand):
    help = "Veteran Badge"
    
    def handle_noargs(self, **options):
        for user in User.objects.all():
            try:
                email = EmailAddress.objects.get(
                            user=user,
                            email=user.email
                        )
                if email and email.verified != True:
                    print "setting email of user: %s to verified"%user
                    email.verified = True
                    email.save()
                else:
                    print "Nothing to do"
            except:
                print "verifiying users email: %s"%user
                EmailAddress.objects.create(
                        user=user,
                        email=user.email,
                        verified=True,
                        primary=True
                    )
            

        