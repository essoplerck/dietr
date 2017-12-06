# Dietr

## Installing

## Usage

```bash
$ export FLASK_APP=dietr/router.py
$ flask run --host=localhost --port=80
```

Change the **SECRET_KEY** to ensure the safety of the program.

```python
import os

# Set generate a 24 bit secret key
SECRET_KEY = hex(int.from_bytes(os.urandom(24), byteorder='big'))

del os
```

## Releases

## Contributing

## Copyright and license

Code and documentation copyright 2017 Camilla Kuijper, Daan Renken, Glenn van de Loo, Nabil Driuch, Rens Wolters, Sem van Nieuwenhuizen and Tieke Stellingwerf. Code released under the [MIT license](LICENSE).
