# Serial Device Handler
[![PyPi version][shields-pypi_version]][url-pypi_version]
[![Github Issues][shields-issues]][url-issues]

Execute commands on a device via serial port.


<br>


## Installing
Install using <a href="https://pip.pypa.io/en/stable/">pip</a>

```bash
pip install serialdevicehandler
```

or install it from <a href="https://pypi.org/project/serialdevicehandler/#files">PyPi</a>


<br>


## Example
```python
from serialdevicehandler import *

device = serialdevicehandler(port="COM10", baudrate="115200")

output = device.execute("help")

print(output)
```


<br>


## SerialDeviceHandler()
`SerialDeviceHandler()` is the core class within the library.

Syntax:

```python
device = SerialDeviceHandler(port, baudrate, timeout)
```

| argument | description | expected type | default value |
| :------- | :---------- | :------------ | :------------ |
| `port`      | Specifies the device port | `str` | COM1 |
| `baudrate`  | Specifies the device baudrate | `str` | 9600 |
| `timeout`   | Specifies the command timeout | `int` | 0.2s |

There are some attributes for statistical and other purposes.

| attribute | description | expected type | default value |
| :-------- | :---------- | :------------ | :------------ |
| `is_open`       | Indicates whether the serial port is open | `bool` | False |
| `eol_delimiter` | defines the end-of-line separator for line reading | `str` | \n |
| `total_rx`      | stores the total bytes received | `int` | 0 |
| `total_tx`      | stores the total bytes transmitted | `int` | 0 |


<br>


### SerialDeviceHandler.execute()
Use the `execute()` function to run a command.

Syntax:

```python
device.execute(command, <optional arguments>)
```

| argument | description | expected type | default value |
| :------- | :---------- | :------------ | :------------ |
| `command` | Defines the command to be executed | `str` | n/a |
| `stdout`  | Live output while the command is running | `bool` | False |
| `read_only` | read only execution | bool | False
| `write_only` | write only execution | bool | False


<br>


## Summary

- <a href="https://github.com/Salliii/conlay#serialdevicehandler">SerialDeviceHandler()</a>
  - <a href="https://github.com/Salliii/conlay#serialdevicehandlerexecute">_execute()_</a>




<!-- shields -->
[shields-pypi_version]: https://img.shields.io/pypi/v/serialdevicehandler?label=PyPi%20Version&style=for-the-badge
[shields-issues]: https://img.shields.io/github/issues/Salliii/serialdevicehandler?style=for-the-badge

<!-- url -->
[url-pypi_version]: https://pypi.org/project/serialdevicehandler/
[url-issues]: https://github.com/Salliii/serialdevicehandler/issues