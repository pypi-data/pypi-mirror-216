# json-dict-transformer


This package helps transform an input JSON (as Python `dict`) into another
JSON (also `dict`) using provided schema.

The main goal behind this package was to enable proxying requests between
two systems. The first returns JSON data, which can be transformed and sent
to the second system.

Transforming is understood as changing the structure of JSON data.
For example, splitting some fields or concatenating fields into other fields.
In other words, it is a process of reformatting JSON data preserving values
but changing the structure.


## Example

```python
from json_dict_transformer import translateDictToDict

input_dict = {
    "name": "John",
    "surname": "Doe",
    "age": 30,
    "address": {
        "street": "Main Street",
        "number": 123,
        "city": "New York",
        "country": "USA"
    },
    "hobbies": [
        "football",
        "basketball",
        "tennis"
    ]
}

schema_dict = {
    "full name": ["json::name", "txt:: ", "json::surname"],
    "age": ["json::age"],
    "address": [
        "json::address.street",
        "txt::,",
        "json::address.number",
        "txt::,",
        "json::address.city",
        "txt::,",
        "json::address.country"
    ],
    "hobbies": [
        "txt::My hobbies are: ",
        "json::hobbies"
    ]
}

output_dict = translateDictToDict(input_dict, schema_dict)
print(output_dict)
```

Input dict:
```
{
  'name': 'John',
  'surname': 'Doe',
  'age': 30,
  'address': {
    'street': 'Main Street',
    'number': 123,
    'city': 'New York',
    'country': 'USA'
  },
  'hobbies': [
    'football',
    'basketball',
    'tennis'
  ]
}
```

Output dict:
```
{
  'full name': 'John Doe',
  'age': '30',
  'address': 'Main Street,123,New York,USA',
  'hobbies': 'My hobbies are: football,basketball,tennis'
}
```

## Installation

Install the package using PIP:
```sh
pip install json_dict_transformer
# or
pip install git+https://github.com/thevops/json-dict-transformer.git@master
```

## Usage

### Input data format

The package needs data in Python `dict` format. You can convert JSON into `dict`
using the following code:

```python
import json

with open('data.json') as json_file:
    data = json.load(json_file)

print(type(data)) # it should return type `dict`
```

### Selectors

The schema for mapping uses selectors to point to specific fields.
For now, there are only 2 available selectors.

`json::<field path>`

The selector extracts data from a field. A path is built using dot
notation. Please, take a look at the above example.


`txt::<string>`

The selector adds a string. It can be used to add a splitter or
any other text to the output data.


## Similar projects

- https://github.com/Onyo/jsonbender
- https://github.com/ebi-ait/json-converter
