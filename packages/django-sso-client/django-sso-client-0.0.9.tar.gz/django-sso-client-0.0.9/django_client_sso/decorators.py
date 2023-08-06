from functools import wraps
from django_client_sso.client_base import ClientBase
from django_client_sso.exceptions import Exception403,Exception401

def validator_with_request(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self, request):
            client = ClientBase()
            token = request.META.get('HTTP_AUTHORIZATION')
            
            if not token:
                raise Exception401()
            
            token = token.replace('Bearer ', '')
            token_decode = client.decode_token(token)
            
            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self,request)
           
            raise Exception403()
    
        return wrapper

    return decorator_func


def validator_with_args_kwargs(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            client = ClientBase()
            token = request.META.get('HTTP_AUTHORIZATION')
            
            if not token:
                raise Exception401()
            
            token = token.replace('Bearer ', '')
            token_decode = client.decode_token(token)
            
            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self,request, *args, **kwargs)
           
            raise Exception403()
    
        return wrapper

    return decorator_func

def validator_without_request(permissions):
    def decorator_func(func):
        @wraps(func)
        def wrapper(self):
            client = ClientBase()
            token = self.request.META.get('HTTP_AUTHORIZATION')
            
            if not token:
                raise Exception401()
            
            token = token.replace('Bearer ', '')
            token_decode = client.decode_token(token)
            
            required = str(permissions).split()
            scope = token_decode['scope']

            for r in required:
                if r in scope:
                    return func(self)
           
            raise Exception403()
    
        return wrapper

    return decorator_func
