import random

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError

ERROR = "Kod topilmadi, muddati tugagan yoki urinishlar tugagan"
NOT_CONFIRMED = "Avval kodni tasdiqlang yoki kod muddati tugagan"


def send_verification_code(user):
    code = str(random.randint(100000, 999999))
    data = {"code": code, "tries": 0}
    key = f"verify:{user.id}"

    cache.set(key, data, 300)
    print(f"DEBUG send - user.id: {user.id}, key: {key}, code: {code}")

    send_mail(
        "Tasdiqlash kodi",
        f"Kodingiz: {code}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def confirm_code(user, code):
    key = f"verify:{user.id}"
    data = cache.get(key)
    print(f"DEBUG confirm - user.id: {user.id}, key: {key}, data: {data}")

    if data is None or data["tries"] >= 5:
        raise ValidationError({"detail": ERROR})

    if data["code"] != code:
        data["tries"] += 1
        cache.set(key, data, 300)
        raise ValidationError({"detail": "Kod noto'g'ri"})

    data["confirmed"] = True
    cache.set(key, data, 300)


def finish_code(user):
    key = f"verify:{user.id}"
    data = cache.get(key)
    if data is None or not data.get("confirmed"):
        raise ValidationError({"detail": NOT_CONFIRMED})

    cache.delete(key)