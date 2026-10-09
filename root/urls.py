from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from app.views import (
    ProductListPublicView,
    ProductCreateView,
    ProductDeleteView,
    ProductListCreateView,
    RegisterView,
    VerifyEmailView,
    LogoutView,
    MeView,
    ResendCodeView,
)
from views import ForgotPasswordView, ConfirmPasswordView, ResetPasswordView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Root URL - redirect to Swagger UI
    path('', lambda request: HttpResponse('<h1></h1><p>Visit <a href="/swagger/">Swagger UI</a> </p>')),
    path('admin/', admin.site.urls),

    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/products/', ProductListPublicView.as_view()),
    path('api/products/create/', ProductCreateView.as_view()),
    path('api/products/<int:pk>/delete/', ProductDeleteView.as_view()),
    path('api/products/list/', ProductListCreateView.as_view()),

    path('api/register/', RegisterView.as_view()),
    path('api/verify-email/', VerifyEmailView.as_view()),
    path('api/resend-code/', ResendCodeView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/me/', MeView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("confirm-password/", ConfirmPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
]