from django import template
from audio.models import Audio

register = template.Library()

def show_smith_audioplayer(user):
    return {"audios": user.added_audios.all(), "user":user}
register.inclusion_tag("audioplayer.html")(show_smith_audioplayer)

def show_main_audioplayer():
    return {"audios": Audio.objects.all()}
register.inclusion_tag("audioplayer.html")(show_main_audioplayer)


def show_single_audioplayer(audio):
    return {"audios": [audio]}
register.inclusion_tag("audioplayer.html")(show_single_audioplayer)