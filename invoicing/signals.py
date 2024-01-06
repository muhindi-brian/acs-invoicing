# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to YourSite'
        message = render_to_string('welcome_email_template.html', {'user': instance})
        instance.email_user(subject, message, from_email='your@example.com')
