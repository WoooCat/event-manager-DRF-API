from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registration


@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance: Registration, created: bool, **kwargs):
    if not created:
        return

    user = instance.user
    event = instance.event

    subject = f"Registration confirmed: {event.title}"
    message = (
        f"Hi {user.first_name or user.username},\n\n"
        f"You have successfully registered for '{event.title}'.\n"
        f"When: {event.date}\n"
        f"Where: {event.location}\n\n"
        f"Organizer: {event.organizer.username}\n\n"
        f"Thank you!"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[user.email] if user.email else [],
        fail_silently=True,  # for demo/test
    )
