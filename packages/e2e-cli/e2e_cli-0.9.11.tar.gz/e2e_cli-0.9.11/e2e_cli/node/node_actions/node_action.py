from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.node.node_actions.helpers import node_action_helper, node_rename_helper


class NodeActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_recovery": self.enable_recovery,
                        "disable_recovery": self.disable_recovery,
                        "reinstall": self.reinstall,
                        "reboot": self.reboot,
                        "power_on": self.power_on,
                        "power_off": self.power_off,
                        "rename_node": self.rename_node,
                        "lock_vm": self.lock_vm,
                        "unlock_vm": self.unlock_vm,
                        "monitor": self.node_monitoring
                        }
        return function_set.get(method)

    def action_table(self, status, req):
        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, req):
        #         try:
        #             x = PrettyTable()
        #             x.field_names = ["Action_type", "Status", "Action ID"]
        #             x.add_row([status['data']['action_type'],
        #                     status['data']['status'], status['data']['id']])
        #             Py_version_manager.py_print(x)
        #         except Exception as e:
        #                 Py_version_manager.py_print("Errors while reading json ", str(e))
        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)


    def node_monitoring(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = {}
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/monitor/server-health/?&apikey="+API_key
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def enable_recovery(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "enable_recovery_mode"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def disable_recovery(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "disable_recovery_mode"
        })
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def reinstall(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "reinstall"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def reboot(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "reboot"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def power_on(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "power_on"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def power_off(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "power_off"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def rename_node(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_rename_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        new_name = self.kwargs["inputs"]["new_name"]
        my_payload = json.dumps({
            "name": new_name,
            "type": "rename"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def unlock_vm(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "unlock_vm"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)


    def lock_vm(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        node_action_helper(self.kwargs["inputs"])
        node_id = self.kwargs["inputs"]["node_id"]
        my_payload = json.dumps({
            "type": "lock_vm"
        })
        url = "myaccount/api/v1/nodes/" + str(node_id) + \
            "/actions/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req)
