# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import deci_platform_client
from deci_platform_client.paths.invites_ import post  # noqa: E501
from deci_platform_client import configuration, schemas, api_client

from .. import ApiTestMixin


class TestInvites(ApiTestMixin, unittest.TestCase):
    """
    Invites unit test stubs
        Invite Colleague  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = post.ApiForpost(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200






if __name__ == '__main__':
    unittest.main()
