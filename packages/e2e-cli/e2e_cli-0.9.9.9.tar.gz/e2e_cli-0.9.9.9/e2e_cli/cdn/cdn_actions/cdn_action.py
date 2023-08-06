from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.cdn.cdn_actions import helpers


class CdnActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if (get_user_cred(kwargs['alias'])):
            self.API_key = get_user_cred(kwargs['alias'])[1]
            self.Auth_Token = get_user_cred(kwargs['alias'])[0]
            self.possible = True
        else:
            self.possible = False

    def caller(self, method):
        function_set = {"enable_cdn": self.enable_cdn,
                        "disable_cdn": self.disable_cdn,
                        "list": self.cdn_monitoring,
                        "cdn_bandwidth_usage": self.cdn_bandwidth_usage
                        }
        return function_set.get(method)


    def cdn_monitoring(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.cdn_monitoring_helper()
        my_payload = {}
        query = dict()
        query['start_date'] = self.kwargs["inputs"]["start_date"]
        query['end_date'] = self.kwargs["inputs"]["end_date"]
        query['distribution_id'] = self.kwargs["inputs"]["distribution_id"]
        query['granularity'] = self.kwargs["inputs"]["granularity"]
        url = "myaccount/api/v1/cdn/monitoring-data/?&apikey="+API_key+"&location=Delhi"
        req = "GET"
        status = Request(url, Auth_Token, my_payload,
                         req, query=query).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def enable_cdn(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.enable_disable_cdn_helper(self.kwargs["inputs"])
        my_payload = json.dumps({
            "domain_id": self.kwargs["inputs"]["domain_id"],
            "is_enabled": True
        })
        url = "myaccount/api/v1/cdn/distributions/?apikey="+API_key
        req = "PUT"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def disable_cdn(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.enable_disable_cdn_helper(self.kwargs["inputs"])
        my_payload = json.dumps({
            "domain_id": self.kwargs["inputs"]["domain_id"],
            "is_enabled": False
        })
        url = "myaccount/api/v1/cdn/distributions/?apikey="+API_key
        req = "PUT"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def cdn_bandwidth_usage(self):
        API_key = self.API_key
        Auth_Token = self.Auth_Token
        helpers.cdn_bandwidth_usage_helper(self.kwargs["inputs"])
        my_payload = json.dumps({
            "domain": "all",
            'start_date': self.kwargs["inputs"]["start_date"],
            'end_date': self.kwargs["inputs"]["end_date"],
            'granularity': self.kwargs["inputs"]["granularity"]
        })
        url = "myaccount/api/v1/cdn/domain-usage/?apikey="+API_key+"&location=Delhi"
        req = "POST"
        status = Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
