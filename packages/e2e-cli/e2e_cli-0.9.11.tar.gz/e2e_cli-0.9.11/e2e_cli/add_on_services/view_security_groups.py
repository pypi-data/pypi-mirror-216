import json

from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request



class SecurityGroup:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False


    def list_security_groups(self):
        my_payload = ""
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "myaccount/api/v1/security_group/?apikey="+API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()
        data=status['data']
        if(data):
            x = PrettyTable()
            x.field_names = ["security_group_id", "Name", "description"]
            x.add_row([ data[0]['id'], data[0]['name'], data[0]['description'] ])
        Py_version_manager.py_print(x)
