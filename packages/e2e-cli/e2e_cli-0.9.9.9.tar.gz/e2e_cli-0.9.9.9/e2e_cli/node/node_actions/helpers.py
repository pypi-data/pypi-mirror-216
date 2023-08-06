
from e2e_cli.core.helper_service import inputs_and_required_check, inputs_and_optional_check


def node_action_helper(inputs):
    required = {"node_id": int, }
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)


def node_rename_helper(inputs):
    required = {"node_id": int, "new_name":str}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

