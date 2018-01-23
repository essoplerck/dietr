# Dietr

[![build status][image-build]][build]
[![issues][image-issues]][issues]
[![releases][image-releases]][releases]
[![license][image-license]](LICENSE)
[![website][image-website]](https://dietr.io)

![header image](header.png)

Dietr is a web app that allows users to search recipes and takes in account of their allergies and preferences. It also allows users to add roommates and check for their allergies and preferences. All allergies are gatherd from external sources using a custom made crawler.

## Table of Contents

- [Installing](#installing)
- [Usage](#usage)
- [Contributing](#contributing)
- [Releases](#releases)
- [License](#license)

## Installing

```bash
$ git clone https://github.com/essoplerck/dietr.git

$ pip3 install -r requirements.txt
```

This project is build using python version `3.6`. To check your python version run the following command.

```bash
$ python3 -V
```

This project requires redis, use the following command to install:

```bash
$ sudo apt-get install redis-server
```

## Usage

To run the project on a properly configured server run the following command:

```bash
$ sudo python3 dietr.py
```

When serving localy the config needs to be changed. Open the configurationu using `$ sudo nano config.py` and comment out the following lines:

```python
SESSION_COOKIE_DOMAIN = 'dietr.io'
SERVER_NAME = 'dietr.io:80'
PREFERRED_URL_SCHEME = 'https'
```

Open the database config using `$ sudo nano dietr/database.py` and replace the lines that specify the `self.connection` in the connect method:

```python
self.connection = sql.connect(database='renswnc266_production',
                              host='185.182.57.56',
                              user='renswnc266_dietr',
                              password='qvuemzxu',
                              cursorclass=sql.cursors.DictCursor)
```

This project requires a relis server to run at `127.0.0.1:6379`. To run redis
run the following command in a separte prompt:

```bash
$ redis-server
```

Change the **SECRET_KEY** to ensure the safety of the program.

```python
import os

# Set generate a 24 bit secret key
SECRET_KEY = hex(int.from_bytes(os.urandom(32), byteorder='big'))

del os
```

## Releases

- `v0.1.0` Initial release

A detailed changelog can be found [here](CHANGELOG.md).

## Contributing

See [contributing](CONTRIBUTING.md)

## License

Code and documentation copyright 2017 - 2018 dietr.io. Code released under the [MIT license](LICENSE).

[build]:    https://travis-ci.org/essoplerck/dietr
[issues]:   https://github.com/essoplerck/dietr/issues
[releases]: https://github.com/essoplerck/dietr/releases
[website]:  https://dietr.io

[image-build]:    https://img.shields.io/travis/essoplerck/dietr.svg?style=flat-square
[image-issues]:   https://img.shields.io/github/issues/essoplerck/dietr.svg?style=flat-square
[image-license]:  https://img.shields.io/github/license/essoplerck/dietr.svg?style=flat-square
[image-releases]: https://img.shields.io/github/tag/essoplerck/dietr.svg?label=latest%20stable%20release&style=flat-square
[image-website]:  https://img.shields.io/badge/website-online-orange.svg?style=flat-square
