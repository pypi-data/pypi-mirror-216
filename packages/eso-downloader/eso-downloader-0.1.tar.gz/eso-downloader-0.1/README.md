# eso-downloader

A python package which provides an easy way to download data for a given ESO
observational program ID.

## Getting started

To run eso-downloader, you will need to add your ESO portal username and
password to the system keyring (the secure place to store login details), and
create a config file detailing where to put the data.

### Storing passwords/credentials

This package uses the keyring package (https://pypi.org/project/keyring) to
store passwords and other credentials. If keyring is unable to find a place to
store and read secrets from, see how to configure keyring at
https://keyring.readthedocs.io/en/stable/#configuring.

To add your password to the keyring on your system, run:
```
keyring set eso-downloader <your ESO portal username>
```
and enter your ESO portal password (in the future, we hope that there will be
long-lasting tokens so that we do not need to store the portal password
directly).
To confirm that the password is saved, run:
```
keyring get eso-downloader <your ESO portal username>
```

### Creating a config file

An initial starter config file (in ``.ini`` format) would be:
```
[DEFAULT]
username = <your ESO portal username>
base_dir = <where you want to save the downloaded data>
```

If you need to use different paths or different usernames for particular
programs, you can add sections for specific programs e.g.
```
[103.20AX.101]
username = <some other username>
```
or

```
[98.13BA.215]
base_dir = <some other directory>
```

### Running the script

The script will use the config file and the list of program IDs passed to it to
download in parallel all the files needed for the reduction of the found science
files, skipping those already downloaded (see algorithm below).

Doing
```
eso-downloader --config <path_to_config_file> <program_id> <program_id> ...
```
will start the download. If sent `SIGTERM`, the script will stop requesting new
files, and finish downloading the files it was working on.

## Algorithm

Given a program id `prog_id`, find science files (`dp_cat = 'SCIENCE'`) in the
ESO TAP archive using the query:
```
SELECT dp_id, datalink_url FROM dbo.raw WHERE prog_id = :prog_id AND dp_cat = 'SCIENCE'
```

Each row contains a datalink url, which will give us the following rows:
 - The science file itself (semantics `#this`)
 - The night log for that file (semantics `http://archive.eso.org/rdf/datalink/eso#night_log`)
 - URL to a datalink service for raw calibrations (semantics `http://archive.eso.org/rdf/datalink/eso#calSelector_raw2raw`)
 - URL to a datalink service for processed calibrations (semantics `http://archive.eso.org/rdf/datalink/eso#calSelector_raw2master`)

For each row:
1. Check if we have the science frame already, and if we have downloaded the
   calibrations for that science frame. If we have, skip this row.
2. Check the night log to confirm the data is acceptable. If not acceptable,
   skip this row.
3. Download the science frame, and record as having been downloaded.
4. Download the calibrations, and record as having been downloaded. See
   http://archive.eso.org/cms/application_support/calselectorInfo.html for
   details.
