'''
    configpilot
    ~~~~~~~~~~~

        https://github.com/ValentinBELYN/configpilot

    :copyright: Copyright 2017-2019 Valentin BELYN.
    :license: MIT, see the LICENSE for details.

    ~~~~~~~~~~~

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the 'Software'), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
    OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .exceptions import *
from re import compile


_PATTERN_SECTION    = compile(r'^\s*\[(.+?)\]\s*(?:#.*)?$')
_PATTERN_OPTION     = compile(r'^\s*([^\'"]+?)\s*[:=]'
                               r'\s*([\'"]?)(.*?)\2\s*(?:#.*)?$')
_PATTERN_VALUE_ONLY = compile(r'^\s*([\'"]?)(.+?)\1\s*(?:#.*)?$')
_PATTERN_EMPTY_LINE = compile(r'^\s*(?:#.*)?$')


def parse_section(line):
    '''
    Parse the section present in the given configuration line. Return
    the name of the section if there is one, None otherwise.

    '''
    result = _PATTERN_SECTION.match(line)

    if not result:
        return None

    return result[1]


def parse_option(line):
    '''
    Parse the option and the value present in the given configuration
    line. Return a tuple with the option and the value, None otherwise.

    If an option is found but not its value, this function returns a
    tuple with the name of the option and None as a value.

    '''
    result = _PATTERN_OPTION.match(line)

    if not result:
        return None

    option = result[1]
    value  = result[3] if result[3] else None

    return option, value


def parse_value(line):
    '''
    Parse a single value from the configuration line. Return the value
    or None if no value is found.

    '''
    result = _PATTERN_VALUE_ONLY.match(line)

    if not result:
        return None

    return result[2]


def is_section(line):
    '''
    Take a configuration line and indicate whether it is a section or
    not. Return a boolean.

    '''
    return parse_section(line) is not None


def is_option(line):
    '''
    Take a configuration line and indicate whether it is an option or
    not. Return a boolean.

    '''
    return parse_option(line) is not None


def is_value(line):
    '''
    Take a configuration line and indicate whether it is a single value
    or not. Return a boolean.

    '''
    return parse_value(line) is not None


def is_empty(line):
    '''
    Take a configuration line and indicate whether it is an empty line
    (or a comment) or not. Return a boolean.

    '''
    return _PATTERN_EMPTY_LINE.match(line) is not None


class INIParser:
    '''
    Read and parse a configuration file.

    This class implements basic operations to manipulate files with a
    structure similar to INI files, which are prevalent in the world of
    Windows and Linux.

    An INI file consists of sections and keys (also called options and
    properties). The name of a section is always surrounded by square
    brackets. Each section can contain several keys and each key must
    have at least one value. The equal ('=') or colon (':') symbol is
    used to separate a key from a value. A hash sign ('#') is used for
    comments.

    '''
    def __init__(self):
        self._filename = None
        self._config = {}

    def _parse_lines(self, lines):
        '''
        Parse the configuration.

        :type lines: list of str
        :param lines: The lines of the configuration file.

        :rtype: dict
        :returns: A dictionary containing sections, options and values.

        :raises OSError: If the file cannot be opened.
        :raises ParseError: If the file does not have a valid
            structure.

        '''
        section = None
        option = None
        config = {}
        values = []

        for line in lines:
            # We ignore empty lines and comments that do not provide
            # any information. Inline comments are not processed at
            # this stage.
            if is_empty(line):
                pass

            # A section is surrounded by square brackets. We get its
            # name. We raise an error if the section already exists.
            elif is_section(line):
                if option and not values:
                    raise MissingValueError(section, option)

                section = parse_section(line)
                option = None

                if section in config:
                    raise DuplicateSectionError(section)

                config[section] = {}

            # An option must be in a section. We raise an error if it
            # is not the case. We also raise an error if the option is
            # defined more than once in the same section.
            elif is_option(line):
                if not section:
                    raise MissingSectionHeaderError

                if option and not values:
                    raise MissingValueError(section, option)

                option, value = parse_option(line)
                values = []

                if option in config[section]:
                    raise DuplicateOptionError(section, option)

                config[section][option] = values

                # If the current line contains a value, we add it
                if value: values.append(value)

            # The multivalued options are handled here. If a value is
            # not preceded by the name of an option, we add it to the
            # current option. We raise an error if no section or
            # option has been defined before.
            elif is_value(line):
                if not section:
                    raise MissingSectionHeaderError

                if not option:
                    raise MissingOptionError(section)

                value = parse_value(line)
                values.append(value)

        return config

    def read(self, filename):
        '''
        Read and parse a configuration file.

        :type filename: str
        :param filename: The path of the file to read.

        :raises OSError: If the file cannot be opened.
        :raises ParseError: If the file does not have a valid
            structure.

        '''
        self._filename = filename
        self._config = {}

        with open(filename) as file:
            lines = file.readlines()

        self._config = self._parse_lines(lines)

    def has_section(self, section):
        '''
        Return whether the given section exists.

        '''
        return section in self._config

    def has_option(self, section, option):
        '''
        Return whether the given section and option exist.

        '''
        return (section in self._config and
                option in self._config[section])

    def get(self, section, option, default=None):
        '''
        Get the value corresponding to the section and option passed as
        parameters. Return the default value if the option is not
        found.

        This method always returns the value(s) in a list.

        '''
        if self.has_option(section, option):
            return self._config[section][option]

        return default

    @property
    def filename(self):
        '''
        The name of the last opened file.

        '''
        return self._filename
