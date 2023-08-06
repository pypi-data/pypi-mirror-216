
from e2e_cli.core.helper_service import inputs_and_required_check, inputs_and_optional_check


def create_vpc_helper(inputs):
    required = {"vpc_name": "", }
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def delete_vpc_helper(inputs):
    required = {"network_id": int, }
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)


class Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for bucket_name_validity"""
