# Add parent directory to path to be able to import json_transformer
import sys
sys.path.append('../')
# The above part can be omitted if json_transformer is installed as a package


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
