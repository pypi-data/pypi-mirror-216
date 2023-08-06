import requests
import jwt
import tempfile
import json
from os import path, getenv
from django_client_sso.exceptions import Exception401

class ClientBase():
    
    def __init__(self) -> None:
        self.host = settings.SSO_HOST
        self.client = settings.CLIENT_ID
        self.secret = settings.CLIENT_SECRET

    def get_app_token(self):
        data = {
            'client_id':self.client,
            'client_secret':self.secret,
            'grant_type':'client_credentials'
        }
        response = requests.post(f'{self.host}/o/token/',data=data)
        
        if response.status_code != 200:
            raise Exception(f'Erro ao tentar conectar no servidor sso. cod:{response.status_code}')
        
        content = response.content.decode('utf-8')
        content = json.loads(content)
        
        return content['access_token']
   
    def get_pub(self):
        if path.exists(f'{tempfile.gettempdir()}/sso.pub'):
            return        
        
        app_token = self.get_app_token()
        headers = {
            'Authorization':f'Bearer {app_token}'
        }        
        response = requests.get(f'{self.host}/pub/',headers=headers)
        content = response.content.decode('utf-8')
        content = json.loads(content)
        
        with open(f'{tempfile.gettempdir()}/sso.pub','w') as file:
            file.write(content['data'])
            file.close()
            
        
    def decode_token(self,token:str):
        self.get_pub()
        publib_key = open(f'{tempfile.gettempdir()}/sso.pub','r').read()        
        try:
            return jwt.decode(token,key=publib_key,algorithms=['RS256'])    
        except:
            raise Exception401()