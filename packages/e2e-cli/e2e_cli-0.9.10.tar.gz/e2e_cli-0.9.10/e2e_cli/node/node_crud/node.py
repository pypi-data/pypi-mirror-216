import json

from prettytable import PrettyTable


from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.core.helper_service import Checks
from e2e_cli.node.node_crud.helpers import node_create_helper, node_delete_helper, node_get_helper
from e2e_cli.node.node_crud.node_listing_service import Nodelisting


class NodeCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False


    def caller(self, method):
        function_set = {"create": self.create_node,
                        "delete": self.delete_node,
                        "get": self.get_node_by_id,
                        "list": self.list_node
                        }
        return function_set.get(method)


    def create_node(self):
        Py_version_manager.py_print("Creating")
        my_payload = node_create_helper(self.kwargs)
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "POST"
        if ('auto' in self.kwargs["inputs"]):
            user_agent = 'cli_python'
        else:
            user_agent = 'cli-e2e'
        my_payload = my_payload.__dict__

        status = Request(url, Auth_Token, json.dumps(
            my_payload), req, user_agent).response.json()

        # if Checks.status_result(status,req):
        #     try :
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at", "disk", "Status", "Plan"]
        #         x.add_row([status['data']['id'], status['data']['name'],
        #               status['data']['created_at'], status['data']['disk'], status['data']['status'], status['data']['plan']])
        #         Py_version_manager.py_print(x)
        #     except Exception as e:
        #             Py_version_manager.py_print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        Checks.status_result(status)
        Checks.show_json(status)


    def delete_node(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_delete_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        url = "myaccount/api/v1/nodes/" + \
            str(node_id) + "/?apikey="+API_key
        req = "DELETE"

        confirmation = Py_version_manager.py_input(
            "are you sure you want to delete press y for yes, else any other key : ")
        if (confirmation.lower() == "y"):
            status = Request(url, Auth_Token, my_payload, req).response.json()
            if Checks.status_result(status, req):
                Py_version_manager.py_print("Node Successfully deleted")
                Py_version_manager.py_print(
                    "use following command -> e2e_cli <alias> node list to check if bucket has been deleted")

            # if('json' in self.kwargs["inputs"]):
            #     Checks.show_json(status)
        Checks.show_json(status)


    def get_node_by_id(self):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_get_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        url = "myaccount/api/v1/nodes/" + \
            str(node_id) + "/?apikey="+API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["VM id", "Name", "Created at", "disk", "Plan", "Public IP", "Status"]
        #         x.add_row([ status['data']['vm_id'], status['data']['name'], status['data']['created_at'], status['data']['disk'],  status['data']['plan'], status['data']['public_ip_address'], status['data']['status'] ])
        #         Py_version_manager.py_print(x)
        #     except Exception as e:
        #                 Py_version_manager.py_print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        Checks.status_result(status)
        Checks.show_json(status)


    def list_node(self, parameter=0):
        my_payload = {}
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "myaccount/api/v1/nodes/?apikey=" + API_key+"&location=Delhi"
        req = "GET"
        status = Request(url, Auth_Token, my_payload,
                         req).response.json()

        if parameter == 0:
            # if Checks.status_result(status, req):
            #     list=status['data']
            #     try:
            #         i = 1
            #         x = PrettyTable()
            #         x.field_names = ["index", "ID", "Name", "Plan", "Status"]
            #         for element in list:
            #             x.add_row([i, element['id'], element['name'],
            #                       element['plan'],  element['status']])
            #             i = i+1
            #         Py_version_manager.py_print(x)
            #     except Exception as e:
            #             Py_version_manager.py_print("Errors : ", e)

            #     if('json' in self.kwargs["inputs"]):
            #         Checks.show_json(status)
            Checks.status_result(status)
            Checks.show_json(status)

        elif parameter == 1:
            return status['data']


    def update_node(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        Py_version_manager.py_print("update call")
