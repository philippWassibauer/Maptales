from django.core.management.base import NoArgsCommand
from brabeion import badges
from django.contrib.auth.models import User

class Command(NoArgsCommand):
    help = "Veteran Badge"
    
    def handle_noargs(self, **options):
        for user in User.objects.all():
            badges.possibly_award_badge("existing_account", user=user)