"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

import os
import unittest

from graph_notebook.configuration.get_config import get_config
from graph_notebook.configuration.generate_config import Configuration, DEFAULT_AUTH_MODE, AuthModeEnum, generate_config


class TestGenerateConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generic_host = 'blah'
        cls.neptune_host = 'instance.cluster.us-west-2.neptune.amazonaws.com'
        cls.port = 8182
        cls.test_file_path = f'{os.path.abspath(os.path.curdir)}/test_configuration_file.json'

    def tearDown(self) -> None:
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_configuration_default_auth_defaults_neptune(self):
        config = Configuration(self.neptune_host, self.port)
        self.assertEqual(self.neptune_host, config.host)
        self.assertEqual(self.port, config.port)
        self.assertEqual(DEFAULT_AUTH_MODE, config.auth_mode)
        self.assertEqual(True, config.ssl)
        self.assertEqual('', config.load_from_s3_arn)

    def test_configuration_default_auth_defaults_generic(self):
        config = Configuration(self.generic_host, self.port)
        self.assertEqual(self.generic_host, config.host)
        self.assertEqual(self.port, config.port)
        self.assertEqual(True, config.ssl)

    def test_configuration_override_defaults_neptune(self):
        auth_mode = AuthModeEnum.IAM
        ssl = False
        loader_arn = 'foo'
        config = Configuration(self.neptune_host, self.port, auth_mode=auth_mode, load_from_s3_arn=loader_arn, ssl=ssl)
        self.assertEqual(auth_mode, config.auth_mode)
        self.assertEqual(ssl, config.ssl)
        self.assertEqual(loader_arn, config.load_from_s3_arn)

    def test_configuration_override_defaults_generic(self):
        ssl = False
        config = Configuration(self.generic_host, self.port, ssl=ssl)
        self.assertEqual(ssl, config.ssl)

    def test_generate_configuration_with_defaults_neptune(self):
        config = Configuration(self.neptune_host, self.port)
        c = generate_config(config.host, config.port, auth_mode=config.auth_mode, ssl=config.ssl,
                            load_from_s3_arn=config.load_from_s3_arn, aws_region=config.aws_region)
        c.write_to_file(self.test_file_path)
        config_from_file = get_config(self.test_file_path)
        self.assertEqual(config.to_dict(), config_from_file.to_dict())

    def test_generate_configuration_with_defaults_generic(self):
        config = Configuration(self.generic_host, self.port)
        c = generate_config(config.host, config.port, ssl=config.ssl)
        c.write_to_file(self.test_file_path)
        config_from_file = get_config(self.test_file_path)
        self.assertEqual(config.to_dict(), config_from_file.to_dict())

    def test_generate_configuration_override_defaults_neptune(self):
        auth_mode = AuthModeEnum.IAM
        ssl = False
        loader_arn = 'foo'
        aws_region = 'us-west-2'
        config = Configuration(self.neptune_host, self.port, auth_mode=auth_mode, load_from_s3_arn=loader_arn, ssl=ssl,
                               aws_region=aws_region)

        c = generate_config(config.host, config.port, auth_mode=config.auth_mode, ssl=config.ssl,
                            load_from_s3_arn=config.load_from_s3_arn, aws_region=config.aws_region)
        c.write_to_file(self.test_file_path)
        config_from_file = get_config(self.test_file_path)
        self.assertEqual(config.to_dict(), config_from_file.to_dict())

    def test_generate_configuration_override_defaults_generic(self):
        ssl = False
        config = Configuration(self.generic_host, self.port, ssl=ssl)
        c = generate_config(config.host, config.port, ssl=config.ssl)
        c.write_to_file(self.test_file_path)
        config_from_file = get_config(self.test_file_path)
        self.assertEqual(config.to_dict(), config_from_file.to_dict())
