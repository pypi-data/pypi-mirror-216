import re

from e2e_cli.core.helper_service import ApiFilter


def bucket_crud_helper(inputs):
    required = {"bucket_name": __Check.bucket_name_validity, }
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for bucket_name_validity"""

    @classmethod
    def bucket_name_validity(self, bucket_name):
        valid = not (bool(re.findall("[A-Z]", bucket_name)) or bool(re.findall('[!@#$%^&*)(_+=}{|/><,.;:"?`~]', bucket_name)) or bool(re.findall("'", bucket_name)) or bool(re.search("]", bucket_name)) or bool(re.search("[[]", bucket_name)))
        if valid :
            return bucket_name
        else :
            raise Exception("Only following chars are supported, lowercase letters (a-z) or numbers(0-9)")