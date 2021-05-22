## GNUCASH-ASX-FETCH

This is a command line utility to fetch and update
[ASX](https://asx.com.au) share prices to one or more
[GnuCash](https://www.gnucash.org/) XML files. It takes multiple path
arguments: one of more GnuCash files, or directories. If a directory is
given then it updates all the GnuCash files in that directory. It can
not update any GnuCash files that are currently open so will generate an
error message for those files. A new price entry is added for each ASX
share existing in the file each time you run it. Open the GnuCash price
database editor for a file to view, edit, or remove the new entries
added.

For example, to update the share prices of all the ASX shares in all the
GnuCash files in the current directory type:

```
$ gnucash-asx-fetch .
```

:warning: This utility overwrites your GnuCash file[s] so be sure to save
copies at least the first time you try using it.

Note it only updates GnuCash XML files, not GnuCash sqlite files. It
silently skips GnuCash backup and log files.
This utility should work on any modern Linux platform and has been
developed against GnuCash v4.4.

### MOTIVATION

GnuCash uses the [Finance::Quote](https://github.com/finance-quote)
module to update share prices but I have found it fragile over the short
time I have been using GnuCash. E.g. At the time I created this utility,
ASX price fetches via [Finance::Quote](https://github.com/finance-quote)
have not worked for more than 3 months as per [this
bug](https://github.com/finance-quote/finance-quote/issues/166).

Fetching prices from [ASX](https://asx.com.au) is actually quite easy
and this utility uses a simple approach. By merely requiring the user to
not have the file open at the time the prices are updated, it can avoid
the awkward interface with
[Finance::Quote](https://github.com/finance-quote) and GnuCash
completely, and merely write directly to the XML file.

If you like this utility then you may be interested in [another
utility](https://github.com/bulletmark/gnucash-select) I created to
facilitate working with multiple GnuCash files.

### USAGE

```
usage: gnucash-asx-fetch [-h] [-i] [-q] [-d] path [path ...]

Utility to fetch and add current ASX share prices to one or more gnucash XML
files.

positional arguments:
  path               directories or files to update

optional arguments:
  -h, --help         show this help message and exit
  -i, --ignore-open  silently ignore any files currently open
  -q, --quiet        suppress message output
  -d, --dry-run      do not update any file[s]
```

See the latest documentation and code at
https://github.com/bulletmark/gnucash-asx-fetch.

### INSTALLATION

Python 3.6 or later is required. Note [gnucash-asx-fetch is on
PyPI](https://pypi.org/project/gnucash-asx-fetch/) so just ensure that
`python3-pip` and `python3-wheel` are installed then type the following
to install (or upgrade):

```
$ sudo pip3 install -U gnucash-asx-fetch
```

Arch Linux users can install [gnucash-asx-fetch from the
AUR](https://aur.archlinux.org/packages/gnucash-asx-fetch/).
Alternately, do the following to install from the source repository.

```sh
$ git clone http://github.com/bulletmark/gnucash-asx-fetch
$ cd gnucash-asx-fetch

# Install globally ..
$ sudo pip3 install -U .
```

### UPGRADE

```sh
$ cd gnucash-asx-fetch  # Source dir, as above
$ git pull

$ sudo pip3 install -U .
```

### REMOVAL

```sh
$ sudo pip3 uninstall gnucash-asx-fetch
```

### LICENSE

Copyright (C) 2020 Mark Blakeney. This program is distributed under the
terms of the GNU General Public License.
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License at <http://www.gnu.org/licenses/> for more details.
