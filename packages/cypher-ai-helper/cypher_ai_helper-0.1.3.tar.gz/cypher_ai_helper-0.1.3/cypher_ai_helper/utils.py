"""
Helper functions for Cypher AI
"""
from typing import Union, Type, Any, get_type_hints

from pydantic import BaseModel

import functools
import inspect
import re


def pydantic_model_to_str(model: Union[BaseModel, Type[BaseModel]]) -> str:
    """
    Converts a pydantic model to a string representation of the class definition

    :param model:
    :return:
    """

    def get_field_def(name, field_info) -> str:
        """
        Returns a string representation of a field definition

        :param name:
        :param field_info:
        :return:
        """
        default = field_info.default if not field_info.required else "..."
        description = field_info.field_info.description
        if description:
            description = ', description="' + description.replace("\n", " ") + '"'
        else:
            description = ""
        return f'{name}: {field_info.outer_type_.__name__} = Field({default}{description})'

    fields = [get_field_def(name, field_info) for name, field_info in model.__fields__.items()]

    docstring = f'"""\n{model.__doc__}\n"""' if model.__doc__ else ""
    class_def = f'class {model.__name__}(BaseModel):\n{docstring}'
    class_fields = '\n'.join([f'    {line}' for line in fields])
    return f'{class_def}\n{class_fields}'


def pydantic_models_to_str(models: list[Union[BaseModel, Type[BaseModel]]]) -> str:
    """
    Converts a list of pydantic models to a string representation of the class definitions
    :param models:
    :return:
    """
    return '\n\n'.join([pydantic_model_to_str(model) for model in models])


def class_definition_in_str_for_dataclasses(model: Any) -> str:
    """
    Creates schema for dataclass

    :param model:
    :return:
    """
    fields = ', '.join([f'{name}: {field_type.__name__}'
                        for name, field_type in get_type_hints(model).items()])

    docstring = f'"""\n{model.__doc__}\n"""' if model.__doc__ else ""
    class_def = f'@dataclasses.dataclass\nclass {model.__name__}:\n{docstring}'
    class_fields = '\n'.join([f'    {line}' for line in fields.split(', ')])
    return f'{class_def}\n{class_fields}'


# Below functions are taken from: https://github.com/amikos-tech/funkagent/blob/feature/partials/funkagent/parser.py


def type_mapping(dtype: type) -> str:
    """
    Maps python types to OpenAPI types

    :param dtype:
    :return:
    """
    if dtype == float:
        return "number"
    elif dtype == int:
        return "integer"
    elif dtype == str:
        return "string"
    else:
        return "string"


def extract_params(doc_str: str) -> dict[str, str]:
    """
    Extracts parameters from docstring
    :param doc_str:
    :return:
    """
    # split doc string by newline, skipping empty lines
    params_str = [line for line in doc_str.split("\n") if line.strip()]
    params = {}
    for line in params_str:
        # we only look at lines starting with ':param'
        if line.strip().startswith(':param'):
            param_match = re.findall(r'(?<=:param )\w+', line)
            if param_match:
                param_name = param_match[0]
                desc_match = line.replace(f":param {param_name}:", "").strip()
                # if there is a description, store it
                if desc_match:
                    params[param_name] = desc_match
    return params


def func_to_json(func) -> dict[str, Any]:
    """
    Converts a function to a json schema for OpenAI

    :param func:
    :return:
    """
    # Check if the function is a functools.partial
    if isinstance(func, functools.partial) or isinstance(func, functools.partialmethod):
        fixed_args = func.keywords
        _func = func.func
    else:
        fixed_args = {}
        _func = func

    # first we get function name
    func_name = _func.__name__
    # then we get the function annotations
    argspec = inspect.getfullargspec(_func)
    # get the function docstring
    func_doc = inspect.getdoc(_func)
    # parse the docstring to get the description
    func_description = ''.join([line for line in func_doc.split("\n") if not line.strip().startswith(':')])
    # parse the docstring to get the descriptions for each parameter in dict format
    param_details = extract_params(func_doc) if func_doc else {}
    # attach parameter types to params and exclude fixed args
    # get params
    params = {}
    for param_name in argspec.args:
        if param_name not in fixed_args.keys():
            params[param_name] = {
                "description": param_details.get(param_name) or "",
                "type": type_mapping(argspec.annotations.get(param_name, type(None)))
            }
    # calculate required parameters excluding fixed args
    # _required = [arg for arg in argspec.args if arg not in fixed_args]
    _required = [i for i in argspec.args if i not in fixed_args.keys()]
    if inspect.getfullargspec(_func).defaults:
        _required = [argspec.args[i] for i, a in enumerate(argspec.args) if
                     argspec.args[i] not in inspect.getfullargspec(_func).defaults and argspec.args[
                         i] not in fixed_args.keys()]
    # then return everything in dict
    return {
        "name": func_name,
        "description": func_description,
        "parameters": {
            "type": "object",
            "properties": params
        },
        "required": _required
    }
