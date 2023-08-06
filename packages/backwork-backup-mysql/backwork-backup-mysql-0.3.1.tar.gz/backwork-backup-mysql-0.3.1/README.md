# backwork-backup-mysql [![Build Status](https://travis-ci.org/IBM/backwork-backup-mysql.svg?branch=master)](https://travis-ci.org/IBM/backwork-backup-mysql) [![PyPI version](https://badge.fury.io/py/backwork-backup-mysql.svg)](https://badge.fury.io/py/backwork-backup-mysql)
Add support for MySQL backups on [`backwork`](https://github.com/IBM/backwork).

## Requirements
This plug-in is build on top of [`mysqldump`](http://dev.mysql.com/doc/refman/en/mysqldump.html),
so you will need to it installed.

`mysqldump` is part of the `mysql` client.cd .

## Installing
You can use `pip` to install this plug-in:
```sh
$ pip install backwork-backup-mysql
```

## Using
After installing the plug-in you will be able to use the `backup mysql` and `restore mysql` commands
on `backwork`:


#### backwork backup mysql
```sh
$ backwork backup mysql -h
usage: backwork backup mysql [-h] [--gzip] [-o OUTPUT]

Backup a MySQL database. It uses `mysqldump` so it's required to have it
installed and added to the system's PATH. You can use any of the arguments
supported by `mysqldump`. Use `mysqldump -h` for more information.

optional arguments:
  -h, --help            show this help message and exit
  --gzip                compress output file  (requires gzip to be installed)
  -o OUTPUT, --output OUTPUT
                        output file path
```

You can pass any option that you would normally use on `mysqldump`:

```sh
$ backwork backup mysql --host 192.168.99.1 -u root -ppassword --port 32769 --all-databases
```

As shown in the `--help` message, there are two extra arguments you can use in
your backup process `--gzip` and `-o`.

`--gzip` will compress the output and requires the `gzip` command to be
available in your system.

`-o OUTPUT` or `--output OUTPUT` will save the output of `mysqldump` into a
file.

#### backwork restore mysql

```sh
usage: backwork restore mysql [-h] [--gzip] [-i INPUT]

Restore MySQL databases. It uses `mysql` so it's required to have it
installed and added to the system's PATH.

optional arguments:
  -h, --help            show this help message and exit
  --gzip                decompress backup file before restoring (requires gzip to be installed)
  ```

You can pass any option that you would normally use to connect to your mysql instance:

```sh
$ backwork restore mysql --host 192.168.99.1 -u root -ppassword --port 32769 --gzip --input=="mybackup.archive.gz"
```

**Important:** There is a conflict with the `-h` argument since it is reserved
for the help/usage message. User `--host` to pass the hostname.
