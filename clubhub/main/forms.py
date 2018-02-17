from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Setting
import re


# The event submission form at '/submit'
class SubmitEvent(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Event
        fields = ('event_name', 'event_host', 'host_email', 'event_body', 'event_start_datetime', 'event_end_datetime',
                  'event_location', 'event_specific_location', 'external_link', 'rsvp_link', 'poster_file',
                  'internal', 'hub_group', 'display_fullscreen', 'display_no_slideshow')

    # Ensure that end-times are not earlier than start-times.
    def clean_event_end_datetime(self):
        start = self.cleaned_data.get('event_start_datetime')
        end = self.cleaned_data.get('event_end_datetime')
        if not start or not end:
            raise forms.ValidationError("Missing Date/Times.")
        elif end < start:
            raise forms.ValidationError("End Date/Time cannot be earlier than Start Date/Time.")
        return end


# Dynamically retrieve allowed email suffixes from the database.
def get_email_suffixes():
    EMAIL_SUFFIXES = Setting.objects.filter(key='ALLOWED_EMAIL_SUFFIX')
    return [suffix.value for suffix in EMAIL_SUFFIXES]


# Generate the email-field helptext for the sign-up form
# depending on whether there are limited allowed email suffixes.
def generate_email_helptext():
    EMAIL_SUFFIXES = get_email_suffixes()
    if len(EMAIL_SUFFIXES) > 0:
        return "Must have one of these suffixes: <ul>{}</ul>".format(
            "".join(["<li>" + suffix + "</li>" for suffix in EMAIL_SUFFIXES]))
    else:
        return None


# The user sign-up form at '/signup'
class SignUp(UserCreationForm):
    required_css_class = 'required'
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=256, help_text=generate_email_helptext)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    # Ensure that the email contains an allowed suffix.
    def clean_email(self):
        EMAIL_SUFFIXES = get_email_suffixes()
        email = self.cleaned_data.get('email')
        if len(EMAIL_SUFFIXES) > 0:
            if re.search(r'(' + "|".join(EMAIL_SUFFIXES) + ')$', email) == None:
                raise forms.ValidationError("Not an allowed email suffix.")
        return email
