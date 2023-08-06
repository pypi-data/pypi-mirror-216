import dataclasses
from typing import _GenericAlias


def get_defaults_if_dataclass(hub, param) -> dict:
    # Return dictionary with the default values for a dataclass argument
    # Otherwise an empty dictionary
    param_structure_with_defaults = {}
    if dataclasses.is_dataclass(param.annotation):
        _annotation_recursive(param_structure_with_defaults, param.annotation)
    elif (
        isinstance(param.annotation, _GenericAlias)
        and isinstance(param.annotation.__args__, tuple)
        and dataclasses.is_dataclass(param.annotation.__args__[0])
    ):
        _annotation_recursive(
            param_structure_with_defaults, param.annotation.__args__[0]
        )

    return param_structure_with_defaults


def populate_default_values(hub, default_vals: dict, value):
    # Recursive method to set default values in an argument
    # of type dataclass
    if default_vals is None:
        return

    if isinstance(value, list):
        for elem in value:
            for arg_name, arg_value in default_vals.items():
                if arg_value is None:
                    continue
                if not elem.get(arg_name) and not isinstance(arg_value, dict):
                    elem[arg_name] = arg_value
                elif isinstance(arg_value, dict):
                    populate_default_values(hub, arg_value, elem[arg_name])
    else:
        for arg_name, arg_value in default_vals.items():
            if arg_value is None:
                continue
            if not value.get(arg_name) and not isinstance(arg_value, dict):
                value.update({arg_name: arg_value})
            elif isinstance(arg_value, dict):
                populate_default_values(hub, arg_value, value[arg_name])


def _annotation_recursive(defaults, param_annotation):
    # Populate the default values of an argument of type dataclass
    # from the parameter annotation
    for field in dataclasses.fields(param_annotation):
        if dataclasses.is_dataclass(field.type):
            defaults[field.name] = {}
            _annotation_recursive(defaults[field.name], field.type)
        else:
            defaults[field.name] = field.default
