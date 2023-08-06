#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.netorca_common import NetorcaBaseModule, NetorcaModuleValidationError
from ..module_utils.netorca_constants import (
    FIELDS_API_KEY,
    FIELDS_CONTEXT,
    FIELDS_OBJECT_ID,
    FIELDS_PASS,
    FIELDS_SERVICE,
    FIELDS_STATE,
    FIELDS_URL,
    FIELDS_USER,
    NETORCA_VALID_UPDATE_STATES,
)

DOCUMENTATION = r"""
---
module: update_change_instances

short_description: Update Change Instances in NetOrca

version_added: "0.1.0"

description: This module updates the change instances for a team in NetOrca.

options:
    url:
        description: Base URL for NetOrca.
        required: true
        type: str
    api_key:
        description: API Key generated for the team. If this is not specified, username and password need to be provided.
        required: false
        type: str
    username:
        description: Username for the account in the team. Use when no API KEY is available.
        required: false
        type: str
    password:
        description: Password for the account in the team. Use when no API KEY is available.
        required: false
        type: str
    uuid:
        description: The ID of the change instance to update.
        required: false
        type: str
    state:
        description: One of 'PENDING', 'ACCEPTED', 'COMPLETED'.
        required: false
        type: str

extends_documentation_fragment:
    - netautomate.netorca.update_change_instances

author:
    - Scott Rowlandson
"""

EXAMPLES = r"""
# Supply API Key and update change instance
- name: Update change instance
  update_change_instances:
    url: https://app.netorca.io
    api_key: <api key here>
    uuid: <change instance ID here>
    state: ACCEPTED

# Supply credentials and update change instance
- name: Update change instance
  netorca_update_changes:
    url: https://app.netorca.io
    username: team_member_a
    password: super_secure_password_here
    uuid: <change instance ID here>
    state: COMPLETED
"""

RETURN = r"""
# These are examples of possible return values, and in general, should use other names for return values.
updated_change_instances:
    description: The change instance returned by NetOrca.
    type: list
    returned: always
message:
    description: A general message, useful when errors are encountered.
    type: str
    returned: always
    sample: 'Updated change instance successfully'
"""


class UpdateChangeInstances(NetorcaBaseModule):
    RESULT_FIELD_SI = "updated_change_instances"

    def validate_params(self) -> None:
        super().validate_params()

        # Check that State is one of valid states
        if FIELDS_STATE in self.module.params:
            if not self.module.params[FIELDS_STATE] in NETORCA_VALID_UPDATE_STATES:
                raise NetorcaModuleValidationError("'state' is not one of {NETORCA_VALID_UPDATE_STATES}")


FIELDS = {
    FIELDS_URL: dict(type="str", required=True),
    FIELDS_API_KEY: dict(type="str", required=False, no_log=True),
    FIELDS_USER: dict(type="str", required=False),
    FIELDS_PASS: dict(type="str", required=False, no_log=True),
    FIELDS_SERVICE: dict(type="str", required=False),
    FIELDS_CONTEXT: dict(type="str", required=False),
    FIELDS_OBJECT_ID: dict(type="str", required=False),
    FIELDS_STATE: dict(type="str", required=False),
}


def main() -> None:
    module = AnsibleModule(argument_spec=FIELDS, supports_check_mode=True)

    try:
        UpdateChangeInstances(module).run_module(
            "change_instances",
            "update",
            id=module.params[FIELDS_OBJECT_ID],
            data={FIELDS_STATE: module.params[FIELDS_STATE]},
        )
    except Exception as e:
        module.fail_json(msg=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
