from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import json


# Generate HTML with only approved tags from a Flatpickr DateTimePicker Delta.
# It is called UNSAFE because the text is not escaped
# Make sure to use this text with Django's safe text, or the sanitizer
def unsafeHTMLFromDelta(delta):
    delta = json.loads(delta)
    output = ""

    for i, op in enumerate(delta['ops']):
        if 'insert' in op:
            segment = op['insert']
            if 'attributes' in op:
                if 'italic' in op['attributes']:
                    segment = "<i>" + segment + "</i>"
                if 'underline' in op['attributes']:
                    segment = "<u>" + segment + "</u>"
                if 'bold' in op['attributes']:
                    segment = "<b>" + segment + "</b>"
                if 'strike' in op['attributes']:
                    segment = "<s>" + segment + "</s>"
                if 'link' in op['attributes']:
                    if not (i > 0
                            and 'attributes' in delta['ops'][i - 1]
                            and 'link' in delta['ops'][i - 1]['attributes']
                            and delta['ops'][i - 1]['attributes']['link'] == op['attributes']['link']):
                        segment = "<a href=\"" + op['attributes']['link'] + "\">" + segment
                    if not (i + 1 < len(delta['ops'])
                            and 'attributes' in delta['ops'][i + 1]
                            and 'link' in delta['ops'][i + 1]['attributes']
                            and delta['ops'][i + 1]['attributes']['link'] == op['attributes']['link']):
                        segment = segment + "</a>"
            output += segment

    return output


# Extends the Password Reset Token Generator
# to generate similar tokens for email confirmation.
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Why use six? Why not?
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
