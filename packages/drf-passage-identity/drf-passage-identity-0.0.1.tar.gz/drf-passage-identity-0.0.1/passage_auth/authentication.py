from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import authentication

from passageidentity import Passage

from .models import PassageUser

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the access token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Extract the token from the header
        psg_user_id = psg.authenticateRequest(request)
        psg_user = psg.getUser(psg_user_id)

        # Check if the token exists in the AccessToken model
        try:
            user = PassageUser.objects.get(id=psg_user.id)
        except ObjectDoesNotExist:
            user = PassageUser.objects.create_user(id=psg_user.id, email=psg_user.email)

        # Return the authenticated user
        return (user, None)