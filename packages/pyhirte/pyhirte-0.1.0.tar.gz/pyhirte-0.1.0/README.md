# hirte python bindings

The hirte python bindings provides a python module to interact with the D-Bus API of hirte. It consists of the following
subpackages:

- [gen](./gen/): auto-generated code based the hirte D-BUS API description
- [ext](./ext/): custom written code to simplify common tasks

## Installation

Using `pip3`:

```sh
# from PyPi
pip3 install pyhirte
# or from cloned git repo
pip3 install --force dist/pyhirte-<version>-py3-none-any.whl 
```
