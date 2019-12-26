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


class ParseError(Exception):
    '''
    Base class for parsing exceptions.

    '''


class MissingSectionHeaderError(ParseError):
    '''
    Raised when a configuration file does not begin with a section.

    '''
    def __init__(self):
        message = 'The configuration file contains no section headers'
        super().__init__(message)


class MissingOptionError(ParseError):
    '''
    Raised when a section does not begin with an option.

    '''
    def __init__(self, section):
        message = f'The \'{section}\' section does not begin with ' \
                   'an option'
        super().__init__(message)


class MissingValueError(ParseError):
    '''
    Raised when no value is assigned to an option.

    '''
    def __init__(self, section, option):
        message = f'No value found for the \'{option}\' option in ' \
                  f'the \'{section}\' section'
        super().__init__(message)


class DuplicateSectionError(ParseError):
    '''
    Raised when the same section is defined multiple times in a
    configuration file.

    '''
    def __init__(self, section):
        message = f'The \'{section}\' section already exists'
        super().__init__(message)


class DuplicateOptionError(ParseError):
    '''
    Raised when the same option is defined multiple times in a section.

    '''
    def __init__(self, section, option):
        message = f'The \'{option}\' option already exists in ' \
                  f'the \'{section}\' section'
        super().__init__(message)


class ConfigPilotError(Exception):
    '''
    Base class for ConfigPilot exceptions.

    '''


class NoSectionError(ConfigPilotError):
    '''
    Raised when the requested section is not found in the configuration
    file.

    '''
    def __init__(self, section):
        message = f'The \'{section}\' section was not found'
        super().__init__(message)


class NoOptionError(ConfigPilotError):
    '''
    Raised when the requested option is not found in the configuration
    file.

    '''
    def __init__(self, section, option):
        message = f'The \'{option}\' option (from the \'{section}\' ' \
                   'section) was not found'
        super().__init__(message)


class IllegalValueError(ConfigPilotError):
    '''
    Raised when the requested option does not meet the constraints
    defined by the developer.

    '''
    def __init__(self, section, option):
        message = f'The \'{option}\' option (from the \'{section}\' ' \
                   'section) does not meet the constraints defined ' \
                   'by the OptionSpec object'
        super().__init__(message)
