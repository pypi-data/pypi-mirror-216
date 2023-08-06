from django.http import HttpResponseRedirect
from django_client_sso.client_base import ClientBase
import requests

class ClientOffice365(ClientBase):

    def login(self):
        response =  requests.get(
            url=f'{self.host}/office365/login/',
            headers={'Authorization': f'Bearer {self.get_app_token()}'}
        )
        return HttpResponseRedirect(response.url)