.. _getting-started:

Getting started
###############

In order to start downloading data from the ESO archive, you'll need to do the
following:

#. Install eso-downloader
#. Add your ESO portal password to the system keyring (the secure place to store
   passwords and the like).
#. Create a config file to specify where to download the files to


Installing eso-downloader
-------------------------

eso-downloader is on PyPI, and therefore can be installed via:

.. code-block:: shell

    $ pip install eso-downloader

Development happens at https://dev.aao.org.au/adacs/eso-downloader, and after
cloning the git repository, running:

.. code-block:: shell

    $ pip install .

will install a development version of eso-downloader.

Using pip to install eso-downloader should install all the required
dependencies, but you may need to install additional packages to communicate
with the system keyring (see below) depending on your setup and operating
system.

Adding your password to the system keyring
------------------------------------------

eso-downloader uses the `keyring <https://pypi.org/project/keyring/>`_ package
to securely store your password. As the mechanism for performing the secure
storage vary across systems, you may need to spend some time getting the keyring
package set up correctly. Please see the
`keyring documentation <https://pypi.org/project/keyring/>`_ for how to do this.

The easiest way to confirm that keyring has been set up correctly is to add your
ESO portal password to the keyring. keyring provides a shell command ``keyring``
which allows you to interact with the system keyring. By running:

.. code-block:: shell

    $ keyring set eso-downloader <your ESO portal username>

to set your password, and then running:

.. code-block:: shell

    $ keyring get eso-downloader <your ESO portal username>

you should see your ESO password printed in the terminal. If you do not see your
password, or keyring prints an error, keyring has likely not found the correct
mechanism to access the system keyring. See the
`keyring documentation <https://pypi.org/project/keyring/>`_ for how to
troubleshoot your system.

Creating a config file
----------------------

eso-downloader uses a config file to know where to save the downloaded data, and
any differences in how to treat data from different proposals.

An initial starter config file (in `.ini` format) would be:

.. code-block:: ini

    [DEFAULT]
    username = <your ESO portal username>
    base_dir = <where you want to save the downloaded data>

See :ref:`configuring` for more advanced configuration options and examples.


Downloading your first ESO program
----------------------------------

The eso-downloader shell command is designed to download all the data for a
specific ESO program, allowing a team to re-run eso-downloader to download any
new observations. If you only want a subset of the data (e.g. a specific science
observation and its calibrations and associated files), you will want to use the
Python API to have specific control over what is downloaded.

Starting the download of the program is done by running the following:

.. code-block:: shell

    $ eso-downloader --config <path_to_config_file> <program_id>

This will print out what is being downloaded, and will skip over any files that
already exist.

Running:

.. code-block:: shell

    $ eso-downloader --help

will print out all the other options that eso-downloader supports.
