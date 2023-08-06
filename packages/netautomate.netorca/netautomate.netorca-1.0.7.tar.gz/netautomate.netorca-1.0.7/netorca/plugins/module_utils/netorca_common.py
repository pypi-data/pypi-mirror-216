#!/usr/bin/env python3
"""
NetorcaBaseModule is a base class for all Netorca Ansible modules. It provides common functionality
and helper methods for modules to interact with the Netorca API.

This class handles tasks such as authentication, connection, and error handling.

Copyright: (c) 2022, NetAutomate <info@netautomate.org>
"""
from __future__ import absolute_import, division, print_function

import logging
from typing import Any, Dict, List, Union

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.netorca import Netorca
from validators import url as url_valid

from ..module_utils.netorca_constants import (
    FIELDS_API_KEY,
    FIELDS_CONTEXT,
    FIELDS_FILTERS,
    FIELDS_PASS,
    FIELDS_URL,
    FIELDS_USER,
    VALID_FILTERS,
)

__metaclass__ = type

logging.basicConfig(filename=__name__ + ".log", level=logging.DEBUG)


class NetorcaModuleError(Exception):
    pass


class NetorcaModuleValidationError(NetorcaModuleError):
    pass


class NetorcaBaseModule:
    RESULT_FIELD_SI = None
    RESULT_FIELD_MESSAGE = "message"
    RESULT_FIELD_CHANGED = "changed"

    def __init__(self, module: Any):
        self.module = module
        self.output_dict = {
            self.RESULT_FIELD_SI: [],
            self.RESULT_FIELD_CHANGED: False,
            self.RESULT_FIELD_MESSAGE: "Starting Module",
        }

    def fail_module(self, msg: str) -> None:
        """Fail the module with the given error message."""
        result = {self.RESULT_FIELD_SI: []}
        logging.error(msg)
        self.module.fail_json(msg=msg, result=result)

    def validate_params(self) -> None:
        """Validate the input parameters."""
        params = self.module.params
        keys = params.keys()

        # Check that either api_key or username + password supplied
        if FIELDS_API_KEY not in keys:
            if not (FIELDS_USER in keys and FIELDS_PASS in keys):
                raise NetorcaModuleValidationError("If no api_key specified, username and password required")

        # Check that URL is a valid URL
        if not url_valid(params[FIELDS_URL]):
            raise NetorcaModuleValidationError(f"{params[FIELDS_URL]} is not a valid url")

    def connect(self) -> None:
        """Connect to the Netorca service."""
        try:
            self.validate_params()
        except NetorcaModuleValidationError as e:
            self.fail_module(str(e))

        # Authenticate
        if FIELDS_API_KEY not in self.module.params or not self.module.params[FIELDS_API_KEY]:
            logging.debug("No API key provided, logging in")
            netorca_auth = NetorcaAuth(
                username=self.module.params[FIELDS_USER],
                password=self.module.params[FIELDS_PASS],
                fqdn=self.module.params[FIELDS_URL],
            )
        else:
            logging.debug("API key provided, skipping logging in")
            netorca_auth = NetorcaAuth(api_key=self.module.params[FIELDS_API_KEY], fqdn=self.module.params[FIELDS_URL])

        self.netorca = Netorca(auth=netorca_auth)

    def make_filter(self) -> Dict[str, str]:
        """Create a filter based on the input parameters."""
        filters = self.module.params.get(FIELDS_FILTERS, None)

        # TODO: Implement filter fields validation
        # for filter_key in VALID_FILTERS:
        #     if filter_key in self.module.params.keys() and self.module.params[filter_key]:
        #         filters[filter_key] = self.module.params[filter_key]

        return filters

    def get_context(self) -> Union[Dict[str, Any], None]:
        """Retrieve the context from the input parameters."""
        context = None
        if FIELDS_CONTEXT in self.module.params.keys() and self.module.params[FIELDS_CONTEXT]:
            context = self.module.params.pop(FIELDS_CONTEXT)
        return context

    def run_module(self, func: str, method: str, id: str = None, data: dict = None) -> None:
        """Execute the given function and handle any errors."""
        try:
            self.connect()
            filters = self.make_filter()
            context = self.get_context()
            result_list = self.netorca.caller(func, method, filters=filters, context=context, id=id, data=data)
            if isinstance(result_list, list):
                self.make_response(result_list, as_list=True)
            else:
                self.make_response(result_list)
        except Exception as e:
            self.fail_module(f"An error occurred: {str(e)}")

    def make_response(self, result: Union[List, dict], as_list: bool = False) -> None:
        """Create the response to be returned by the module."""
        self.output_dict[self.RESULT_FIELD_SI] = result["results"] if as_list else result
        self.output_dict[self.RESULT_FIELD_MESSAGE] = f"Returned {len(result)} items"
        self.module.exit_json(**self.output_dict)
