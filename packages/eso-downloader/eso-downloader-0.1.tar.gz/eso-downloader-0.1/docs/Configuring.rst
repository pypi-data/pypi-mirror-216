.. _configuring:

Configuring
###########

:command:`eso-downloader` uses an ``.ini`` file to work out what to do for each program
requested to be downloaded. The ``DEFAULT`` section specifies what the default
values of each setting should be.

If you need to use different paths or different usernames for particular
programs, you can add sections for specific programs. For example, to override
the username (and hence password) to use for a specific program, do:

.. code-block:: ini

    [103.20AX.101]
    username = <some other username>

or to save a program to a different path, do:

.. code-block:: ini

    [98.13BA.215]
    base_dir = <some other directory>

In the future, more options may become available.

Current Options
---------------

.. program:: eso-downloader-config

.. option:: username

    The username to use for finding and downloading the data for an ESO program.
    This must have a matching password stored by keyring.

.. option:: base_dir

    The base path as to where to save the data downloaded for a program. Does
    not have to exist before ``eso-downloader`` is run.
