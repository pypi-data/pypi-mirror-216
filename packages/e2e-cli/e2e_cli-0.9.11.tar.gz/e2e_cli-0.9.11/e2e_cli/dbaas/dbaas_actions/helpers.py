
from e2e_cli.core.helper_service import ApiFilter


def db_common_helper(inputs):
    """used for start/stop/spanshot/restart/disable_backup"""
    required = {"dbaas_id": int,}
    optional = {}
    ApiFilter(inputs, required, optional)

def db_add_rempove_paramter(inputs):
    required = {"dbaas_id": int, "parameter_group_id": int}
    optional = {}
    ApiFilter(inputs, required, optional)

def db_add_rempove_vpc(inputs):
    required = {"dbaas_id": int, "network_id": int}
    optional = {}
    ApiFilter(inputs, required, optional)

def db_enable_backup(inputs):
    required = {"dbaas_id": int, "access_key":"", "bucket_location":"", "secret_key":""}
    optional = {}
    ApiFilter(inputs, required, optional)

def db_reset_password(inputs):
    required = {"dbaas_id": int, "new_password":"", "username":""}
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for bucket_name_validity"""
