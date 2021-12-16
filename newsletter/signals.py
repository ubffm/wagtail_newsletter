
from django.core.mail import get_connection, EmailMultiAlternatives
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from .models import Subscriber, Newsletter

from wagtail.core.signals import page_published


def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), sends
    each message to each recipient list. Returns the number of emails sent.
    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.
    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    messages = []

    for subject, message, html_message, sender, recipient in datatuple:
        msg = EmailMultiAlternatives(subject, message, sender, recipient, connection=connection)
        msg.attach_alternative(html_message, "text/html")
        messages.append(msg)
    return connection.send_messages(messages)


@receiver(page_published, sender=Newsletter, dispatch_uid="newsletter.signals.newsletter_notification")
def newsletter_notification(sender, **kwargs):

    page_instance = kwargs['instance']
    if page_instance.alias_of_id is None:

        if page_instance.notify_subscribers is True:

            subscribers = Subscriber.objects.all().filter(validated=True)

            subject = 'New newsletter from YOUR ORGANIZATION'
            message = strip_tags(page_instance.email_text)
            # html_message = page_instance.email_text
            html_message = render_to_string('newsletter/email_template.html', {'email_content': page_instance.email_text})
            from_email = page_instance.get_parent().subscription_from_email

            emaildata = ()
            for subs in subscribers:
                emaildata = emaildata + ((subject, message, html_message, from_email, [subs.email]),)

            send_mass_mail(datatuple=tuple(emaildata))

            page_instance.notify_subscribers = False
            page_instance.save()
