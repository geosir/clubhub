from django.utils.html import escape
from django.template.loader import render_to_string
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .templatetags.sanitize import sanitize
from .models import Setting
import traceback


# Make an mail using with event data loaded into the context.
def make_event_email(template, event, request):
    CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
    CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None

    context = {
        'CLUBHUB_CONTACT_EMAIL': CLUBHUB_CONTACT_EMAIL,
        'event_host': escape(event.event_host),
        'event_name': escape(event.event_name),
        'host_email': escape(event.host_email),
        'event_start': escape(event.event_start_datetime.strftime("%c %Z")),
        'event_end': escape(event.event_end_datetime.strftime("%c %Z")),
        'event_body': sanitize(event.event_body),
        'event_location': ((escape(event.event_location) + " (" + escape(event.event_specific_location) + ")")
        if event.event_specific_location
        else escape(event.event_location)),
        'event_poster_image': (
                '<img class="poster" src="' + request.scheme + "://" + request.get_host() + settings.MEDIA_URL + str(
            event.poster_file) + '">')
        if event.poster_file else 'No poster.',
        'event_poster': "Yes" if event.poster_file else "No",
        'event_hub_groups': ", ".join([str(group) for group in event.hub_group.all()]),
        'display_slideshow': "Yes" if not event.display_no_slideshow else "No",
        'display_fullscreen': "Yes" if event.display_fullscreen else "No",
        'request': request
    }

    return render_to_string(template, context=context)


# Generate a SendGrid POST request with the given email parts.
def make_sendgrid_data(to_emails, from_email, subject, message, reply_to=None):
    message = Mail(from_email=from_email,
                   to_emails=to_emails,
                   subject=subject,
                   html_content=message)

    if reply_to is not None and \
            (type(reply_to) is list or type(reply_to) is tuple) and \
            len(reply_to) > 0 and type(reply_to[0]) is str:
        # Only one reply_to is supported in SendGrid API V3
        message.reply_to = reply_to[0]

    return message


# A custom Django email backend that uses SendGrid
class SendGridBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        self.sg = SendGridAPIClient(settings.SENDGRID_APIKEY)
        super().__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        successful = 0
        for email in email_messages:
            message = make_sendgrid_data(
                email.to,
                email.from_email,
                email.subject,
                email.body,
                reply_to=email.reply_to
            )
            try:
                self.sg.send(message)
                successful += 1
            except Exception:
                traceback.print_exc()
        return successful
