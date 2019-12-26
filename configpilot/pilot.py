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

from .parsers import INIParser
from .models import Section, Option
from .exceptions import ParseError, NoSectionError
from .utils import magic_cast


class ConfigPilot:
    '''
    A lightweight and powerful configuration parser for Python that
    automates checks and typecasting.

    Do everything you did in fewer lines of code.

    Usage::

        # # file.conf
        #
        # [general]
        #  mode      = master
        #  interface = ens33
        #  port      = 5000
        #
        # [nodes]
        #  slaves    = 10.0.0.1
        #              10.0.0.2
        #              10.0.0.3

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

        mode = config.general.mode
        interface = config.general.interface
        port = config.general.port
        slaves = config.nodes.slaves

        # Alternative syntax
        mode = config['general']['mode']

    See the OptionSpec class for details.

    '''
    def __init__(self):
        self._filename = None
        self._is_opened = False
        self._specifications = []
        self._config = {}
        self._errors = {}

    def __repr__(self):
        return f'<ConfigPilot [{self._filename}]>'

    def __len__(self):
        '''
        Return the number of sections contained in the file.

        '''
        return len(self._config)

    def __getattr__(self, name):
        '''
        Get the specified section.

        :raises NoSectionError: If the section is not found in the
            configuration file.

        '''
        if name[:2] == '__':
            return super().__getattr__(name)

        if name[-1] == '_':
            name = name[:-1]

        return self[name]

    def __getitem__(self, key):
        '''
        Get the specified section.

        :raises NoSectionError: If the section is not found in the
            configuration file.

        '''
        if key not in self._config:
            raise NoSectionError(key)

        return self._config[key]

    def _get_section(self, name):
        if name not in self._config:
            self._config[name] = Section(name)

        return self._config[name]

    def _add_error(self, section, option):
        if section not in self._errors:
            self._errors[section] = []

        self._errors[section].append(option)

    def register(self, *specifications):
        '''
        Register one or several specifications. You can call this
        method multiple times.

        Each option in the configuration file must have its own
        specification. Call the 'read' method next.

        '''
        self._specifications.extend(specifications)

    def read(self, filename):
        '''
        Read and parse a configuration file according to the registered
        specifications.

        '''
        parser = INIParser()
        self._filename = filename
        self._is_opened = False
        self._config = {}
        self._errors = {}

        try:
            parser.read(filename)

        except (OSError, ParseError):
            return self._is_opened

        for spec in self._specifications:
            # We get the value(s) corresponding to the specification.
            # This method always returns the value(s) in a list.
            values = parser.get(
                section=spec.section,
                option=spec.option)

            # If the configuration file contains a value, we cast it
            # into the desired type and we verify that it is within the
            # specified range.
            if values:
                try:
                    casted_value = magic_cast(
                        *values,
                        expected_type=spec.type)

                    if (spec.allowed and
                        casted_value not in spec.allowed):
                        raise ValueError

                except Exception:
                    casted_value = None

                    self._add_error(
                        section=spec.section,
                        option=spec.option)

            # If no option is provided in the file and a default value
            # is set, we use this value.
            elif spec.default:
                casted_value = spec.default

            # If no option is provided and no default value is defined,
            # we add an error to the option.
            else:
                self._add_error(
                    section=spec.section,
                    option=spec.option)
                continue

            option = Option(
                name=spec.option,
                value=casted_value,
                specification=spec)

            section = self._get_section(spec.section)
            section.add(option)

        self._is_opened = True
        return self._is_opened

    @property
    def filename(self):
        '''
        The name of the last opened file.

        '''
        return self._filename

    @property
    def is_opened(self):
        '''
        Return a boolean that indicates whether the file is opened or
        not.

        '''
        return self._is_opened

    @property
    def errors(self):
        '''
        Return a dictionary containing sections and options that do not
        meet the specifications.

        '''
        return self._errors
