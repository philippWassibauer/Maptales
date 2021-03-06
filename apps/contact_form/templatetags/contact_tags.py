from django import template
from contact_form.forms import ContactForm

register = template.Library()

def show_contact_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("contact_form.html")(show_contact_form)

def show_feedback_form():
    return {"contact_form": ContactForm()}
register.inclusion_tag("feedback_form.html")(show_feedback_form)
