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
"""Simple GAE app to demonstrate the usage of the rdbms API."""

from google.appengine.api import rdbms
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import cgi
import os

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS Notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT
);
"""

INSERT_NOTE = "INSERT INTO Notes (note) VALUES (?);"

def get_login_or_logout(user):
    """Returns login/logout link."""

    s = '<a href="%(href)s">%(label)s</a>'
    if user:
        r = (False, s % dict(href=users.create_logout_url('/'), label='Logout'))
    else:
        r = (True, s % dict(href=users.create_login_url('/'), label='Login'))
    return r


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    def get(self):
        """Renders the main template."""

        # Get the appropriate login or logout link
        anonymous, login_or_logout = get_login_or_logout(
            users.get_current_user())

        notes = []

        if not anonymous:
            connection = rdbms.connect()
            cursor = connection.cursor()
            try:
                notes = cursor.execute("SELECT note FROM Notes ORDER BY id;")
                notes = [n[0] for n in notes]
            except:
                notes = ["Add your first note below..."]

        # Render the index.html template
        index_html = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(index_html, locals()))

    def post(self):
        """Insert a new note."""

        text = self.request.get('text')

        if not users.get_current_user() or not text:
            self.get()
            return

        connection = rdbms.connect()

        cursor = connection.cursor()

        try:
            cursor.execute(CREATE_TABLE)
            cursor.execute(INSERT_NOTE, (cgi.escape(text),))
            connection.commit()
        except:
            connection.rollback()

        self.get()


class ClearHandler(webapp.RequestHandler):

    def get(self):
        """Drops the notes table."""

        if users.get_current_user():
            connection = rdbms.connect()
            cursor = connection.cursor()
            cursor.execute("DROP TABLE Notes;")

        self.redirect('/')


app = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/clear', ClearHandler),
], debug=True)


def main():
    """The main function."""

    webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
