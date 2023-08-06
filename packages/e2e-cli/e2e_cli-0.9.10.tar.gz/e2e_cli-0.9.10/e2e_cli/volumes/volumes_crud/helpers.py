from e2e_cli.core.helper_service import ApiFilter
from e2e_cli.volumes.volumes_crud.constants import VOLUME_IOPS


def create_volumes_helper(inputs):
    required = {"name": "", "size":__Check.allowed_size_for_volume, }
    optional = {}
    ApiFilter(inputs, required, optional)

def delete_volumes_helper(inputs):
    required = {"blockstorage_id": int,}
    optional = {}
    ApiFilter(inputs, required, optional)


class __Check:
    """Note format for input checks has been defined in this way, so that data type and format both can be handeled by inputs_and_required_check and inputs_and_optional_check"""
    """All checks/validation functions must follow this format/syntax as shown for autoscaling_name_validity"""

    @classmethod
    def allowed_size_for_volume(self, size):
        valid = size in VOLUME_IOPS
        if valid :
            return size
        else :
            raise Exception(f"Enter size, from {list(VOLUME_IOPS.keys())} only")