import ast
import inspect
import re
import json
import copy
from typing import Type
from xia_fields import BaseField, StringField, IntField, FloatField, BooleanField


class PythonCompiler:
    field_dict = {
        "integer": IntField,
        "number": FloatField,
        "string": StringField,
        "boolean": BooleanField
    }

    @classmethod
    def _to_snake(cls, input_string: str):
        output_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', output_string).lower()

    @classmethod
    def _to_upper_camel(cls, input_string: str):
        parts = input_string.replace('-', '_').split('_')
        if len(parts) > 1:
            return ''.join([part.capitalize() for part in parts])
        elif input_string:
            return input_string[0].upper() + input_string[1:]
        else:
            return input_string

    @classmethod
    def _to_camel(cls, input_string: str):
        upper_camel = cls._to_upper_camel(input_string)
        if upper_camel:
            return upper_camel[0].lower() + upper_camel[1:]
        else:
            return upper_camel

    @classmethod
    def ast_to_dict(cls, node):
        """Parsed AST to python dictionary

        Args:
            node: AST node

        Returns:

        """
        if isinstance(node, ast.AST):
            node_dict = {attr: cls.ast_to_dict(getattr(node, attr)) for attr in node._fields}
            node_dict['type'] = node.__class__.__name__
            return node_dict
        elif callable(node):
            # For callable objects (functions), serialize the source code
            source_code = inspect.getsource(node)
            return {"type": "function", "code": source_code}
        elif isinstance(node, list):
            return [cls.ast_to_dict(child) for child in node]
        else:
            return node

    @classmethod
    def dict_to_ast(cls, node_dict: dict):
        """Reconstruct AST by using node dictionary

        Args:
            node_dict: dictionary of node descriptions

        Returns:
            AST Tree
        """
        if isinstance(node_dict, dict) and 'type' in node_dict:
            if node_dict['type'] == 'function':
                # For functions, compile the source code to a code object and then convert it to a function object
                code = compile(node_dict['code'], '<string>', 'exec')
                namespace = {}
                exec(code, namespace)
                return namespace[node_dict['code'].split(' ', 2)[1].split('(', 1)[0]]
            else:
                class_ = getattr(ast, node_dict['type'])
                node_dict = {k: cls.dict_to_ast(v) for k, v in node_dict.items() if k != 'type'}
                return ast.fix_missing_locations(class_(**node_dict))
        elif isinstance(node_dict, list):
            return [cls.dict_to_ast(child) for child in node_dict]
        else:
            return node_dict

    @classmethod
    def code_to_dict(cls, code: str) -> dict:
        """Python Source Code to python dictionary

        Args:
            code: source code of model

        Returns:
            dictionary of parsed code
        """
        tree = ast.parse(code)
        ast.fix_missing_locations(tree)
        tree_dict = cls.ast_to_dict(tree)
        return tree_dict

    @classmethod
    def dict_to_code(cls, tree_dict: dict) -> str:
        """python dictionary convert back to Python Source Code

        Args:
            tree_dict: AST in dictionary mode

        Returns:
            source code
        """
        tree = cls.dict_to_ast(tree_dict)
        code = ast.unparse(tree)
        return code

    @classmethod
    def module_to_dict(cls):
        base_code = """from xia_fields import StringField, IntField, FloatField, BooleanField
from xia_engine import EmbeddedDocument, Document, EmbeddedDocumentField, ListField
        """
        base_dict = cls.code_to_dict(base_code)
        return base_dict

    @classmethod
    def data_model_to_dict(cls, model_name: str, base_name: str, key_fields: list = None):
        base_code = """class A(B):
    _key_fields = ["1", "2"]
        """
        key_fields = [] if not key_fields else key_fields
        base_dict = cls.code_to_dict(base_code)["body"][0]
        base_dict["name"] = model_name
        base_dict["bases"][0]["id"] = base_name
        if key_fields:
            key_item = base_dict["body"][0]["value"]["elts"][0]
            key_items = base_dict["body"][0]["value"]["elts"] = []
            for key_field in key_fields:
                new_item = key_item.copy()
                new_item["value"] = key_field
                key_items.append(new_item)
        else:
            base_dict["body"] = []
        return base_dict

    @classmethod
    def field_parameters_to_dict(cls, field_parameters: dict):
        base_code = """class A:
    field: str = StringField(description="Test")
            """
        keywords = []
        keyword_example = cls.code_to_dict(base_code)["body"][0]["body"][0]["value"]["keywords"][0]
        for key, value in field_parameters.items():
            current_keyword = copy.deepcopy(keyword_example)
            current_keyword["arg"] = key
            current_keyword["value"]["value"] = value
            keywords.append(current_keyword)
        return keywords

    @classmethod
    def simple_field_to_dict(cls, field_name: str, field_class: Type[BaseField], field_parameters: dict):
        base_code = """class A:
    field: str = StringField(description="Test")
        """
        base_dict = cls.code_to_dict(base_code)["body"][0]["body"][0]
        base_dict["target"]["id"] = field_name
        base_dict["annotation"]["id"] = field_class.internal_form.__name__
        base_dict["value"]["func"]["id"] = field_class.__name__
        base_dict["value"]["keywords"] = cls.field_parameters_to_dict(field_parameters)
        return base_dict

    @classmethod
    def embedded_field_to_dict(cls, field_name: str, document_type_name: str, field_parameters: dict):
        base_code = """class A:
    status: object = EmbeddedDocumentField(document_type=Status)
        """
        base_dict = cls.code_to_dict(base_code)["body"][0]["body"][0]
        base_dict["target"]["id"] = field_name
        base_dict["value"]["keywords"][0]['value']['id'] = document_type_name
        base_dict["value"]["keywords"].extend(cls.field_parameters_to_dict(field_parameters))
        return base_dict

    @classmethod
    def list_field_to_dict(cls, field_name: str, field_class: Type[BaseField],
                           list_parameters: dict, field_parameters: dict):
        base_code = """class A:
    status_list: list = ListField(CompressedStringField())
        """
        base_dict = cls.code_to_dict(base_code)["body"][0]["body"][0]
        base_dict["target"]["id"] = field_name
        base_dict["value"]["keywords"] = cls.field_parameters_to_dict(list_parameters)
        base_dict["value"]["args"][0]["func"]["id"] = field_class.__name__
        base_dict["value"]["args"][0]["keywords"] = cls.field_parameters_to_dict(field_parameters)
        return base_dict

    @classmethod
    def list_embedded_field_to_dict(cls, field_name: str, document_type_name: str,
                                    list_parameters: dict, field_parameters: dict):
        base_code = """class A:
    status_list: list = ListField(EmbeddedDocumentField(document_type=Status))
        """
        base_dict = cls.code_to_dict(base_code)["body"][0]["body"][0]
        base_dict["target"]["id"] = field_name
        base_dict["value"]["keywords"] = cls.field_parameters_to_dict(list_parameters)
        base_dict["value"]["args"][0]["keywords"][0]['value']['id'] = document_type_name
        base_dict["value"]["args"][0]["keywords"].extend(cls.field_parameters_to_dict(field_parameters))
        return base_dict

    @classmethod
    def get_field_parameters(cls, field_schema):
        field_params = {}
        for param_name in ["description", "default"]:
            if field_schema.get(param_name, None):
                field_params[param_name] = field_schema[param_name]
        if len(field_schema.get("examples", [])) > 0:
            field_params["sample"] = field_schema["examples"][0]
        elif field_schema.get("example", None):
            field_params["sample"] = field_schema["example"]
        if field_schema.get("minimum", None):
            field_params["value_min"] = field_schema["minimum"]
        if field_schema.get("maximum", None):
            field_params["value_max"] = field_schema["maximum"]
        if field_schema.get("pattern", None):
            field_params["regex"] = field_schema["pattern"]
        if field_schema.get("minLength", None):
            field_params["min_length"] = field_schema["minLength"]
        if field_schema.get("maxLength", None):
            field_params["max_length"] = field_schema["maxLength"]
        if field_schema.get("enum", None):
            field_params["choices"] = field_schema["enum"]
        if field_schema.get("required_field", None):
            field_params["required"] = field_schema["required_field"]
        return field_params

    @classmethod
    def _assign_required(cls, required_list: list, model_schema: dict):
        for required_field in required_list:
            if required_field in model_schema["properties"]:
                model_schema["properties"][required_field]["required_field"] = True

    @classmethod
    def _assign_default(cls, default_dict: dict, model_schema: dict):
        for field_name, default_value in default_dict.items():
            if field_name in model_schema["properties"]:
                model_schema["properties"][field_name]["default"] = default_value

    @classmethod
    def generate_model(cls, model_name: str, base_name: str, json_schema: dict,
                       is_embedded: bool = False, key_fields: list = None) -> dict:
        """Generate code structure dictionary for a given model

        Args:
            model_name: Model Name
            base_name: Parent Class Name, typically Document or EmbeddedDocument
            json_schema: json schema
            is_embedded: Is embedded
            key_fields: key fields list

        Returns:
            Code structure dictionary
        """
        model_dict = cls.data_model_to_dict(cls._to_upper_camel(model_name), base_name, key_fields=key_fields)
        model_schema = json_schema["definitions"][model_name] if is_embedded else json_schema
        cls._assign_required(model_schema.pop("required", []), model_schema)
        cls._assign_default(model_schema.pop("default", {}), model_schema)
        for field_name, field_schema in model_schema["properties"].items():
            field_type = field_schema.pop('type', None)
            field_name = cls._to_snake(field_name)
            if field_type in cls.field_dict:
                # Case 1: Simple Field
                field_class = cls.field_dict[field_type]
                field_params = cls.get_field_parameters(field_schema)
                model_dict["body"].append(cls.simple_field_to_dict(
                    field_name, field_class, field_params
                ))
            elif "$ref" in field_schema:
                # Case 2: Embedded Field
                embedded_name = field_schema.pop("$ref").split("/")[-1]
                embedded_schema = json_schema["definitions"][embedded_name]
                field_params = cls.get_field_parameters(embedded_schema)
                model_dict["body"].append(cls.embedded_field_to_dict(
                    field_name, cls._to_upper_camel(embedded_name), field_params
                ))
            elif field_type == "array":
                item_schema = field_schema.pop("items")
                item_type = item_schema.pop('type', None)
                list_params = cls.get_field_parameters(field_schema)
                if item_type in cls.field_dict:
                    # Case 3: List of Simple Field
                    field_class = cls.field_dict[item_type]
                    field_params = cls.get_field_parameters(item_schema)
                    model_dict["body"].append(cls.list_field_to_dict(
                        field_name, field_class, list_params, field_params
                    ))
                elif "$ref" in item_schema:
                    embedded_name = item_schema.pop("$ref").split("/")[-1]
                    embedded_schema = json_schema["definitions"][embedded_name]
                    field_params = cls.get_field_parameters(embedded_schema)
                    model_dict["body"].append(cls.list_embedded_field_to_dict(
                        field_name, cls._to_upper_camel(embedded_name), list_params, field_params)
                    )
        return model_dict

    @classmethod
    def generate_python(cls, model_name: str, json_schema: dict, key_fields: list = None) -> str:
        """Using json schema and json data to reconstruct data model

        Args:
            model_name: Name of Model
            json_schema: Json schema definition
            key_fields: key fields list:
                * Value None = auto-generate key fields (1 items of json schema)
                * Value [] = no key fields

        Returns:
            Python code
        """
        module_dict = cls.module_to_dict()
        embedded_dict, dependencies_dict = {}, {}
        definitions = json_schema.get("definitions", {})
        if key_fields is None:
            key_fields = [cls._to_snake(list(json_schema["properties"])[0])]
        model_dict = cls.generate_model(model_name, "Document", json_schema, key_fields=key_fields)
        for embedded_name, embedded_schema in definitions.items():
            dependencies_dict[embedded_name] = re.findall(r'"#/definitions/(.*?)"', json.dumps(embedded_schema))
        while dependencies_dict and any(not dep for dep in dependencies_dict.values()):
            for embedded_name in [embedded for embedded in dependencies_dict if not dependencies_dict[embedded]]:
                embedded_dict[embedded_name] = cls.generate_model(embedded_name, "EmbeddedDocument", json_schema, True)
                for key, dependencies in dependencies_dict.items():
                    dependencies_dict[key] = [dep for dep in dependencies if dep != embedded_name]
                dependencies_dict.pop(embedded_name)
        module_dict["body"].extend(embedded_dict.values())
        module_dict["body"].append(model_dict)
        return cls.dict_to_code(module_dict)
