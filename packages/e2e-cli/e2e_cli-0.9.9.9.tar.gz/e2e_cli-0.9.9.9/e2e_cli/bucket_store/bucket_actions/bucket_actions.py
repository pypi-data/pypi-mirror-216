from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.bucket_store.bucket_actions import helpers


class BucketActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_versioning": self.enable_versioning,
                        "disable_versioning": self.disable_versioning,
                        "create_key": self.create_key,
                        "delete_key": self.delete_key,
                        "list_key": self.list_key,
                        "lock_key": self.lock_key,
                        "unlock_key": self.unlock_key,
                        "add_permission": self.add_permission
                        }
        return function_set.get(method)


    def enable_versioning(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_versioning_helper(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        my_payload = json.dumps({
            "bucket_name": bucket_name,
            "new_versioning_state": "Enabled"
        })
        url = "myaccount/api/v1/storage/bucket_versioning/" + \
            bucket_name + "/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def disable_versioning(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_versioning_helper(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        my_payload = json.dumps({
            "bucket_name": bucket_name,
            "new_versioning_state": "Disabled"
        })
        url = "myaccount/api/v1/storage/bucket_versioning/" + \
            bucket_name + "/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def create_key(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_create_key(self.kwargs["inputs"])
        key_name = self.kwargs["inputs"]["key_name"]
        my_payload = json.dumps({
            "tag": key_name
        })
        url = "myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Key Created successfully")

        Checks.show_json(status)


    def delete_key(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_delete_key(self.kwargs["inputs"])
        access_key = self.kwargs["inputs"]["access_key"]
        my_payload = {}
        query = dict()
        query['access_key'] = access_key
        url = "myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req = "DELETE"
        status = Request(url, Auth_Token, my_payload,
                         req, query=query).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Key deleted successfully")

        Checks.show_json(status)


    def list_key(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        my_payload = {}
        url = "myaccount/api/v1/storage/core/list/users/?apikey=" + API_key+"&location=Delhi"
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        # if Checks.status_result(status, req):
        #         Py_version_manager.py_print("Your Keys : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "Name", "access_key" ]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['tag'], element['access_key']])
        #                 i = i+1
        #             Py_version_manager.py_print(x)
        #         except Exception as e:
        #               Checks.show_json(status, e)
        #               return
        Checks.status_result(status)
        Checks.show_json(status)


    def lock_key(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_lock_unlock_key(self.kwargs["inputs"])
        key_id = self.kwargs["inputs"]["key_id"]
        my_payload = json.dumps({
            "disabled": True,
            "id": key_id
        })
        url = "myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req = "PUT"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Key locked")
        Checks.show_json(status)


    def unlock_key(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_lock_unlock_key(self.kwargs["inputs"])
        key_id = self.kwargs["inputs"]["key_id"]
        my_payload = json.dumps({
            "disabled": False,
            "id": key_id
        })
        url = "myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req = "PUT"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Key unlocked")
        Checks.show_json(status)


    def add_permission(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        my_payload = json.dumps({
            "role_name": "Bucket Admin",
            "users": [
                {
                    "access_key": Py_version_manager.py_input("input access key (Alphanumeric): "),
                    "disabled": False,
                    "email": "",
                    "id": Py_version_manager.py_input("enter bucket id "),
                    "is_default": False,
                    "my_account_id": None,
                    "secret_key": None,
                    "tag": Py_version_manager.py_input("name "),
                    "user_name": Py_version_manager.py_input("username ")
                }
            ]
        })
        query = dict()
        query['bucket_name'] = bucket_name
        url = "myaccount/api/v1/storage/bucket_perms/?apikey="+API_key+"&location=Delhi"
        req = "PUT"
        status = Request(url, Auth_Token, my_payload,
                         req, query=query).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Premission added successfully")
        Checks.show_json(status)


    def remove_permission(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.bucket_remove_permission(self.kwargs["inputs"])
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        bucket_permission_id = self.kwargs["inputs"]["bucket_permission_id"]
        my_payload = {}
        query = dict()
        query['access_key'] = bucket_name
        url = f"myaccount/api/v1/storage/bucket_perm/{bucket_permission_id}/?apikey={API_key}"
        req = "DELETE"
        status = Request(url, Auth_Token, my_payload,
                         req, query=query).response.json()

        if (Checks.status_result(status)):
            Py_version_manager.py_print("Premission removed")
        Checks.show_json(status)