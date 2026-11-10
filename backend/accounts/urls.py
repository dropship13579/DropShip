from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    get_crsf_token,
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    ProfileView,
    ChangePasswordView,
    AddressViewSet,
    SupportTicketCreateView,
    NewsletterSubscribeView,
)



router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="address")


urlpatterns = [
    path("csrf/", get_crsf_token, name="accounts-csrf"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
    path("me/", MeView.as_view(), name="accounts-me"),
    path("profile/", ProfileView.as_view(), name="accounts-profile"),
    path("change/password/", ChangePasswordView.as_view(), name="accounts-change-password"),
    path("support/", SupportTicketCreateView.as_view(), name="accounts-support"),
    path("newsletter/", NewsletterSubscribeView.as_view(), name="accounts-newsletter"),
    path("", include(router.urls)),
]