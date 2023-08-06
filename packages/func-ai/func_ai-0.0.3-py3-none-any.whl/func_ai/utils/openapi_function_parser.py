""" doc """
import requests
import json


def get_spec_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception in case of a failure
    return response.json()


def get_operations_from_path_item(path_item):
    http_methods = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]
    operations = [op_spec for op, op_spec in path_item.items() if op in http_methods]
    return operations


def get_operation_details(operation):
    name = operation.get('operationId')
    description = operation.get('description')
    parameters = operation.get('parameters')

    return {
        "name": name,
        "description": description,
        "parameters": parameters
    }


def parse_parameters(parameters):
    params_dict = {"type": "object", "properties": {}, "required": []}

    for param in parameters:
        name = param['name']
        description = param.get('description', '')  # TODO generate a description if not present
        param_type = param['schema'].get('type', 'string') if 'schema' in param else 'string'
        #TODO if parameter is schema then
        params_dict["properties"][name] = {
            "description": description,
            "type": param_type
        }

        if param.get('required', False):
            params_dict["required"].append(name)

    return params_dict


def get_func_details(operation):
    name = operation.get('name')
    description = operation.get('description')  # TODO if description not present generate one with AI
    parameters = operation.get('parameters', [])

    # Parse the parameters
    parameters = parse_parameters(parameters)

    return {
        "name": name,
        "description": description,
        "parameters": parameters
    }


def parse_spec(spec):
    paths = spec['paths']
    for path, path_item in paths.items():
        operations = get_operations_from_path_item(path_item)
        for operation in operations:
            details = get_operation_details(operation)
            print(details)
            print(json.dumps(get_func_details(details), indent=2))


if __name__ == '__main__':
    spec = get_spec_from_url('http://petstore.swagger.io/v2/swagger.json')
    parse_spec(spec)
