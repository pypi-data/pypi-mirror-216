from typing import Type, List, Dict
import re
import os
import json
from inspect import signature
from xia_fields import BaseField
from xia_fields import BooleanField, DoubleField, FloatField, StringField, ByteField, DecimalField, JsonField
from xia_fields import DateField, DateTimeField, TimestampField, TimeField
from xia_fields import Int64Field, UInt64Field, Int32Field, UInt32Field, IntField, CompressedStringField
from xia_fields import Fixed64Field, Fixed32Field, SFixed32Field, SFixed64Field
from xia_engine import Base, Document, EmbeddedDocumentField, ExternalField, ListField
from xia_api import XiaCollectionDeleteMsg, XiaDocumentDeleteMsg, XiaFileMsg, XiaErrorMessage, XiaActionResult


class XiaCompilerOpenapi:
    """Generate OpenApi Specification from data model

    """
    bundled: bool = True  # Bundle everything into one file

    string_dict = {
        "str": str,
        "float": float,
        "int": int,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    python_dict = {
        int: "integer",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    field_dict = {
        DoubleField: {"type": "number", "format": "double"},
        FloatField: {"type": "number", "format": "float"},
        Int64Field: {"type": "integer", "format": "int64"},
        DateField: {"type": "string"},
        TimestampField: {"type": "number"},
        UInt64Field: {"type": "integer", "format": "int64"},
        Int32Field: {"type": "integer", "format": "int32"},
        Fixed64Field: {"type": "integer", "format": "int64"},
        Fixed32Field: {"type": "integer", "format": "int32"},
        DateTimeField: {"type": "string"},
        TimeField: {"type": "string"},
        ByteField: {"type": "string"},
        CompressedStringField: {"type": "string"},
        UInt32Field: {"type": "integer", "format": "int32"},
        SFixed32Field: {"type": "integer", "format": "int32"},
        SFixed64Field: {"type": "integer", "format": "int64"},
        # General Field part
        IntField: {"type": "integer"},
        BooleanField: {"type": "boolean"},
        StringField: {"type": "string"},
        DecimalField: {"type": "string"},
        JsonField: {"type": "string"},
    }

    known_parameters = {
        "_catalog": {"name": "_catalog", "in": "query", "schema": {"type": "string"}, "example": "{}",
                     "description": "A dictionary which control which field should be displayed"},
        "_lazy": {"name": "_lazy", "in": "query", "schema": {"type": "boolean"}, "example": True,
                  "description": "When lazy is True, only minimum of data will be loaded."},
        "_limit": {"name": "_limit", "in": "query", "schema": {"type": "integer"}, "example": 50,
                   "description": "Maximum number of documents to be retrieved"},
        "_show_hidden": {"name": "_show_hidden", "in": "query", "schema": {"type": "boolean"}, "example": False,
                         "description": "Show the hidden fields"},
        "catalog": {"name": "catalog", "in": "query", "schema": {"type": "string"}, "example": "{}",
                    "description": "A dictionary which control which field should be displayed"},
        "lazy": {"name": "lazy", "in": "query", "schema": {"type": "boolean"}, "example": True,
                 "description": "When lazy is True, only minimum of data will be loaded."},
        "limit": {"name": "limit", "in": "query", "schema": {"type": "integer"}, "example": 50,
                  "description": "Maximum number of documents to be retrieved"},
        "show_hidden": {"name": "show_hidden", "in": "query", "schema": {"type": "boolean"}, "example": False,
                        "description": "Show the hidden fields"},
    }

    known_messages = [XiaCollectionDeleteMsg, XiaDocumentDeleteMsg, XiaErrorMessage, XiaActionResult]

    @classmethod
    def _get_ref(cls, class_name: str):
        if cls.bundled:
            return {"$ref": f"#/components/schemas/{class_name}"}
        else:
            return {"$ref": f"../documents/{class_name}.json"}

    @classmethod
    def _describe_errors(cls, response: dict) -> dict:
        error_content = {
            "application/json": {
                "schema": cls._get_ref("XiaErrorMessage")
            }
        }
        standard_errors = {
            "401": {"description": "Not authenticated", "content": error_content},
            "403": {"description": "Not authorized", "content": error_content},
            "404": {"description": "Not found", "content": error_content},
            "default": {"description": "Internal Server Error / Unknown Error", "content": error_content},
        }
        response["responses"].update(standard_errors)
        return response


    @classmethod
    def _get_properties_from_simple_field(cls, field: BaseField) -> dict:
        result = {}
        description = getattr(field, "description", None)
        default = getattr(field, "default", None)
        minimum = getattr(field, "value_min", None)
        maximum = getattr(field, "value_max", None)
        choices = getattr(field, "choices", None)
        max_length = getattr(field, "max_length", None)
        min_length = getattr(field, "min_length", None)
        regex = getattr(field, "regex", None)
        if description is not None:
            result["description"] = description
        if default is not None:
            result["default"] = field.to_display(default)
        if minimum is not None:
            result["minimum"] = field.to_display(minimum)
        if maximum is not None:
            result["maximum"] = field.to_display(maximum)
        if choices:
            result["enum"] = [field.to_display(val) for val in choices]
        if max_length is not None:
            result["maxLength"] = max_length
        if min_length is not None:
            result["minLength"] = min_length
        if regex is not None:
            result["pattern"] = regex if isinstance(regex, str) else regex.pattern
        for base_type, field_info in cls.field_dict.items():
            field_obj = field.field if isinstance(field, ListField) else field
            if isinstance(field_obj, base_type):
                result.update(field_info)
                return result

    @classmethod
    def _get_properties_from_field(cls, field: BaseField, document_library: dict, action_library: dict):
        result = {}
        # Step 1: Get description
        description = getattr(field, "description", None)
        if description is not None:
            result["description"] = description
        # Step 2: Get type / format
        if isinstance(field, EmbeddedDocumentField):
            if cls.bundled:
                result = cls._get_ref(field.document_type_class.__name__)
            else:
                result["type"] = "object"
                result["schema"] = cls._get_ref(field.document_type_class.__name__)
            cls.generate_document_model(field.document_type_class, document_library, action_library)
        elif isinstance(field, ExternalField):
            if field.list_length == 0:
                if cls.bundled:
                    result = cls._get_ref(field.document_type_class.__name__)
                else:
                    result["type"] = "object"
                    result["schema"] = cls._get_ref(field.document_type_class.__name__)
                cls.generate_document_model(field.document_type_class, document_library, action_library)
            else:
                result["type"] = "array"
                result["items"] = cls._get_ref(field.document_type_class.__name__)
                action_library[list] = {}
                cls.generate_document_model(field.document_type_class, document_library, action_library[list])
        elif isinstance(field, ListField):
            result["type"] = "array"
            if isinstance(field.field, EmbeddedDocumentField):
                action_library[list] = {}
                result["items"] = cls._get_ref(field.field.document_type_class.__name__)
                cls.generate_document_model(field.field.document_type_class, document_library, action_library[list])
            else:
                result["items"] = cls._get_properties_from_simple_field(field.field)
        else:
            return cls._get_properties_from_simple_field(field)
        return result

    @classmethod
    def _get_method_from_method_path(cls, document_class: Type[Base], method_path: str) -> callable:
        if "." not in method_path:
            return getattr(document_class, method_path)
        sub_paths = method_path.split('.')
        sub_class = document_class
        for sub_path in sub_paths[:-1]:
            sub_path = sub_path.split("[")[0]
            sub_class = getattr(sub_class, sub_path)
            if isinstance(sub_class, (EmbeddedDocumentField, ExternalField)):
                sub_class = sub_class.document_type_class
            elif isinstance(sub_class, ListField):
                sub_class = sub_class.field.document_type_class
        return getattr(sub_class, sub_paths[-1])

    @classmethod
    def _get_input_dict_from_action(cls, document_class: Type[Base], method_path: str) -> dict:
        method = cls._get_method_from_method_path(document_class, method_path)
        params = signature(method).parameters
        input_dict = {}
        for k, v in params.items():
            if k not in ["self", "cls"] and not k.startswith("_"):
                if v.annotation in cls.string_dict:
                    input_dict[k] = cls.string_dict[v.annotation]
                elif isinstance(v.annotation, type):
                    input_dict[k] = v.annotation
        return input_dict

    @classmethod
    def _inject_collection_method(cls, document_action: dict, document_class: Type[Base]):
        """If a method is a class method, set collection_method as true
        """
        for action_name, action_info in document_action.items():
            action_method = getattr(document_class, action_name)
            if callable(action_method):
                self_instance = getattr(action_method, "__self__", None)
                if self_instance is document_class:
                    action_info["collection_method"] = True

    @classmethod
    def generate_document_model(cls, document_class: Type[Base], document_library: dict, action_library: dict):
        """Generate Open API specs

        Args:
            document_library: Dict[class_name: class_definition]All document definition
            action_library: Dict[path: action]All actions
            document_class: Document class to be parsed
        """
        if document_class is None:
            return  # Bypass some control logic
        # Step 1 : Generation Operation
        properties, required = {}, []
        document_sample = document_class.get_sample()
        document_actions = document_class.get_actions()
        cls._inject_collection_method(document_actions, document_class)
        if document_actions:
            action_library[""] = document_actions
            # We might need generate document models
            for action_name, action_info in document_actions.items():
                # Predefined Output Objects
                output_type = action_info.get("out", None)
                cls.generate_document_model(output_type, document_library, {})
                # Predefined Input Objects
                input_dict_predefined = action_info.get("in", {})
                for _, input_type in input_dict_predefined.items():
                    cls.generate_document_model(input_type, document_library, {})
                # Parsed Input Objects
                input_dict = cls._get_input_dict_from_action(document_class, action_name)
                for input_key, input_type in input_dict.items():
                    if issubclass(input_type, Base):
                        cls.generate_document_model(input_type, document_library, {})
        if issubclass(document_class, Document):  # adding _id to outputs
            properties["_id"] = {"description": "Document ID", "type": "string"}
        for key in [fn for fn in document_sample.__dir__() if not fn.startswith("_")]:
            field = object.__getattribute__(document_sample, key)
            if isinstance(field, BaseField):
                action_library[key] = {}  # Pass a sub item for output
                properties[key] = cls._get_properties_from_field(field, document_library, action_library[key])
                if field.required:
                    required.append(key)
                if not action_library[key]:
                    # No action found so no need to keep the key
                    action_library.pop(key)
        # Step 2: Document Library related operation
        if document_class.__name__ in document_library:
            # Document Class already parsed, so we will pass
            return
        document_library[document_class.__name__] = {"type": "object", "properties": properties}
        document_library[document_class.__name__]["example"] = document_class.get_sample().get_display_data()
        if required:
            document_library[document_class.__name__]["required"] = required

    @classmethod
    def get_collection_get_path(cls, resource_name: str, document_class: Type[Document]):
        get_path = {
            "summary": "List " + document_class.__name__,
            "operationId": "search" + cls._convert_resource_name(resource_name),
            "description": "Retrieves a list of " + document_class.get_meta_data()["description"],
            "parameters": [
                cls.known_parameters["_catalog"],
                cls.known_parameters["_lazy"],
                cls.known_parameters["_limit"],
                cls.known_parameters["_show_hidden"]
            ],
            "responses": {
                "200": {
                    "description": "An array of " + document_class.__name__,
                    "content": {"application/json": {"schema": {
                        "type": "array", "items": cls._get_ref(document_class.__name__)
                    }}}
                }
            }
        }
        return cls._describe_errors(get_path)

    @classmethod
    def get_collection_delete_path(cls, resource_name: str, document_class: Type[Document]):
        delete_path = {
            "summary": "Delete all " + document_class.__name__,
            "operationId": "drop" + cls._convert_resource_name(resource_name),
            "description": "Delete all elements of " + document_class.get_meta_data()["description"],
            "parameters": [
                {"name": "drop", "in": "query", "schema": {"type": "boolean", "default": False},
                 "description": "When drop is true, all elements is dropped without validation check."}
            ],
            "responses": {
                "200": {
                    "description": "Summary of delete operation of " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref("XiaCollectionDeleteMsg")}}
                }
            }
        }
        return cls._describe_errors(delete_path)

    @classmethod
    def get_collection_post_path(cls, resource_name: str, document_class: Type[Document]):
        post_path = {
            "summary": "Create multiple " + document_class.__name__,
            "operationId": "append" + cls._convert_resource_name(resource_name),
            "description": "Create a few " + document_class.get_meta_data()["description"],
            "parameters": [],
            "requestBody": {"content": {"application/json": {"schema": {
                "type": "array", "items": cls._get_ref(document_class.__name__)
            }}}},
            "responses": {
                "200": {
                    "description": "An array of created" + document_class.__name__,
                    "content": {"application/json": {"schema": {
                        "type": "array", "items": cls._get_ref(document_class.__name__)
                    }}}
                }
            }
        }
        return cls._describe_errors(post_path)

    @classmethod
    def get_collection_path(cls, prefix: str, resource_name: str, document_class: Type[Document]) -> dict:
        full_prefix = prefix + "/" + resource_name
        collection_paths, get_path, delete_path, post_path = {full_prefix: {}}, {}, {}, {}
        get_path = cls.get_collection_get_path(resource_name, document_class)
        delete_path = cls.get_collection_delete_path(resource_name, document_class)
        post_path = cls.get_collection_post_path(resource_name, document_class)

        if get_path:
            collection_paths[full_prefix]["get"] = get_path
        if delete_path:
            collection_paths[full_prefix]["delete"] = delete_path
        if post_path:
            collection_paths[full_prefix]["post"] = post_path
        return collection_paths

    @classmethod
    def get_document_field_path(cls, key_fields: list):
        field_path = []
        for field_name in key_fields:
            field_path.append(field_name)
            field_path.append("{" + cls._get_operation_name(field_name) + "}")
        return '/'.join(field_path)

    @classmethod
    def get_path_parameter_from_field(cls, field_name: str, document_class: Type[Document]):
        if field_name == "_id":
            path_parameter = {"name": "_id", "in": "path", "schema": {"type": "string"}, "required": True}
        else:
            field = object.__getattribute__(document_class, field_name)
            field_schema = cls._get_properties_from_simple_field(field)
            field_schema.pop("default", None)  # Path parameter do not have default value
            path_parameter = {
                "name": cls._get_operation_name(field_name),
                "in": "path",
                "description": field_schema.pop("description", ""),
                "schema": field_schema,
                "required": True
            }
        return path_parameter

    @classmethod
    def _get_key_description(cls, key_fields: list):
        return ", ".join([cls._get_operation_name(fd) for fd in key_fields])

    @classmethod
    def _convert_resource_name(cls, resource_name: str):
        """Transform from kebab or snake case to camel case and make the lead letter upper"""
        words = resource_name.replace("-", "_").split("_")
        return ''.join([word.capitalize() for word in words])

    @classmethod
    def _get_operation_name(cls, path_string: str):
        """Transform from snake to camel case and keep the leading underscore"""
        starts_with_underscore = path_string.startswith("_")
        words = path_string.replace(".", "_").split("_")
        if not starts_with_underscore:
            return words[0] + ''.join([word.capitalize() for word in words[1:]])
        else:
            return "_" + words[1] + ''.join([word.capitalize() for word in words[2:]])

    @classmethod
    def _get_by_name(cls, key_fields: list, document_class: Type[Document]):
        if "_id" in key_fields:
            return "ById"
        elif key_fields == document_class.get_meta_data()["key_fields"]:
            return "ByKey"
        else:
            field_name = ''.join([word.capitalize() for word in key_fields[0].split("_")])
            return f"By{field_name}"

    @classmethod
    def get_document_get_path(cls, key_fields: list, resource_name: str, document_class: Type[Document]):
        fields_desc = cls._get_key_description(key_fields)
        document_sample = document_class.get_sample()
        path_parameters = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        query_parameters = [
            cls.known_parameters["catalog"],
            cls.known_parameters["lazy"],
            cls.known_parameters["show_hidden"],
        ]
        operation_id = cls._convert_resource_name(resource_name) + cls._get_by_name(key_fields, document_class)
        get_path = {
            "summary": "Get a " + document_class.__name__ + " by " + fields_desc,
            "operationId": "get" + operation_id,
            "description": f"Using key value ({fields_desc}) to get " + document_class.get_meta_data()["description"],
            "parameters": path_parameters + query_parameters,
            "responses": {
                "200": {
                    "description": "Detail of the document " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref(document_class.__name__)}}
                }
            }
        }
        return cls._describe_errors(get_path)

    @classmethod
    def get_document_delete_path(cls, key_fields: list, resource_name: str, document_class: Type[Document]):
        document_sample = document_class.get_sample()
        path_parameters = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        query_parameters = []
        operation_id = cls._convert_resource_name(resource_name) + cls._get_by_name(key_fields, document_class)
        delete_path = {
            "summary": "Delete a " + document_class.__name__,
            "operationId": "delete" + operation_id,
            "description": f"Delete by using one of the path defined in GET method. "
                           f"This path is just one of the possibility",
            "parameters": path_parameters + query_parameters,
            "responses": {
                "200": {
                    "description": "Detail of the document " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref("XiaDocumentDeleteMsg")}}
                }
            }
        }
        return cls._describe_errors(delete_path)

    @classmethod
    def get_document_patch_path(cls, key_fields: list, resource_name: str, document_class: Type[Document]):
        document_sample = document_class.get_sample()
        path_parameters = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        query_parameters = [
            cls.known_parameters["catalog"],
        ]
        operation_id = cls._convert_resource_name(resource_name) + cls._get_by_name(key_fields, document_class)
        patch_path = {
            "summary": "Update a " + document_class.__name__,
            "operationId": "modify" + operation_id,
            "description": f"Update some fields by using one of the path defined in GET method. "
                           f"This path is just one of the possibility",
            "parameters": path_parameters + query_parameters,
            "requestBody": {"content": {"application/json": {"schema": cls._get_ref(document_class.__name__)}}},
            "responses": {
                "200": {
                    "description": "Detail of the document " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref("XiaDocumentDeleteMsg")}}
                }
            }
        }
        return cls._describe_errors(patch_path)

    @classmethod
    def get_document_put_path(cls, key_fields: list, resource_name: str, document_class: Type[Document]):
        document_sample = document_class.get_sample()
        path_parameters = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        query_parameters = [
            cls.known_parameters["catalog"],
            {"name": "create", "in": "query", "schema": {"type": "boolean", "default": False},
             "description": "When create is True, a new document will be created instead of throwing errors."},
        ]
        operation_id = cls._convert_resource_name(resource_name) + cls._get_by_name(key_fields, document_class)
        put_path = {
            "summary": "Reset a " + document_class.__name__,
            "operationId": "replace" + operation_id,
            "description": f"Reset whole document by using one of the path defined in GET method. "
                           f"This path is just one of the possibility",
            "parameters": path_parameters + query_parameters,
            "requestBody": {"content": {"application/json": {"schema": cls._get_ref(document_class.__name__)}}},
            "responses": {
                "200": {
                    "description": "Detail of the document " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref("XiaDocumentDeleteMsg")}}
                }
            }
        }
        return cls._describe_errors(put_path)

    @classmethod
    def get_document_post_path(cls, key_fields: list, resource_name: str, document_class: Type[Document]):
        document_sample = document_class.get_sample()
        path_parameters = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        query_parameters = [
            cls.known_parameters["catalog"]
        ]
        operation_id = cls._convert_resource_name(resource_name) + cls._get_by_name(key_fields, document_class)
        post_path = {
            "summary": "Create a " + document_class.__name__,
            "operationId": "create" + operation_id,
            "description": f"Create a new document by using one of the path defined in GET method. "
                           f"This path is just one of the possibility",
            "parameters": path_parameters + query_parameters,
            "requestBody": {"content": {"application/json": {"schema": cls._get_ref(document_class.__name__)}}},
            "responses": {
                "200": {
                    "description": "Detail of the created document " + document_class.__name__,
                    "content": {"application/json": {"schema": cls._get_ref("XiaDocumentDeleteMsg")}}
                }
            }
        }
        return cls._describe_errors(post_path)

    @classmethod
    def get_document_path(cls, prefix: str, resource_name: str, endpoints: list, document_class: Type[Document]):
        document_paths = {}
        for idx, key_fields in enumerate(endpoints):
            full_prefix = prefix + "/" + resource_name + "/" + cls.get_document_field_path(key_fields)
            document_paths[full_prefix] = {}
            get_path = cls.get_document_get_path(key_fields, resource_name, document_class)
            post_path = cls.get_document_post_path(key_fields, resource_name, document_class)
            delete_path = cls.get_document_delete_path(key_fields, resource_name, document_class)
            patch_path = cls.get_document_patch_path(key_fields, resource_name, document_class)
            put_path = cls.get_document_put_path(key_fields, resource_name, document_class)
            if get_path:
                document_paths[full_prefix]["get"] = get_path
            if post_path:
                document_paths[full_prefix]["post"] = post_path
            if delete_path:
                document_paths[full_prefix]["delete"] = delete_path
            if patch_path:
                document_paths[full_prefix]["patch"] = patch_path
            if put_path:
                document_paths[full_prefix]["put"] = put_path
        return document_paths

    @classmethod
    def _get_index_path_parameter(cls, index_path_name: str):
        path_parameter = {
            "name": cls._get_operation_name(index_path_name),
            "in": "path",
            "description": f"Index number of {index_path_name.replace('_index', '')}, could be offset or key",
            "schema": {"type": "string"},
            "required": True
        }
        return path_parameter

    @classmethod
    def _get_action_schema_in_from_signature(cls, document_class: Type[Base], method_path: str) -> dict:
        param = {}
        input_dict = cls._get_input_dict_from_action(document_class, method_path)
        for input_key, input_type in input_dict.items():
            if input_type in cls.python_dict:
                param[input_key] = {"type": cls.python_dict.get(input_type)}
            elif issubclass(input_type, Base):
                param[input_key] = cls._get_ref(input_type.__name__)
            else:
                # by default object
                param[input_key] = {"type": "object"}
        return param

    @classmethod
    def _get_single_action_path(cls, key_fields: list, action_path: str, action: dict, operation_id: str,
                                collection_action: bool, document_class: Type[Base]):
        document_sample = document_class.get_sample()
        method_path = action_path.split("/_/")[-1].replace("/", ".").replace(".{", "[").replace("}.", "].")
        action_brief = f"Action: {document_class.__name__}.{method_path}"
        object_params = [cls.get_path_parameter_from_field(fd, document_sample) for fd in key_fields]
        index_list = [frag.split("}")[0] for frag in action_path.split("/_/")[-1].split("{")[1:]]
        index_params = [cls._get_index_path_parameter(index_item) for index_item in index_list]
        action_param = {
            "summary": action_brief,
            "operationId": operation_id,
            "description": action.get("description", action_brief),
            "responses": {
                "200": {
                    "description": "Result of action " + action_path + " of " + document_class.__name__,
                }
            }
        }
        if not collection_action:
            action_param["parameters"] = object_params + index_params
        # Get out action
        if "out" in action:
            output_type = action["out"]
            if isinstance(output_type, XiaFileMsg):
                action_param["responses"]["200"]["content"] = {
                    output_type.mime_type: {"schema": {"type": "string", "format": "binary"}}
                }
            else:
                action_param["responses"]["200"]["content"] = {
                    "application/json": {"schema": cls._get_ref(output_type.__name__)}
                }
        # Get in action from signature and then be completed by pre-defined actions
        action_schema_in = cls._get_action_schema_in_from_signature(document_class, method_path)
        if action_schema_in:
            input_dict = action.get("in", {})
            for input_key, input_type in input_dict.items():
                if action_schema_in.get(input_key, {}).get("type", None) == "array":
                    action_schema_in[input_key]["items"] = cls._get_ref(input_type.__name__)
                else:
                    action_schema_in[input_key] = cls._get_ref(input_type.__name__)
            for param_key, param_type in action_schema_in.items():
                if param_type.get("type", None) == "array" and "items" not in param_type:
                    param_type["items"] = {"type": "string"}  # Default to list of string
            action_param["requestBody"] = {
                "content": {"application/json": {"schema": {"type": "object", "properties": action_schema_in}}}
            }
        return cls._describe_errors(action_param)

    @classmethod
    def get_action_path_list(cls, action_path: str, action_dict: dict, action_list: list):
        for action_root, actions in action_dict.items():
            if action_root == "":
                for key, action in actions.items():
                    action_list.append([action_path + "/" + key, action])
            elif action_root == list:
                index_prefix = action_path.split("/")[-1]
                cls.get_action_path_list(action_path + "/{" + cls._get_operation_name(index_prefix) + "Index}",
                                         actions, action_list)
            else:
                cls.get_action_path_list(action_path + "/" + action_root, actions, action_list)

    @classmethod
    def get_action_path(cls, prefix: str, resource_name: str, endpoints: list,
                        document_class: Type[Document], document_actions: dict):
        action_list, action_paths = [], {}
        cls.get_action_path_list("", document_actions, action_list)
        for action_item in action_list:
            for key_fields in endpoints:
                resource_prefix = prefix + "/" + resource_name + "/" + cls.get_document_field_path(key_fields) + "/_"
                resource_prefix_cls = prefix + "/" + resource_name + "/_"  # Class method path
                operation_id = re.sub(r'\{.*?\}', '', action_item[0][1:]).replace("//", "/").replace("/", "_")
                operation_id = cls._get_operation_name(operation_id)
                operation_id += resource_name[0].upper() + resource_name[1:]
                if action_item[1].get("collection_method", False) and "/" not in action_item[0][1:]:
                    # the method is class method and the action path must be a root path like "/action"
                    full_prefix = resource_prefix_cls + action_item[0]
                    collection_action = True
                else:
                    full_prefix = resource_prefix + action_item[0]
                    operation_id += cls._get_by_name(key_fields, document_class)
                    collection_action = False
                action_path = cls._get_single_action_path(key_fields, full_prefix, action_item[1], operation_id,
                                                          collection_action, document_class)
                action_paths[full_prefix] = {"post": action_path}
        return action_paths

    @classmethod
    def get_root(cls, title: str, version: str, resource: str = ""):
        if os.path.exists("./VERSION"):
            with open("./VERSION") as fp:
                version = fp.read().strip()
        root_spec = {
            "openapi": "3.0.3",
            "info": {
                "title": title + " (" + resource + ")" if resource else title,
                "version": version
            },
            "paths": {}
        }
        return root_spec

    @classmethod
    def compile_spec(
            cls,
            resource_mapping: dict,
            document_library: dict,
            location: str,
            title: str,
            version: str,
            url_prefix: str,
            by_resource: bool = False,
            simplified: bool = True
    ):
        """Compile Open API Document

        Args:
            resource_mapping: URL map given by the application
            document_library: All models will be saved here
            location: file location to where all compiled files will be saved
            title: API Title
            version: API version
            url_prefix: URL prefix of API
            by_resource: when True, will generate a specification file per resource name
            simplified: Only contain essential endpoint (removing duplicates)
            bundled: Will include the schema definition in one file

        Returns:

        """
        if not url_prefix.startswith("/"):
            url_prefix = "/" + url_prefix  # url prefix must be / or it won't work
        # File system preparation
        if not os.path.exists(f"{location}"):
            os.makedirs(f"{location}")
        if not os.path.exists(f"{location}/resources"):
            os.makedirs(f"{location}/resources/")
        if not os.path.exists(f"{location}/documents"):
            os.makedirs(f"{location}/documents/")

        # Generate standard messages
        for message_class in cls.known_messages:
            cls.generate_document_model(message_class, document_library, {})

        # Generate specification
        root_spec = cls.get_root(title, version)
        action_library = {}
        for resource_name, document_class in resource_mapping.items():
            document_meta_data = document_class.get_meta_data()
            action_library[resource_name] = {}
            cls.generate_document_model(document_class, document_library, action_library[resource_name])
            collection_paths = cls.get_collection_path(url_prefix, resource_name, document_class)
            root_spec["paths"].update(collection_paths)

            unique_list, key_fields = [["_id"]], ["_id"]
            if document_meta_data["unique_lists"]:
                unique_list.extend(document_meta_data["unique_lists"])
            if document_meta_data["key_fields"]:
                # Case 1: key field are defined
                if document_meta_data["key_fields"] not in unique_list:
                    unique_list.append(document_meta_data["key_fields"])
                key_fields = document_meta_data["key_fields"]
            elif document_meta_data["unique_lists"]:
                # Case 2: we used the first unique list as key field.
                key_fields = document_meta_data["unique_lists"][0]
                # Case 3: we continue to use _id as key field
            endpoints = [key_fields] if simplified else unique_list
            document_paths = cls.get_document_path(url_prefix, resource_name, endpoints, document_class)
            root_spec["paths"].update(document_paths)

            document_actions = action_library[resource_name]
            action_paths = cls.get_action_path(url_prefix, resource_name, endpoints, document_class, document_actions)
            root_spec["paths"].update(action_paths)

            if by_resource:
                if cls.bundled:
                    root_spec["components"] = {"schemas": dict()}
                    for doc_name, doc_schema in document_library.items():
                        root_spec["components"]["schemas"][doc_name] = doc_schema

                with open(f"{location}/resources/{resource_name}.json", "w") as fp:
                    json.dump(root_spec, fp, ensure_ascii=False, indent=2)
                root_spec = cls.get_root(title, resource_name)

        # Save all document library
        if not cls.bundled:
            for doc_name, doc_schema in document_library.items():
                with open(f"{location}/documents/{doc_name}.json", "w") as fp:
                    json.dump(doc_schema, fp, ensure_ascii=False, indent=2)

        # Save the root spec if not seperated
        if not by_resource:
            if cls.bundled:
                root_spec["components"] = {"schemas": dict()}
                for doc_name, doc_schema in document_library.items():
                    root_spec["components"]["schemas"][doc_name] = doc_schema

            with open(f"{location}/resources/openapi.json", "w") as fp:
                json.dump(root_spec, fp, ensure_ascii=False, indent=2)
