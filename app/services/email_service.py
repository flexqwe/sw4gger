
import random

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.serializers import ValidationError

from app.models import EmailCode

ERROR = "Kod topilmadi, muddati tugagan yoki urinishlar tugagan"
NOT_CONFIRMED = "Avval kodni tasdiqlang yoki kod muddati tugagan"


def send_verification_code(user):
    code = str(random.randint(100000, 999999))

    EmailCode.objects.filter(user=user).delete()
    EmailCode.objects.create(
        user=user,
        code=code,
        attempts=0,
        is_confirmed=False,
    )

    send_mail(
        "Tasdiqlash kodi",
        f"Kodingiz: {code}\n5 daqiqa amal qiladi.",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def confirm_code(user, code):
    record = EmailCode.objects.filter(user=user).first()

    if not record or record.is_expired():
        raise ValidationError({"detail": ERROR})

    if record.attempts >= EmailCode.MAX_ATTEMPTS:
        raise ValidationError({"detail": ERROR})

    if record.code != code:
        record.attempts += 1
        record.save()
        raise ValidationError({"detail": "Kod noto'g'ri"})

    record.is_confirmed = True
    record.save()


def finish_code(user):
    record = EmailCode.objects.filter(
        user=user, is_confirmed=True
    ).first()

    if not record:
        raise ValidationError({"detail": NOT_CONFIRMED})

    record.delete()