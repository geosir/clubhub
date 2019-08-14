from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Event, Setting, HubGroup, get_universal_group
from .forms import SubmitEvent, SignUp
from .emails import make_event_email
from .utils import unsafeHTMLFromDelta, account_activation_token
from urllib.parse import quote
import hashlib
import datetime
import pytz


# The Main View
def index(request, hub_group):
    # If a Hub Group is specified, check that it exists
    # and check that the user is authorized to view events in the group.
    if hub_group:
        hub_group = HubGroup.objects.filter(name=hub_group).first()
        if hub_group:
            if hub_group.internal and not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login') + "?next=" + request.path)
        else:
            raise Http404

    CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
    CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None

    # Filter posters based on date and user privilege.
    if hub_group:
        posters = Event.get_approved().filter(
            event_end_datetime__gt=timezone.now(),
            hide_from_registry=False,
            internal__in=[False, request.user.is_authenticated],
            hub_group__in=[hub_group]
        ).order_by(
            'event_start_datetime')
    else:
        posters = Event.get_approved().filter(
            event_end_datetime__gt=timezone.now(),
            hide_from_registry=False,
            internal__in=[False, request.user.is_authenticated],
            hub_group__in=[get_universal_group()]
        ).order_by(
            'event_start_datetime')

    # Add additional metadata to the posters
    for poster in posters:
        # Generate a Google Calendar location string.
        if poster.event_specific_location:
            location = "{} | {}".format(poster.event_location, poster.event_specific_location)
        else:
            location = poster.event_location

        # Generate an Add To Google Calendar link.
        poster.gcal_link = ("http://www.google.com/calendar/event"
                            "?action=TEMPLATE&text={}&dates={}/{}"
                            "&details={}&location={}&trp=false"
                            "&sprop=&sprop=name:") \
            .format(poster.event_name,
                    poster.event_start_datetime.astimezone(pytz.utc).strftime("%Y%m%dT%H%M00Z"),
                    poster.event_end_datetime.astimezone(pytz.utc).strftime("%Y%m%dT%H%M00Z"),
                    quote(poster.event_body),
                    location)

        # Generate a UUID for the poster. Used for linking directly to the poster.
        poster.uuid = hashlib.md5((poster.event_start_datetime.astimezone(pytz.utc).strftime("%Y%m%d") + " " +
                                   poster.event_name + " " +
                                   poster.event_host).encode('UTF-8')).hexdigest()

        poster.link = request.scheme + "://" + request.get_host() + "/#" + poster.uuid

    # The 'parties' group gets special CSS. Check if the user is viewing the 'parties' Hub Group
    is_party = (hub_group and hub_group.name.lower() == 'parties')

    return render(request, 'main/index.html',
                  {'posters': posters, 'CLUBHUB_CONTACT_EMAIL': CLUBHUB_CONTACT_EMAIL, 'is_party': is_party})


# Update the user's timezone based on
# their selection from the timezone spinner.
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('index')


# The Slideshow View
def present(request, hub_group):
    # If a Hub Group has been specified,
    # Check that the Hub Group exists and that
    # the user is authorized to view events in the group.
    if hub_group:
        hub_group = HubGroup.objects.filter(name=hub_group).first()
        if hub_group:
            if hub_group.internal and not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login') + "?next=" + request.path)
        else:
            raise Http404

        # Filter events based on time and user privilege.
        posters = Event.get_approved().filter(event_end_datetime__gt=timezone.now(),
                                              hub_group__in=[hub_group],
                                              internal__in=[False, request.user.is_authenticated],
                                              display_no_slideshow=False).order_by(
            'event_start_datetime')
    else:
        # Filter events based on time and user privilege.
        posters = Event.get_approved().filter(event_end_datetime__gt=timezone.now(),
                                              hub_group__in=[get_universal_group()],
                                              internal__in=[False, request.user.is_authenticated],
                                              display_no_slideshow=False).order_by(
            'event_start_datetime')

    return render(request, 'present/index.html', {'posters': posters})


# A view that generates a single-slide preview based on query parameters.
def slide_factory(request):
    params = request.GET
    poster = {
        'poster_file': {'url': params.get('poster')} if params.get('poster') else False,
        'display_fullscreen': (params.get('fullscreen') == 'true'),
        'event_name': params.get('name'),
        'event_host': params.get('host'),
        'event_start_datetime': datetime.datetime.strptime(params.get('start'), "%Y-%m-%d %H:%M") if params.get(
            'start') else None,
        'event_end_datetime': datetime.datetime.strptime(params.get('end'), "%Y-%m-%d %H:%M") if params.get(
            'end') else None,
        'event_location': params.get('location'),
        'event_specific_location': params.get('specific_location'),
        'event_body': params.get('body'),
    }

    return render(request, 'factory/slides.html', {'posters': [poster]})


