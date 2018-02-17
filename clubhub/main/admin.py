from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin
from django.core.mail import EmailMessage
import clubhub.settings as settings
from .models import Event, Setting, HubGroup, Location
from .emails import make_event_email


# ========== Register Actions ==========
# Mark an event as approved.
def approve_event(modeladmin, request, queryset):
    queryset.update(approved=True)


approve_event.short_description = "Approve selected events"


# Mark an event as approved and notify its contact.
def approve_and_notify_event(modeladmin, request, queryset):
    approve_event(modeladmin, request, queryset)

    CLUBHUB_CONTACT_EMAIL = Setting.objects.filter(key='CLUBHUB_CONTACT_EMAIL').first()
    CLUBHUB_CONTACT_EMAIL = CLUBHUB_CONTACT_EMAIL.value if CLUBHUB_CONTACT_EMAIL else None

    for event in queryset:
        submitter_message = make_event_email('mail/event_approved.html', event, request)
        submitter_subject = "[Club Hub] Event Approved"

        mail = EmailMessage(submitter_subject, submitter_message, settings.EMAIL_HOST_USER, [event.host_email],
                            reply_to=[CLUBHUB_CONTACT_EMAIL])
        mail.content_subtype = 'html'
        mail.send()


approve_and_notify_event.short_description = "Approve and notify contacts"


# Unmark an event as approved.
def disapprove_event(modeladmin, request, queryset):
    queryset.update(approved=False)


disapprove_event.short_description = "Disapprove selected events"


# Mark an event as campus-internal
def internalize_event(modeladmin, request, queryset):
    queryset.update(internal=True)


internalize_event.short_description = "Make selected events internal"


# Unmark an event as campus-internal
def publicize_event(modeladmin, request, queryset):
    queryset.update(internal=False)


publicize_event.short_description = "Make selected events public"


# ========== Register Models ==========
# A view for editing events in the admin panel.
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_host', 'body_preview', 'event_location', 'event_start_datetime',
                    'poster_preview', 'internal', 'approved']
    ordering = ['approved', '-event_start_datetime']
    editor_fields = (
        'event_name', 'event_host', 'host_email', 'event_body', 'event_start_datetime', 'event_end_datetime',
        'event_location', 'event_specific_location', 'external_link', 'rsvp_link', 'poster_file', 'poster_preview',
        'internal', 'hub_group', 'display_fullscreen', 'display_no_slideshow',
        'owners')
    approver_fields = (
        'slide_duration', 'approved', 'hide_from_registry')
    superuser_fields = ()
    readonly_fields = ('poster_preview',)
    search_fields = ['event_name', 'event_host', 'event_body']

    actions = [disapprove_event, approve_event, approve_and_notify_event, publicize_event, internalize_event]

    def get_actions(self, request):
        actions = super(EventAdmin, self).get_actions(request)
        if request.user.is_superuser or \
                request.user.groups.filter(name='Approvers').exists():
            return actions
        else:
            for action in ['disapprove_event', 'approve_event', 'approve_and_notify_event', 'publicize_event',
                           'internalize_event']:
                if action in actions:
                    del actions[action]
            return actions

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.editor_fields + self.approver_fields + self.superuser_fields
        elif request.user.groups.filter(name='Approvers').exists():
            self.fields = self.editor_fields + self.approver_fields
        elif request.user.groups.filter(name='Editors').exists():
            self.fields = self.editor_fields
        else:
            self.fields = []

        return super(EventAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        # Record event creators as owners
        if not change:
            obj.save()
            obj.owners.add(request.user)
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser or \
                request.user.groups.filter(name='Approvers').exists():
            return super(EventAdmin, self).get_queryset(request)
        else:
            return super(EventAdmin, self).get_queryset(request).filter(owners__in=[request.user], approved=False)


admin.site.register(Event, EventAdmin)


# A view for editing Hub Groups in the admin panel.
class HubGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'active']
    ordering = ['name']


admin.site.register(HubGroup, HubGroupAdmin)


# A view for editing Locations in the admin panel.
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'active']
    ordering = ['name']


admin.site.register(Location, LocationAdmin)


# A view for editing Settings in the admin panel.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    ordering = ['key']


admin.site.register(Setting, SettingAdmin)


# A customized view for editing Users in the admin panel.
# Customized to be able to see 'is_active' in the list view.
class ClubHubUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, ClubHubUserAdmin)
