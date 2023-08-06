#!/usr/bin/env python3
from ansible.module_utils.basic import AnsibleModule

from ..module_utils.netorca_common import NetorcaBaseModule
from ..module_utils.netorca_constants import (
    FIELDS_API_KEY,
    FIELDS_CONTEXT,
    FIELDS_FILTERS,
    FIELDS_OBJECT_ID,
    FIELDS_PASS,
    FIELDS_SERVICE,
    FIELDS_URL,
    FIELDS_USER,
)

DOCUMENTATION = r"""
---
module: get_service_items.yml

short_description: Get Service Items form NetOrca

version_added: "0.1.0"

description: This modules gets the change instances for a team in Netorca

options:
    url:
        description : Base URL for NetOrca.
        required: true
        type: str
    api_key:
        description : API Key generataed for tema. If this is not specified, \
            username and password need to be provided.
        required: false
        type: str
    username:
        description : Username for account in the team. Use when no API KEY is \
            available.
        required: false
        type: str
    password:
        description : Password for account in the team. Use when no API KEY is \
            available.
        required: false
        type: str
    service_name:
        description : The name of the service for which we want the instances
        required: true
        type: str

extends_documentation_fragment:
    - netautomate.netorca.get_service_items

author:
    - Scott Rowlandson
"""

EXAMPLES = r"""
# Supply API Key and get all changes
- name: Get all service items
  get_service_items:
    url: https://app.netorca.io
    api_key: <api key here>
    service_name: LoadBalancer
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
service_items:
    description: An array of all the instances of that service
    type: array
    returned: always
message:
    description: A general message, useful when errors are encountered
    type: str
    returned: always
    sample: 'Returned 10 items'
"""


class GetServiceItems(NetorcaBaseModule):
    RESULT_FIELD_SI = "service_items"


FIELDS = {
    FIELDS_URL: dict(type="str", required=True),
    FIELDS_API_KEY: dict(type="str", required=False, no_log=True),
    FIELDS_USER: dict(type="str", required=False),
    FIELDS_PASS: dict(type="str", required=False, no_log=True),
    FIELDS_SERVICE: dict(type="str", required=False),
    FIELDS_CONTEXT: dict(type="str", required=False),
    FIELDS_FILTERS: dict(type="dict", required=False),
    FIELDS_OBJECT_ID: dict(type="str", required=False),
}


def main() -> None:
    module = AnsibleModule(argument_spec=FIELDS, supports_check_mode=True)

    try:
        GetServiceItems(module).run_module("service_items", "get", id=module.params.get(FIELDS_OBJECT_ID, None))
    except Exception as e:
        module.fail_json(msg=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
