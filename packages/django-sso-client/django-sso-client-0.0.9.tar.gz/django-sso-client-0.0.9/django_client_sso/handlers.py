from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django_client_sso.exceptions import Exception401,Exception403

def default_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        return response
    
    if isinstance(exc, Exception401):
        return Response({'mensagem':str(exc.message)}, status=status.HTTP_401_UNAUTHORIZED)
        
    if isinstance(exc, Exception403):
        return Response({'mensagem':str(exc.message)}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({'mensagem':str(exc.args)}, status=status.HTTP_400_BAD_REQUEST)
    
    