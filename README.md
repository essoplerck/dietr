# Dietr

## Installing

```bash
pip3 install -r requirements.txt
```

This project is build using python version `3.6`. To check your python version simply run:

```bash
python3 -V
```

## Usage

```bash
python3 dietr.py
```

Change the **SECRET_KEY** to ensure the safety of the program.

```python
import os

# Set generate a 24 bit secret key
SECRET_KEY = hex(int.from_bytes(os.urandom(24), byteorder = 'big'))

del os
```

## Releases

## Contributing

## Copyright and license

Code and documentation copyright 2017 - 2018 dietr.io. Code released under the [MIT license](LICENSE).
