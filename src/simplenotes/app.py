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
import logging
import os

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS Notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT,
    user_id VARCHAR(80)
);
"""

INSERT_NOTE = "INSERT INTO Notes (note, user_id) VALUES (?, ?);"

SELECT_NOTES = "SELECT note FROM Notes WHERE user_id=? ORDER BY id;"

DELETE_NOTES = "DELETE FROM Notes WHERE user_id=?;"

def get_login_or_logout(user):
    """Returns login/logout link."""

    link = '<a href="%(href)s">%(label)s</a>'

    if user:
        return link % dict(href=users.create_logout_url('/'), label='Logout')
    else:
        return link % dict(href=users.create_login_url('/'), label='Login')


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    @staticmethod
    def get_notes(user):
        """Retrives notes nor the given user and renders the main template."""

        notes = []
        login_or_logout = get_login_or_logout(user)

        if user:
            connection = rdbms.connect()
            cursor = connection.cursor()
            try:
                notes = cursor.execute(SELECT_NOTES, (user.user_id(),))
                notes = [n[0] for n in notes]
            except Exception, e:
                logging.error("%s", e)

        # Render the index.html template
        index_html = os.path.join(os.path.dirname(__file__), "index.html")

        template_vars = {
            "anonymous": user is None,
            "login_or_logout": login_or_logout,
            "notes": notes
        }

        return template.render(index_html, template_vars)

    def get(self):
        """Renders the main template."""

        # Get the appropriate login or logout link
        user = users.get_current_user()

        self.response.out.write(self.get_notes(user))

    def post(self):
        """Insert a new note."""

        text = self.request.get('text')

        user = users.get_current_user()

        if not user or not text:
            self.get()
            return

        connection = rdbms.connect()

        cursor = connection.cursor()

        try:
            cursor.execute(CREATE_TABLE)
            cursor.execute(INSERT_NOTE, (cgi.escape(text), user.user_id()))
            connection.commit()
        except:
            connection.rollback()

        self.response.out.write(self.get_notes(user))


class ClearHandler(webapp.RequestHandler):

    def get(self):
        """Drops the notes table."""

        user = users.get_current_user()

        if user:
            connection = rdbms.connect()
            try:
                cursor = connection.cursor()
                cursor.execute(DELETE_NOTES, (user.user_id(),))
                connection.commit()
            except Exception, e:
                logging.error("%s", e)
                connection.rollback()

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
