from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.bucket_store.bucket_crud.helpers import bucket_crud_helper


class BucketCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"create": self.create_bucket,
                        "delete": self.delete_bucket,
                        "list": self.list_bucket
                        }
        return function_set.get(method)


    def create_bucket(self):
        Py_version_manager.py_print("Creating")
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        bucket_crud_helper(self.kwargs["inputs"])
        my_payload = {}
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        url = "myaccount/api/v1/storage/buckets/" + \
            bucket_name + "/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at"]
        #         x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
        #         Py_version_manager.py_print(x)
        #     except Exception as e:
        #             Py_version_manager.py_print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        


    def delete_bucket(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        bucket_crud_helper(self.kwargs["inputs"])
        my_payload = {}
        bucket_name = self.kwargs["inputs"]["bucket_name"]
        url = "myaccount/api/v1/storage/buckets/" + \
            bucket_name + "/?apikey="+API_key+"&location=Delhi"
        req = "DELETE"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        if Checks.status_result(status, req):
            Py_version_manager.py_print("Bucket Successfully deleted")
            Py_version_manager.py_print(
                "use following command -> e2e_cli <alias> bucket list to check if bucket has been deleted")
        Checks.show_json(status)
        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
        

    def list_bucket(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        my_payload = {}
        url = "myaccount/api/v1/storage/buckets/?apikey=" + API_key+"&location=Delhi"
        req = "GET"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
        # if Checks.status_result(status, req):
        #         Py_version_manager.py_print("Your Buckets : ")
        #         try:
        #             list=status['data']
        #             i=1
        #             x = PrettyTable()
        #             x.field_names = ["index", "ID", "Name", "Created at", "bucket size"]
        #             for element in list:
        #                 x.add_row([i, element['id'], element['name'], element['created_at'], element['bucket_size']])
        #                 i = i+1
        #             Py_version_manager.py_print(x)
        #         except Exception as e:
        #             Py_version_manager.py_print("Errors : ", e)

        # if('json' in self.kwargs["inputs"]):
        #     Checks.show_json(status)
