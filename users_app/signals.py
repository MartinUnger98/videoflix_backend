from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.dispatch import Signal

password_reset_requested = Signal()

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

        subject = "Activate your Videoflix account"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email

        html_content = render_to_string("users_app/email_verification.html", {
            "username": instance.username,
            "activation_link": activation_link,
            "logo_url": "https://martin-unger.at/images/Capa_1.png"
        })

        email = EmailMultiAlternatives(subject, "", from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()
        
@receiver(password_reset_requested)
def send_password_reset_email(sender, user, **kwargs):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"

    subject = "Reset your Videoflix password"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    html_content = render_to_string("users_app/password_reset_email.html", {
        "reset_link": reset_link,
        "logo_url": "https://martin-unger.at/images/Capa_1.png"
    })

    email = EmailMultiAlternatives(subject, "", from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
