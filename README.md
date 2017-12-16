# Dietr

## Installing

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

Code and documentation copyright 2017 dietr.io. Code released under the [MIT license](LICENSE).
