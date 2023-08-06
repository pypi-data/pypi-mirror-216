import re

from e2e_cli.core.helper_service import ApiFilter


def autoscaling_crud_helper(inputs):
    required = {"autoscaling_id": int, }
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for autoscaling_name_validity"""

    @classmethod
    def autoscaling_name_validity(self, autoscaling_name):
        valid = not (bool(re.findall("[A-Z]", autoscaling_name)) or bool(re.findall('[!@#$%^&*)(_+=}{|/><,.;:"?`~]', autoscaling_name)) or bool(re.findall("'", autoscaling_name)) or bool(re.search("]", autoscaling_name)) or bool(re.search("[[]", autoscaling_name)))
        if valid :
            return autoscaling_name
        else :
            raise Exception("Only following chars are supported, lowercase letters (a-z) or numbers(0-9)")