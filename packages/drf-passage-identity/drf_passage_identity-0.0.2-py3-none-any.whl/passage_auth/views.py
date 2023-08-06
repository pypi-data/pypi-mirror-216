from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .authentication import TokenAuthentication

class AuthTokenView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        user = request.user
        user_id = user.id
        return Response({"authStatus": "success", "identifier": user_id}, status=status.HTTP_200_OK)