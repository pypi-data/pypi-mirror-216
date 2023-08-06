from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from passageidentity import Passage, PassageError

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

        # Get User Id from Passage Authenticate Request
        try:
            psg_user_id = psg.authenticateRequest(request)
        except PassageError as e:
            raise AuthenticationFailed(e.message)

        # Check if the user exists in the database.
        try:
            user = PassageUser.objects.get(id=psg_user_id)
        except ObjectDoesNotExist:
            psg_user = psg.getUser(psg_user_id)
            user = PassageUser.objects.create_user(id=psg_user_id, email=psg_user.email)

        # Return the authenticated user
        return (user, None)