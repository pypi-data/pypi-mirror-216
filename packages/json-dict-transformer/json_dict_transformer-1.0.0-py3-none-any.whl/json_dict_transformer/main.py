def getDictfield(data, field):
    """
    Get value from dict field using dot notation
    """

    fields = field.split(".")
    result = data

    for f in fields:
        if isinstance(result, dict) and f in result:
            result = result[f]
        else:
            raise Exception(f"Field {field} not found")

    if isinstance(result, str):
        return result
    elif isinstance(result, int):
        return str(result)
    elif isinstance(result, list):
        return ",".join(result)
    else:
        raise Exception(f"Unknown type {type(result)} for {field}")


def translateDictToDict(input: dict, schema: dict) -> dict:
    """
    Create output dict from input dict using schema dict as template.
    This function is recursive.
    """

    # Shallow copy of schema
    output = schema.copy()

    # Iterate over output dict and replace the proper values
    for k, v in output.items():
        if isinstance(v, dict):
            # Go deeper
            translateDictToDict(v)
        elif isinstance(v, list):
            # Override list to empty string as preparation for replacing
            output[k] = "" # the same as "v", but "v" is used for iteration

            for item in v:
                # Recognized format: <type>::<value>
                # Remember about double colon!
                item_type, item_value = item.split("::")

                if item_type == "json":
                    # Extract the proper field from input dict
                    input_field_value = getDictfield(input, item_value)
                    # Concatenate the value to the output
                    output[k] = output[k] + input_field_value

                elif item_type == "txt":
                    output[k] = output[k] + item_value

                else:
                    raise Exception(f"Unknown type {item_type} for {item_value}")

            # Remove leading and trailing whitespaces
            output[k] = output[k].strip()
        else:
            # Skip all values other than dict and list
            pass

    return output
