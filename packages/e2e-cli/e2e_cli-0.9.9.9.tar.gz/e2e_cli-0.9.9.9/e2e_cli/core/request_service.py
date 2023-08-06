#create
import requests

from e2e_cli.core.constants import BASE_URL


class Request:
    def __init__(self, url, Auth_Token, payload, req, user_agent='cli-e2e', query={}):
        self.headers= {
                        'Authorization': 'Bearer ' + Auth_Token,
                        'Content-Type': 'application/json',
                        'User-Agent' : user_agent
                        }
        self.url=f"{BASE_URL}{url}"
        self.response = requests.request(req, self.url, headers=self.headers, data=payload, params=query)

