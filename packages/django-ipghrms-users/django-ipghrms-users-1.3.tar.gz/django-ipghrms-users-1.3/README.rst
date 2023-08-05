
============================
Django IPG HRMS users
============================


Quick start
============


1. Add 'users' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'users'
    ]

2. Include the users to project URLS like this::

    path('users/', include('users.urls')),

3. Run ``python manage.py migrate`` to create users model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user