# -*- coding: utf-8 -*-
#
# Copyright 2011 Tobias Rodäbel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for the Simple Notes application."""

from google.appengine import api
from google.appengine.api import rdbms_sqlite
from google.appengine.ext import testbed

import os
import sys
import unittest
import webtest


class TestApp(unittest.TestCase):
    """Test case for the Simple Notes application."""

    def setUp(self):
        """Set up test environment."""

        # Create an instance of the Testbed class
        self.testbed = testbed.Testbed()

        # Activate the testbed
        self.testbed.activate()

        # We need an authenticated admin user
        self.testbed.init_user_stub()
        os.environ["USER_EMAIL"] = "test@example.com"
        os.environ["USER_ID"] = "185804764220139124118"
        os.environ["USER_IS_ADMIN"] = "1"

        # Setup the rdbms sqlite service
        sys.modules['google.appengine.api.rdbms'] = rdbms_sqlite
        api.rdbms = rdbms_sqlite
        rdbms_sqlite.SetSqliteFile("test.rdbms")
        rdbms_sqlite.connect(database='')

    def tearDown(self):
        """Clean up."""

        self.testbed.deactivate()

        # Remove the rdbms sqlite test db
        os.unlink("test.rdbms")

    def testMainHandler(self):
        """Tests the main handler."""

        from app import app

        simplenotes = webtest.TestApp(app)

        response = simplenotes.get('/')
