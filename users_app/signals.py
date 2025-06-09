from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
import os

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

        subject = "Activate your Videoflix account"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = instance.email

        html_content = f"""
        <div style="text-align: center;">
            <img src="cid:logo" alt="Videoflix Logo" style="width:150px;" />
            <p>Dear {instance.username},<br><br>
            Thank you for registering with Videoflix. To complete your registration and verify your email address, please click the link below:</p>
            <a href="{activation_link}" style="background-color:#ff3333;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin:20px 0;">Activate Account</a>
            <p>If you did not create an account with us, please disregard this email.<br><br>
            Best regards,<br>Your Videoflix Team.</p>
        </div>
        """

        email = EmailMultiAlternatives(subject, "", from_email, [to_email])
        email.attach_alternative(html_content, "text/html")

        # Optional: Bild inline anhängen
        image_path = os.path.join(settings.BASE_DIR, 'static', 'Capa_1.svg')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                email.attach_inline('logo', img.read(), 'image/svg+xml')

        email.send()
