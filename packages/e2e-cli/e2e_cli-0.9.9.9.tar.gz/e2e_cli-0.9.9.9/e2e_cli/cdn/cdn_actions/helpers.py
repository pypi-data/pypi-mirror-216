from e2e_cli.core.helper_service import inputs_and_required_check, inputs_and_optional_check


def enable_disable_cdn_helper(inputs):
    required = {"domain_id": int, }
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def cdn_monitoring_helper(inputs):
    required = {"distribution_id": int, "start_date": "",
                "end_date": "", "granularity": ""}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def cdn_bandwidth_usage_helper(inputs):
    required = {"start_date": "", "end_date": "", "granularity": ""}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)


class _Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown """
