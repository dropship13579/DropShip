# backend/config/authentication.py
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that skips CSRF validation.
    Used for decoupled cross-origin Single Page Applications (e.g. Vercel frontend
    talking to Cloudflare Tunnel / Django API backend).
    Security is maintained via CORS (origin whitelisting), credentials rules,
    and Django's cryptographically-signed session cookies.
    """
    def enforce_csrf(self, request):
        return  # Bypass CSRF enforcement

