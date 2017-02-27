Django Active Users Stats
=========================

A reusable Django app that tracks number of requests per day per user.

The default User model only tracks `date_joined` and `last_login`, which is
not enough to calculate daily active users and monthly active users over time.

You could theoretically solve this by sending custom tagged events to
Google Analytics or Mixpanel, but that might also be tricky to implement and
not 100% reliable (because of ad-blockers, for example).

This is just a very simple middleware that fills rows into a table of the
form:

```
PK | User (FK) | Day (Date) | Requests (Integer)
------------------------------------------------
```

This should allow you to easily create queries to compute your daily active
users metric and, using `TruncMonth` to compute your monthly active users
metric. It should also allow you to compute other metrics like active users,
returning users and churned users.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-active-users-stats

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/theartling/django-active-users-stats.git#egg=active_users

Add ``active_users`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'active_users',
    )

Add ``active_users.middleware.ActiveUsersMiddleware`` to your
``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...,
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'active_users.middleware.ActiveUsersMiddleware',
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate active_users


Usage
-----

Once the middleware is installed, your app should start tracking events.
Check the ``active_users.Requests`` table and see if rows are being created
when you browse your site.

Configuration
-------------

**DISABLE_ACTIVE_USERS**

Set to ``True`` to disable tracking. The middleware will just return the
request and do nothing.

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-active-users-stats
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
