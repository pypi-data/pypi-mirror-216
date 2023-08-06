# Introduction 
Common functions to liveliness algorithms

# Getting Started

1. Install Python 3
2. Create virtual env (python3 -m venv .venv)
3. Activate virtual env (. ./.venv/bin/activate)
4. Install dependencies (pip install -U pip --no-cache && pip install -r requirements.txt)


# Package Library
1. pip install twine
2. Compile: python setup.py sdist
3. Upload: twine upload dist/* -r pypi

# Configurações de uso

1. Adicionar no arquivo requirements.txt

django-sso-client==0.0.6

# Depenências da lib django-sso-client

django==4.2.1
djangorestframework==3.14.0
django-cors-headers==4.0.0
django-filter==23.2
django-oauth-toolkit==2.2.0
PyJWT==2.7.0
requests==2.31.0
bcrypt==4.0.1
ipython==8.13.2

2. variáveis de ambiente (settings.py)

SSO_HOST= 'https://sso.titcs-devops.com.br'
CLIENT_ID='<client_id>'
CLIENT_SECRET='<passwd>'

3. filtro para capturar de exceções

REST_FRAMEWORK = {
    ....

    'EXCEPTION_HANDLER': 'django_client_sso.handlers.default_exception_handler'

    ....
}

# Exemplo de uso

1. Validação de acesso a rota

from django_client_sso.decorators import validator_with_request,validator_without_request

@action(detail=False, methods=['GET'])
@validator_with_request(permissions ="foguete_user missoes_admin")
def minha_action(self, request):
    return Response({'ok':'ok'})  

@validator_without_request(permissions='foguete_users')
def get_queryset(self):
    return MinhaModel.objects.all() 

2. Login 

from django_client_sso.client_office365 import ClientOffice365

@action(detail=False, methods=['GET'])
def login(self,request):
    client = ClientOffice365()
    response = client.login()
    return response
