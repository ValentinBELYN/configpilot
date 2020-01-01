<div align="center">
  <br><br>
  <img src="media/configpilot-logo.png" height="80" width="185" alt="ConfigPilot">
  <br><br>
  <p>ConfigPilot is a lightweight and powerful configuration parser for Python that automates checks and typecasting.<br>Do everything you did in fewer lines of code!</p>
  <br>
</div>

## Features
- Simple and concise syntax.
- Lightweight and fast.
- Automatic type casting.
- Automation of value checks.
- Support for primitive Python types and user-defined types.
- Support for multi-line values and lists.
- No dependency.

## Installation

The recommended way to install ConfigPilot is to use `pip3`:

```shell
$ pip3 install configpilot
```

ConfigPilot requires Python 3.6 or later.

Import ConfigPilot into your project:

```python
from configpilot import ConfigPilot, OptionSpec

# Exceptions (optional)
from configpilot import ConfigPilotError, NoSectionError, \
                        NoOptionError, IllegalValueError
```

## Examples
### 1. A simple example
#### Configuration file
```ini
# This is a comment
[author]
 name      = 'John DOE' # This is an inline comment
 age       = 27
 github    = 'https://github.com'
 skills    = 'sleep well on airplanes'
             'have a terrific family recipe for brownies'
             'always up for dessert'
```
*Quotes are optional for strings (unless you put special characters).*

For this first example, we want to retrieve:
- The `name` as a string.
- The `age` as an integer between `0` and `100`.
- The `github` option as a string.
- The `skills` as a list of strings.

To achieve this, we have to:
- Define the desired file structure.
- Instantiate a `ConfigPilot` object and indicate the structure of the file.
- Read the file and check that it does not contain any errors in terms of format or content.
- Retrieve values.

#### Python code
```python
options = [
    OptionSpec(
        section='author',
        option='name'
    ),

    OptionSpec(
        section='author',
        option='age',
        allowed=range(0, 100),
        type=int
    ),

    OptionSpec(
        section='author',
        option='github'
    ),

    OptionSpec(
        section='author',
        option='skills',
        type=[str]
    )
]

config = ConfigPilot()
config.register(*options)
config.read('/path/file.conf')

if not config.is_opened:
    print('Error: unable to read the configuration file.')
    exit(1)

if config.errors:
    print('Error: some options are incorrect.')
    exit(1)

name = config.author.name      # 'John DOE'
age = config.author.age        # 27
github = config.author.github  # 'https://github.com'
skills = config.author.skills  # ['sleep well on airplanes',
                               #  'have a terrific family recipe for brownies',
                               #  'always up for dessert']

# Alternative syntax
name = config['author']['name']
age = config['author']['age']
github = config['author']['github']
skills = config['author']['skills']
```

### 2. Use more complex types
#### Configuration file
```ini
[general]
 mode:       master
 interface:  ens33
 port:       5000
 initDelay:  0.5

[logging]
 enabled:    false

[nodes]
 slaves:     10.0.0.1
             10.0.0.2
             10.0.0.3
```

What we want to retrieve:
- The `mode` option as a string. Two values will be possible: `master` or `slave`.
- The `interface` as a string. If the option is not specified, we will use the default value `ens33`.
- The `port` as an integer between `1024` and `49151`. The default value will be `4000`.
- The `initDelay` option as a float. The default value will be `0.0`.
- The `enabled` option, from the `logging` section, as a boolean.
- The `slaves`, from the `nodes` section, as a list of `IPv4Address` (from the `ipaddress` module).

#### Python code
```python
from ipaddress import IPv4Address

options = [
    OptionSpec(
        section='general',
        option='mode',
        allowed=('master', 'slave')
    ),

    OptionSpec(
        section='general',
        option='interface',
        default='ens33'
    ),

    OptionSpec(
        section='general',
        option='port',
        allowed=range(1024, 49151),
        default=4000,
        type=int
    ),

    OptionSpec(
        section='general',
        option='initDelay',
        default=0.0,
        type=float
    ),

    OptionSpec(
        section='logging',
        option='enabled',
        type=bool
    ),

    OptionSpec(
        section='nodes',
        option='slaves',
        type=[IPv4Address]
    )
]

config = ConfigPilot()
config.register(*options)
config.read('/path/file.conf')

if not config.is_opened:
    print('Error: unable to read the configuration file.')
    exit(1)

if config.errors:
    print('Error: some options are incorrect.')
    exit(1)

mode = config.general.mode             # 'master'
interface = config.general.interface   # 'ens33'
port = config.general.port             # 5000
init_delay = config.general.initDelay  # 0.5
logs_enabled = config.logging.enabled  # False
slaves = config.nodes.slaves           # [IPv4Address('10.0.0.1'),
                                       #  IPv4Address('10.0.0.2'),
                                       #  IPv4Address('10.0.0.3')]
```

