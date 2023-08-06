# constant, reserved keywords
RESERVES = ["alias", "all", "config", "node", "bucket", "lb", "dbaas", "create",
            "get", "list", "update", "edit", "delete", "file", "doc", "help", "default"]

# version
PACKAGE_VERSION = "e2e-cli/1.0.0 Python Linux/Mac/Windows"

# package_info
PACKAGE_INFO = " A command line tool developed by E2E Networks Ltd. \n Used to access and manage my_account/e2e_cloud services from cmd/shell \n Published 1st April 2023"

# url for api request
BASE_URL = "https://api.e2enetworks.com/"


# for better error handeling, write --action options and related help strings here for argparser

NODE_ACTIONS = ["enable_recovery", "disable_recovery", "reinstall", "reboot",
                "power_on", "power_off", "rename_node", "lock_vm", "unlock_vm", "monitor"]
NODE_ACTIONS_STR = """
        lock_vm
        unlock_vm
        reinstall
        reboot
        power_on
        power_off
        monitor
        rename_node
        enable_recovery
        disable_recovery
"""

BUCKET_ACTIONS = ["enable_versioning", "disable_versioning", "create_key",
                  "delete_key", "list_key", "lock_key", "unlock_key", "add_permission"]
BUCKET_ACTIONS_STR = """
        enable_versioning
        disable_versioning
        create_key
        delete_key
        list_key
        lock_key
        unlock_key
        add_permission
"""

DBAAS_ACTIONS = ["take_snapshot", "reset_password", "stop_db", "start_db", "restart_db", "enable_backup",
                 "disable_backup", "add_parameter_group", "remove_parameter_group", "add_vpc", "remove_vpc"]
DBAAS_ACTIONS_STR = """
        take_snapshot
        reset_password
        add_vpc
        remove_vpc
        stop_db
        start_db
        restart_db
        enable_backup
        disable_backup
        add_parameter_group
        remove_parameter_group
"""

CDN_ACTIONS = ["enable_cdn", "disable_cdn",
               "cdn_monitoring", "cdn_bandwidth_usage"]
CDN_ACTIONS_STR = """
        enable_cdn
        disable_cdn
        cdn_monitoring
        cdn_bandwidth_usage
"""

VOLUMES_ACTIONS = []
