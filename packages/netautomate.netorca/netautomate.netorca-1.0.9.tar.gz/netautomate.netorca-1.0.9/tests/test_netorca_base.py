import unittest
from unittest.mock import patch

from netorca.plugins.repository import NetorcaBaseModule, NetorcaModuleValidationError


class MockNetorcaAuth:
    def __init__(self, username=None, password=None, fqdn=None, api_key=None):
        pass


class MockNetorca:
    def __init__(self, auth=None):
        pass


class MockAnsibleModule:
    def __init__(self, argument_spec=None):
        self.params = {
            "api_key": "test_key",
            "url": "https://example.com",
        }

    def fail_json(self, *args, **kwargs):
        raise Exception("Module failed")


class TestNetorcaBaseModule(unittest.TestCase):
    def setUp(self):
        self.mock_module = MockAnsibleModule()
        self.base_module = NetorcaBaseModule(self.mock_module)

    @patch("netorca_sdk.netorca.Netorca", new=MockNetorca)
    @patch("netorca_sdk.auth.NetorcaAuth", new=MockNetorcaAuth)
    def test_connect_with_api_key(self):
        try:
            self.base_module.connect()
        except Exception as e:
            self.fail(f"connect() raised an exception: {e}")

    def test_make_filter(self):
        self.mock_module.params["service_name"] = "test_value"
        expected_filter = {"service_name": "test_value"}
        self.assertEqual(self.base_module.make_filter(), expected_filter)

    def test_get_context(self):
        self.mock_module.params["context"] = {"key": "value"}
        expected_context = {"key": "value"}
        self.assertEqual(self.base_module.get_context(), expected_context)

    def test_fail_module(self):
        with self.assertRaises(Exception) as context:
            self.base_module.fail_module("Test failure")
        self.assertTrue("Module failed" in str(context.exception))

    def test_validate_params_without_api_key_and_username_password(self):
        self.mock_module.params = {
            "url": "https://example.com",
        }
        with self.assertRaises(NetorcaModuleValidationError) as context:
            self.base_module.validate_params()
        self.assertTrue("If no api_key specified, username and password required" in str(context.exception))

    def test_validate_params_with_invalid_url(self):
        self.mock_module.params = {
            "api_key": "test_key",
            "url": "invalid_url",
        }
        with self.assertRaises(NetorcaModuleValidationError) as context:
            self.base_module.validate_params()
        self.assertTrue("is not a valid url" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
