from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from CarChargingScheduler import settings


class PreSharedKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None

        if api_key != settings.PRE_SHARED_API_KEY:
            raise AuthenticationFailed('Invalid API key')

        return None, None