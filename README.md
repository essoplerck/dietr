# Dietr

[![build status][image-build]][build]
[![issues][image-issues]][issues]
[![releases][image-releases]][releases]
[![license][image-license]](LICENSE)
[![website][image-website]](https://dietr.io)

![header image](images/header.png)

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

This project is build using python version `3.6`. To check your python version simply run:

```bash
$ python3 -V
```

## Usage

```bash
$ sudo python3 dietr.py
```

This project requires a relis server to run at `127.0.0.1:6379`

Change the **SECRET_KEY** to ensure the safety of the program.

```python
import os

# Set generate a 24 bit secret key
SECRET_KEY = hex(int.from_bytes(os.urandom(24), byteorder = 'big'))

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
