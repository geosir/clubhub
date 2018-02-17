from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import pytz


# Middleware that corrects datetimes for the user's timezone.
class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
