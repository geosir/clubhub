from django.db import models
from django.utils.html import escape
from django.contrib.auth.models import User
from os import urandom
from os.path import join
from binascii import hexlify
import datetime


# Generate a 16-byte hex UUID
def generate_uuid():
    return hexlify(urandom(16)).decode()


# Generate upload paths for posters
def get_upload_path(instance, filename):
    hash = generate_uuid()
    return join('posters/{}/{}/{}'.format(datetime.date.today().year,
                                          datetime.date.today().month,
                                          datetime.date.today().day), hash)


# A model to record Hub Groups
# Hub Groups are categories posters are labeled with, which
# determine how and where the poster is displayed on Club Hub
# and Club Hub LIVE.
class HubGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Hub Group Name", primary_key=True)
    description = models.TextField(verbose_name="Hub Group Description")
    active = models.BooleanField(default=False, verbose_name="Active?")
    internal = models.BooleanField(default=False, verbose_name="Campus-internal?")

    def __str__(self):
        return self.name


# A method to get the 'universal' Hub Group
def get_universal_group():
    return HubGroup.objects.filter(name='universal').first()


# A model to record Locations
# Locations are used by the Event model to geographically label events.
# They are stored in a model for ease-of-editing.
class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Location Name")
    description = models.TextField(verbose_name="Location Description")
    active = models.BooleanField(default=False, verbose_name="Active?")

    def __str__(self):
        return self.name


# A model to record Events
# This is the heart-and-soul of Club Hub!
class Event(models.Model):
    event_name = models.CharField(max_length=200, verbose_name="Event Name")
    event_host = models.CharField(max_length=100, verbose_name="Event Host")
    host_email = models.EmailField(verbose_name="Contact Email")
    event_body = models.TextField(verbose_name="Event Description")
    event_start_datetime = models.DateTimeField(verbose_name="Event Start Date/Time")
    event_end_datetime = models.DateTimeField(verbose_name="Event End Date/Time",
                                              help_text="Must be the same or later than the Start Date/Time.")
    event_location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    event_specific_location = models.CharField(blank=True, max_length=100, verbose_name="Specific Location")
    external_link = models.URLField(blank=True, verbose_name="External Link",
                                    help_text="a link to a Facebook page, etc.")
    rsvp_link = models.URLField(blank=True, verbose_name="RSVP Link")
    hub_group = models.ManyToManyField(
        'main.HubGroup',
        blank=True,
        default=get_universal_group,
        verbose_name="Hub Group")
    display_fullscreen = models.BooleanField(default=False, verbose_name="Display poster fullscreen on Club Hub LIVE")
    display_no_slideshow = models.BooleanField(default=False, verbose_name="Don't show on Club Hub LIVE")
    poster_file = models.ImageField(blank=True, null=True, verbose_name="Poster File", upload_to=get_upload_path)
    slide_duration = models.IntegerField(default=20000, verbose_name="Slide Duration",
                                         help_text="Duration of slide on Club Hub LIVE in milleseconds.")
    hide_from_registry = models.BooleanField(default=False, verbose_name="Don't show in the event listing.")
    approved = models.BooleanField(default=False, verbose_name="Event approved?")
    owners = models.ManyToManyField(User, blank=True, verbose_name="Event Owners")
    internal = models.BooleanField(default=False, verbose_name="Campus-internal?")

    # Return a string representation of the event, used by the admin interface.
    def __str__(self):
        return '"{}" by {}'.format(self.event_name, self.event_host)

    # Generate a poster preview tag, for the admin interface.
    def poster_preview(self):
        if self.poster_file:
            return '<img class="gallerize" src="{}" style="width: 100px" /></a>'.format(
                self.poster_file.url, self.poster_file.url)
        else:
            return "None"

    poster_preview.short_description = 'Poster Preview'
    poster_preview.allow_tags = True

    # Body preview for the admin interface.
    def body_preview(self):
        preview = self.event_body[0:300]
        if len(self.event_body) > 300:
            preview += "..."
        return escape(preview)

    body_preview.short_description = 'Event Description'
    body_preview.allow_tags = True

    @classmethod
    def get_approved(cls):
        return cls.objects.filter(approved=True)


# Model to record Settings.
# Settings are dynamic variables used throughout the
# upper-level Club Hub application.(They are "upper-level" in contrast
# to "lower-level" Django internal settings, like in settings.py.)
# More info on the available key/value pairs for Settings
# can be found in the README.
class Setting(models.Model):
    key = models.CharField(max_length=100, verbose_name="Setting Key")
    value = models.CharField(max_length=100, verbose_name="Setting Value")

    def __str__(self):
        return "Setting: {}={}".format(self.key, self.value)
