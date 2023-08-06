from e2e_cli.core.helper_service import ApiFilter


def cdn_delete_helper(inputs):
    required = {"domain_id": "", }
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown """