from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verifyToken(request):
    req = requests.Request()
    token = request.data['tokenId']
    audience = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
    user_google_info = id_token.verify_oauth2_token(token, req, audience)
    return Response(user_google_info, status=status.HTTP_200_OK)