import re

from e2e_cli.core.helper_service import inputs_and_required_check, inputs_and_optional_check


def bucket_versioning_helper(inputs):
    required = {"bucket_name": Check.bucket_name_validity,}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def bucket_create_key(inputs):
    required = {"key_name": str,}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def bucket_delete_key(inputs):
    required = {"access_key": str,}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def bucket_lock_unlock_key(inputs):
    required = {"key_id": int,}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)

def bucket_remove_permission(inputs):
    required = {"bucket_name": Check.bucket_name_validity, "bucket_permission_id": int}
    optional = {}
    inputs_and_required_check(inputs, required)
    inputs_and_optional_check(inputs, optional)


class Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for bucket_name_validity"""

    @classmethod
    def bucket_name_validity(self, bucket_name):
        valid = not (bool(re.findall("[A-Z]", bucket_name)) or bool(re.findall('[!@#$%^&*)(_+=}{|/><,.;:"?`~]', bucket_name)) or bool(re.findall("'", bucket_name)) or bool(re.search("]", bucket_name)) or bool(re.search("[[]", bucket_name)))
        if valid :
            return bucket_name
        else :
            raise Exception("Only following chars are supported, lowercase letters (a-z) or numbers(0-9)")