### 3. Use functions and lambda functions
#### Configuration file
```ini
[boot]
 hexCode:    0x2A

[statistics]
 lastBoot:   2020-02-01 10:27:00
 lastCrash:  2019-12-10 09:00:00
```

What we want to retrieve:
- The `hexCode` option as an integer (base 16).
- The `lastBoot` option as a `datetime` object.
- The `lastCrash` option as a `datetime` object.

We cannot set the `type` parameter of the `OptionSpec` objects to `datetime` because the constructor of `datetime` expects several parameters. The value contained in the configuration file is a string with a specific format. So, we have to process this data with a dedicated function.

#### Python code
```python
from datetime import datetime


def string_to_datetime(value):
    '''
    Cast a string to a datetime object.

    '''
    # Do not handle any exceptions that can be raised in this function.
    # They are processed by ConfigPilot: the option, which called the
    # function, is considered wrong if an exception is thrown.
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


options = [
    OptionSpec(
        section='boot',
        option='hexCode',
        type=lambda x: int(x, 16)
    ),

    OptionSpec(
        section='statistics',
        option='lastBoot',
        type=string_to_datetime
    ),

    OptionSpec(
        section='statistics',
        option='lastCrash',
        type=string_to_datetime
    )
]

config = ConfigPilot()
config.register(*options)
config.read('/path/file.conf')

if not config.is_opened:
    print('Error: unable to read the configuration file.')
    exit(1)

if config.errors:
    print('Error: some options are incorrect.')
    exit(1)

boot_hex_code = config.boot.hexCode       # 42
last_boot = config.statistics.lastBoot    # datetime.datetime(2020, 2, 1, 10, 27)
last_crash = config.statistics.lastCrash  # datetime.datetime(2019, 12, 10, 9, 0)
```

## Classes
### OptionSpec
A user-created object that represents the constraints that an option must meet to be considered valid.

#### Definition
```python
OptionSpec(section, option, allowed=None, default=None, type=str)
```

#### Parameters / Getters
- `section`

  The name of a section in the file.

  - Type: `str`

- `option`

  The name of an option in the specified section.

  - Type: `str`

- `allowed`

  The list or range of allowed values.

  - Type: `object that supports the 'in' operator (membership)`
  - Default: `None`

- `default`

  The default value of the option if it does not exist.<br>
  Must be an object of the same type as the value obtained after the cast (see the `type` parameter).

  - Type: `object`
  - Default: `None`

- `type`

  The expected value type for this option.<br>
  Set it to `int`, `float`, `bool`, `str` (default) or any other type of object.<br>
  If you expect a list of values, use instead `[int]`, `[float]`, `[bool]`, `[str]` (equivalent of `list`) or even `[MyClass]`.

  - Type: `type` or `list`
  - Default: `str`

### ConfigPilot
#### Definition
```python
ConfigPilot()
```

#### Methods
- `register(*specifications)`

  Register one or several specifications. You can call this method multiple times.<br>
  Each option in the configuration file must have its own specification. Call the `read` method next.

  - `*specifications` parameter: one or several `OptionSpec`.

- `read(filename)`

  Read and parse a configuration file according to the registered specifications.

  - `filename` parameter: the name of the configuration file to read.

#### Getters
- `filename`

  The name of the last opened file.

  - Type: `str`

- `is_opened`

  Return a boolean that indicates whether the file is opened or not.

  - Type: `bool`

- `errors`

  Return a dictionary containing sections and options that do not meet the specifications.

  - Type: `dict`

## Contributing

Comments and enhancements are welcome.

All development is done on [GitHub](https://github.com/ValentinBELYN/configpilot). Use [Issues](https://github.com/ValentinBELYN/configpilot/issues) to report problems and submit feature requests. Please include a minimal example that reproduces the bug.

## Donate

ConfigPilot is completely free and open source. It has been fully developed on my free time. If you enjoy it, please consider donating to support the development.

- [:tada: Donate via PayPal](https://paypal.me/ValentinBELYN)

## License

Copyright 2017-2020 Valentin BELYN.

Code released under the MIT license. See the [LICENSE](LICENSE) for details.
