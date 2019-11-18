from fuzzytable import FieldPattern
from fuzzytable import cellpatterns as cp
from datetime import datetime

int_expected_values = [
    0,
    5,
    42,
    42,
    42,
    42,
    2019,
    None,
    None,
    1,
    1,  # 1, 2, 3,
    123,
    19,
    20,
    20,
    None,
    30,
    None,
    None,
    None,
    None,
    None,
]
int_fields = FieldPattern(
    name='values',
    cellpattern=cp.Integer
)

str_expected_values = [
    '0',
    '5',
    '42',
    '42.4',
    '42.5',
    '42.6',
    '2019-10-18 00:00:00',
    'two spaces left',
    'two spaces right',
    '1',
    '(1, 2, 3)',
    '123 456 78hi',
    '19twenty3',
    '20 8',
    '20 manager',
    "hello, good bye",
    'helper 30',
    'stringofletters',
    'False',
    'True',
    '',
    '',
]
str_fields = FieldPattern(
    name='values',
    cellpattern=cp.String
)

# This test is to show that you can also pass the instantiated cellpattern as well.
str_field_instantiated = FieldPattern(
    name='values',
    cellpattern=cp.String()
)


intlist_expected_values = [
    [0],
    [5],
    [42],
    [42],
    [42],
    [42],
    [2019, 10, 18, 0, 0, 0],
    [],
    [],
    [1],
    [1, 2, 3],
    [123, 456, 78],
    [19, 3],
    [20, 8],
    [20],
    [],
    [30],
    [],
    [],
    [],
    [],
    [],
]
intlist_fields = FieldPattern(
    name='values',
    cellpattern=cp.IntegerList
)

def_excel_expected_values = [
    0,
    5,
    42,
    42.4,
    42.5,
    42.6,
    datetime(2019, 10, 18, 0, 0),
    '  two spaces left',
    'two spaces right  ',
    1,
    (1, 2, 3),
    '123 456 78hi',
    '19twenty3',
    '20 8',
    '20 manager',
    "hello, good bye",
    'helper 30',
    'stringofletters',
    False,
    True,
    None,
    None,
]
def_csv_expected_values = list(def_excel_expected_values)
def_csv_expected_values[6] = '2019-10-18 00:00:00'
def_fields = FieldPattern(
    name='values',
)


float_expected_values = [
    0.0,
    5.0,
    42.0,
    42.4,
    42.5,
    42.6,
    2019,
    None,
    None,
    1.0,
    1,  # 1, 2, 3,
    123,
    19,
    20,
    20,
    None,
    30,
    None,
    None,
    None,
    None,
    None,
]
float_fields = FieldPattern(
    name='values',
    cellpattern=cp.Float
)



if __name__ == '__main__':
    val = 'FALSE'
    _bool = bool(val)
    print(_bool)