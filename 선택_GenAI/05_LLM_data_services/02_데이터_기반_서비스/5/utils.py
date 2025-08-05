from typing import Any


def type_to_json_schema(type_: Any) -> dict:
    """Converts a Python type to a JSON schema object."""
    base_types = {
        str: {"type": "string"},
        int: {"type": "number"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
    }

    if type_ in base_types:
        return base_types[type_]

    # Handle list types
    if hasattr(type_, "__origin__") and type_.__origin__ is list:
        item_type = type_.__args__[0]  # Get the type of items in the list
        return {"type": "array", "items": type_to_json_schema(item_type)}

    # Handle dict types
    if hasattr(type_, "__origin__") and type_.__origin__ is dict:
        return {
            "type": "object",
        }

    return {"type": "string"}


def parse_docstring(docstring: str) -> dict:
    """Parses a function's docstring to extract parameter descriptions."""
    doc_lines = docstring.splitlines()
    doc_lines = [line.strip() for line in doc_lines if line.strip() != ""]

    func_desc = ""
    for i in range(len(doc_lines)):
        if doc_lines[i].startswith("Args:"):
            break
        func_desc += doc_lines[i]

    param_desc = {}
    last_name = ""
    for line in doc_lines[i + 1 :]:
        if line.lower().startswith("returns:"):
            break
        if ":" in line:
            param_name, rest = line.split(":", 1)
            param_name = param_name.strip()
            if "(" in param_name:
                param_name = param_name.split("(")[0].strip()
            param_desc[param_name] = rest.strip()
            last_name = param_name
        else:
            param_desc[last_name] += " " + line

    return {"description": func_desc, "parameters": param_desc}


def function_to_json_schema(func) -> dict:
    """Generates a JSON schema from a function's annotations and docstring."""

    # Get the function's annotations and docstring
    annotations = func.__annotations__
    docstring = parse_docstring(func.__doc__ or "")
    func_info = {
        "name": func.__name__,
        "description": docstring.get("description", ""),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    }

    # Generate JSON schema for each parameter
    for param_name, param_type in annotations.items():
        if param_name == "return":
            continue
        param_info = {
            "description": docstring["parameters"].get(param_name, "")
        }
        param_info.update(type_to_json_schema(param_type))
        func_info["parameters"]["properties"][param_name] = param_info
        func_info["parameters"]["required"].append(param_name)

    return {"type": "function", "function": func_info}
