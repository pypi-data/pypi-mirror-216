from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.vpc import helpers


class vpc_Crud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False

    def caller(self, method):
        function_set = {"create": self.create_vpc,
                        "delete": self.delete_vpc,
                        "list": self.list_vpc,
                        }
        return function_set.get(method)   


    def create_vpc(self):
        Py_version_manager.py_print("Creating")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        helpers.create_vpc_helper(self.kwargs["inputs"])
        my_payload= json.dumps({
                "network_size": 512,
                "vpc_name": self.kwargs["inputs"]["vpc_name"]
            })
        url =  f"myaccount/api/v1/vpc/?apikey={API_key}&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.show_json(status)        
        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name"]
        #         x.add_row([status['data']['vpc_id'], status['data']['name'] ])
        #         Py_version_manager.py_print(x)
        #     except Exception as e:
        #               Py_version_manager.py_print("Errors : ", e)         
        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)    


    def delete_vpc(self):
        my_payload={}
        network_id=self.kwargs["inputs"]["network_id"]
        helpers.delete_vpc_helper(self.kwargs["inputs"])
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  f"myaccount/api/v1/vpc/{network_id}/?apikey={API_key}"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        if Checks.status_result(status,req):
                        Py_version_manager.py_print("vpc Successfully deleted")
                        Py_version_manager.py_print("use following command -> e2e_cli --alias vpc list to check if vpc has been deleted")
        
        Checks.show_json(status)


    def list_vpc(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url =  "myaccount/api/v1/vpc/list/?apikey="+ API_key+"&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        Checks.show_json(status)
        # if Checks.status_result(status, req):
        #         Py_version_manager.py_print("Your vpcs : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "network_id", "Name", "network_mask", "gateway_ip", "pool_size"]
        #             for element in list:
        #                 x.add_row([i, element['network_id'], element['name'], element['network_mask'], element["gateway_ip"], element["pool_size"]])
        #                 i = i+1
        #             Py_version_manager.py_print(x)
        #         except Exception as e:
        #               Py_version_manager.py_print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)    


