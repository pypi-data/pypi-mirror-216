from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.dbaas.dbaas_actions import helpers


class DBaasAction:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"take_snapshot": self.take_snapshot,
                        "reset_password": self.reset_password,
                        "stop_db": self.stop_db,
                        "start_db": self.start_db,
                        "restart_db": self.restart_db,
                        "add_parameter_group": self.add_parameter_group,
                        "remove_parameter_group": self.remove_parameter_group,
                        "add_vpc": self.add_vpc,
                        "remove_vpc": self.remove_vpc,
                        "enable_backup": self.enable_backup,
                        "disable_backup": self.disable_backup
                        }
        return function_set.get(method)


    def take_snapshot(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = json.dumps({
            "name": "sanap3"
        })
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/snapshot?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def reset_password(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = json.dumps({
            "password": self.kwargs["inputs"]["new_password"],
            "username": self.kwargs["inputs"]["username"]
        })
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/reset-password/?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def stop_db(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/shutdown?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def start_db(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/resume?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def restart_db(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/restart?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def add_parameter_group(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_add_rempove_paramter(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        parameter_group_id = self.kwargs["inputs"]["parameter_group_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/parameter-group/{parameter_group_id}/add?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def remove_parameter_group(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_add_rempove_paramter(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        parameter_group_id = self.kwargs["inputs"]["parameter_group_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/parameter-group/{parameter_group_id}/detach?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def add_vpc(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_add_rempove_vpc(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = json.dumps({
            "action": "attach",
            "network_id": self.kwargs["inputs"]["network_id"]
        })
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}//vpc-attach/?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def remove_vpc(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_add_rempove_vpc(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = json.dumps({
            "action": "detach",
            "network_id": self.kwargs["inputs"]["network_id"]
        })
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/vpc-detach/?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def enable_backup(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_enable_backup(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = json.dumps({
            "access_key": self.kwargs["inputs"]["access_key"],
            "bucket_location": self.kwargs["inputs"]["bucket_location"],
            "secret_key": self.kwargs["inputs"]["secret_key"]
        })
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/enable-backup?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def disable_backup(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.db_common_helper(self.kwargs["inputs"])
        dbaas_id = self.kwargs["inputs"]["dbaas_id"]
        my_payload = {}
        url = f"myaccount/api/v1/rds/cluster/{dbaas_id}/disable-backup?apikey={API_key}"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)