# The Event Submission View
def submit(request):
    if request.method == 'POST':
        form = SubmitEvent(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()

            # Attach owner to event, if user is logged in.
            if request.user.is_authenticated:
                event.owners.add(request.user)

            # Process Delta RTF object in event body
            event.event_body = unsafeHTMLFromDelta(form.cleaned_data['event_body'])

            event.save()

            # Generate emails to Approvers and Submitter
            approvers = User.objects.filter(groups__name='Approvers').values_list('email', flat=True)
            approver_message = make_event_email('mail/approver.html', event, request)
            approver_subject = "[Club Hub] New Event Registration"
            submitter_message = make_event_email('mail/submitter.html', event, request)
            submitter_subject = "[Club Hub] Registration Confirmation"

            CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
            CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None

            # Send email to approvers
            if len(approvers) > 0:
                mail = EmailMessage(approver_subject, approver_message, settings.EMAIL_HOST_USER, approvers,
                                    reply_to=[CLUBHUB_CONTACT_EMAIL])
                mail.content_subtype = 'html'
                mail.send()

            # Send email to submitter
            mail = EmailMessage(submitter_subject, submitter_message, settings.EMAIL_HOST_USER, [event.host_email],
                                reply_to=[CLUBHUB_CONTACT_EMAIL])
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'submit/success.html')
        else:
            return render(request, 'submit/submit.html', {'form': form, 'messages': 'Something went wrong!'})

    else:
        form = SubmitEvent()
        return render(request, 'submit/submit.html', {'form': form})


# A view that directs users to the Club Hub info page.
def about(request):
    return HttpResponseRedirect("https://clubhub.live")


# The Login View
def user_login(request, **kwargs):
    # Hide login from logged in users
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return auth_views.login(request, **kwargs)


# The Logout View
def logout(request, **kwargs):
    # Hide logout from logged out users
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        return auth_views.logout(request, **kwargs)


# The Account Sign Up View
def signup(request):
    if request.user.is_authenticated:
        # Don't let logged-in users sign up
        return redirect('index')
    if request.POST:
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
            CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None

            # Send email confirmation email
            subject = '[Club Hub] Confirm Your Email Address'
            message = render_to_string('mail/confirm_email.html', {
                'user': user,
                'CLUBHUB_CONTACT_EMAIL': CLUBHUB_CONTACT_EMAIL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'request': request
            })

            mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email],
                                reply_to=[CLUBHUB_CONTACT_EMAIL])
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'registration/email_confirm_sent.html')
        else:
            return render(request, 'registration/signup.html', {'form': form, 'messages': 'Something went wrong!'})

    else:
        form = SignUp()
        return render(request, 'registration/signup.html', {'form': form})


# The Account Sign Up Confirmation Email Checker View
def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check the user's token and activate if successful.
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/email_confirm_success.html')
    else:
        # Show a failure message.
        CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
        CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None
        return render(request, 'registration/token_confirm_failed.html',
                      {'CLUBHUB_CONTACT_EMAIL': CLUBHUB_CONTACT_EMAIL})


# The Password Reset View
def password_reset(request, **kwargs):
    if request.method == 'POST':
        # Mark session
        request.session['used_reset_form'] = True
    return auth_views.password_reset(request, **kwargs)


# The Password Reset "Email Sent" View
def password_reset_done(request, **kwargs):
    # Hide message from undefined paths
    if not request.session.pop('used_reset_form', False):
        return redirect('index')
    else:
        return auth_views.password_reset_done(request, **kwargs)


# The Password Change View
def password_reset_confirm(request, **kwargs):
    if request.method == 'POST':
        # Mark session
        request.session['used_change_form'] = True
    return auth_views.password_reset_confirm(request, **kwargs)


# The Password Change "Complete Message" View
def password_reset_complete(request, **kwargs):
    # Hide message from undefined paths
    if not request.session.pop('used_change_form', False):
        return redirect('index')
    else:
        return auth_views.password_reset_complete(request, **kwargs)


# The 404 View
def error404(request):
    return render(request, 'main/404.html', status=404)
