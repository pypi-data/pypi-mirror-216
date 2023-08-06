from django.contrib.auth.models import User

from django.db import models

class CookieConsentAcceptance(models.Model):
    user = models.OneToOneField(
        User, models.CASCADE,
        related_name='cookie_consent'
    )

    def __str__(self) -> str:
        return f'cookie consent obj for user "{self.user.username}"'
