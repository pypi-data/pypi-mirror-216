
from e2e_cli.core.helper_service import ApiFilter


def create_image_helper(inputs):
    required = {"node_id": int, "image_name":""}
    optional = {}
    ApiFilter(inputs, required, optional)

def delete_image_helper(inputs):
    required = {"image_id": int, }
    optional = {}
    ApiFilter(inputs, required, optional)

def rename_image_helper(inputs):
    required = {"image_id": int, "new_name":""}
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for autoscaling_name_validity"""
