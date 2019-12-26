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


def cast_to_boolean(value):
    '''
    Cast a string to a boolean. Raise a TypeError exception if the
    given value cannot be casted.

    Case insensitive.

    '''
    value = value.lower()

    boolean_states = {
        'true': True,
        'false': False
    }

    if value in boolean_states:
        return boolean_states[value]

    raise TypeError


def cast_value(value, expected_type):
    '''
    Cast a value (preferably a string) in the specified type. Raise an
    exception (depending on the type passed in parameters) if the value
    cannot be casted.

    '''
    if expected_type is bool:
        expected_type = cast_to_boolean

    return expected_type(value)


def cast_values(values, expected_type):
    '''
    Cast the values (preferably strings) of a list in the specified
    type. Raise an exception (depending on the type passed in
    parameters) if a value cannot be casted.

    '''
    if expected_type is bool:
        expected_type = cast_to_boolean

    return [
        expected_type(value)
        for value in values
    ]


def magic_cast(*values, expected_type):
    '''
    Cast any value (preferably strings) in the specified type, whether
    it is a single value or a list of values. Raise an exception
    (depending on the type passed in parameters) if a value cannot be
    casted.

    Usage::

        # Cast strings to a list of integers
        >>> magic_cast('1', '2', '3', expected_type=[int])
        [1, 2, 3]

        # Cast a string to an integer
        >>> magic_cast('1', expected_type=int)
        1

        # Cast a string to a boolean
        >>> magic_cast('true', expected_type=bool)
        True

    '''
    if (expected_type is list or
        expected_type == []):
        expected_type = [str]

    if isinstance(expected_type, list):
        return cast_values(values, expected_type[0])

    if len(values) == 1:
        return cast_value(values[0], expected_type)

    raise TypeError
