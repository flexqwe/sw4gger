import secrets
import time

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from .models import EmailCode

CODE_TTL = 300        # 5 daqiqa
MAX_ATTEMPTS = 5


def send_code(email):
    code = f"{secrets.randbelow(1000000):06d}"
    cache.set(
        f"verify:{email}",
        {"code": code, "attempts": 0, "expires": time.time() + CODE_TTL},
        CODE_TTL,          # muddati tugagach Redis o'zi o'chiradi
    )
    send_mail("Tasdiqlash kodi", f"Kodingiz: {code}",
              settings.DEFAULT_FROM_EMAIL, [email])


def check_code(email, code):
    data = cache.get(f"verify:{email}")
    if data is None:
        return "expired"
    if data["attempts"] >= MAX_ATTEMPTS:
        return "blocked"
    if data["code"] != code:
        data["attempts"] += 1
        cache.set(f"verify:{email}", data, int(data["expires"] - time.time()))
        return "wrong"
    cache.delete(f"verify:{email}")
    return "ok"




def send_verification_code(user):
    code = f"{secrets.randbelow(1000000):06d}"

    EmailCode.objects.filter(user=user).delete()
    EmailCode.objects.create(user=user, code=code)

    send_mail(
        subject="Tasdiqlash kodi",
        message=f"Tasdiqlash kodingiz: {code}\nKod 5 daqiqa amal qiladi.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )