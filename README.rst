============
Simple Notes
============

This Google App Engine application demonstrates the usage of the Relational
Database support introduced with the SDK 1.4.3 prerelease.


Copyright and License
---------------------

Copyright 2011 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Google App Engine is a trademark of Google Inc.


Requirements
------------

The GAE SDK will be installed by zc.buildout. See the buildout.cfg file.

Buildout needs Python and the tools contained in /bin and /usr/bin of a
standard installation of the Linux operating environment. You should ensure
that these directories are on your PATH and following programs can be found:

* Python 2.5.2+ (3.x is not supported!)
* SQLite 3


Building and Running the Application
------------------------------------

Get the sources::

  $ git clone http://github.com/rodaebel/simplenotes.git

Build and run the application::

  $ cd simplenotes
  $ python bootstrap.py --distribute
  $ ./bin/buildout
  $ ./bin/dev_appserver.py parts/simplenotes

Then access the application using a web browser with the following URL::

  http://localhost:8080/


Running Unit Tests
------------------

In order to run all unit tests, enter the following command::

  $ bin/test
