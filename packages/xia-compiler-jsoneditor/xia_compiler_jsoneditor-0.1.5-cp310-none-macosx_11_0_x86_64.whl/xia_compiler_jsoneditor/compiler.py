from typing import Type, List, Dict
import os
import json
from copy import deepcopy
from inspect import signature
from xia_fields import BaseField
from xia_fields import BooleanField, DoubleField, FloatField, StringField, ByteField, DecimalField, JsonField
from xia_fields import DateField, DateTimeField, TimestampField, TimeField
from xia_fields import Int64Field, UInt64Field, Int32Field, UInt32Field, IntField, CompressedStringField
from xia_fields import Fixed64Field, Fixed32Field, SFixed32Field, SFixed64Field
from xia_engine import Base, Document, EmbeddedDocumentField, ExternalField, ListField
from xia_api import XiaCollectionDeleteMsg, XiaDocumentDeleteMsg, XiaFileMsg, XiaErrorMessage, XiaActionResult


class XiaCompilerJsoneditor:
    """Generate Json Editor Schema from data model

    """
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
        DoubleField: {"type": "number"},
        FloatField: {"type": "number"},
        Int64Field: {"type": "integer"},
        DateField: {"type": "string", "format": "date"},
        TimestampField: {"type": "number"},
        UInt64Field: {"type": "integer"},
        Int32Field: {"type": "integer"},
        Fixed64Field: {"type": "integer"},
        Fixed32Field: {"type": "integer"},
        DateTimeField: {"type": "string"},
        TimeField: {"type": "string", "format": "time"},
        ByteField: {"type": "string"},
        CompressedStringField: {"type": "string"},
        UInt32Field: {"type": "integer"},
        SFixed32Field: {"type": "integer"},
        SFixed64Field: {"type": "integer"},
        # General Field part
        IntField: {"type": "integer"},
        BooleanField: {"type": "boolean"},
        StringField: {"type": "string"},
        DecimalField: {"type": "string"},
        JsonField: {"type": "string"},
    }

    known_messages = [XiaCollectionDeleteMsg, XiaDocumentDeleteMsg, XiaErrorMessage, XiaActionResult]
    schema_types = {
        # "edit": {"show_hidden": True, "external": False, "key_read_only": True},
        # "display": {"show_hidden": False, "external": True, "show_link": True},
        # "search": {"show_hidden": True, "external": False, "no_default": True, "no_required": True},
        "schema_action": {"title": "{}", "show_hidden": False, "external": False},
        "schema_list": {"title": "{} List", "show_hidden": True, "external": False, "list_member": True},
        "schema_create": {"title": "Create {}", "show_hidden": True, "external": False},
        "schema_modify": {"title": "Edit {}", "show_hidden": False, "external": False, "key_read_only": True}
    }

    id_field = {
      "title": "Document ID",
      "type": "string",
      "links": [
        {
          "rel": "Go to document",
          "href": "./_id/{{self}}"
        }
      ]
    }

    @classmethod
    def create_dir_if_not_exists(cls, directory_name: str):
        if not os.path.exists(os.path.normpath(directory_name)):
            os.makedirs(os.path.normpath(directory_name))

    @classmethod
    def _get_properties_from_simple_field(cls, field: BaseField, schema_info: dict) -> dict:
        result = {}
        description = getattr(field, "description", None)
        default = getattr(field, "default", None)
        minimum = getattr(field, "value_min", None)
        maximum = getattr(field, "value_max", None)
        choices = getattr(field, "choices", None)
        max_length = getattr(field, "max_length", None)
        min_length = getattr(field, "min_length", None)
        regex = getattr(field, "regex", None)
        hidden = getattr(field, "hidden", None)
        if description is not None:
            result["description"] = description
        if default is not None and not schema_info.get("no_default", False):
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
        # Options
        if hidden:
            result["options"] = {}   # Need to add options
            if hidden:
                result["options"]["hidden"] = True

        # New get field type:
        for base_type, field_info in cls.field_dict.items():
            field_obj = field.field if isinstance(field, ListField) else field
            if isinstance(field_obj, base_type):
                result.update(field_info)
                break

        # Special adjustment for fields
        if result["type"] == "string" and "format" not in result and "\n" in str(field.sample):
            result["format"] = "textarea"

        return result

    @classmethod
    def _get_properties_from_field(
            cls,
            field: BaseField,
            document_library: dict,
            schema_type: str,
            location: str,
            resource_mapping: dict,
            editor_root: str
    ):
        """Get Properties from a field

        Args:
            field: Field Object
            document_library: Total document library
            schema_type: Type of schema
            location: reference document location
            resource_mapping: full site resource mapping
            editor_root: The root url of editor

        Returns:
            field properties dictionary. None means the item shouldn't be present
        """
        result = {}
        # Step 1: Get description
        description = getattr(field, "description", None)
        if description is not None:
            result["description"] = description
        # Step 2: Get type / format
        schema_info = cls.schema_types.get(schema_type, {})
        if isinstance(field, EmbeddedDocumentField):
            result["$ref"] = f"/static/references/{field.document_type_class.__name__}/{schema_type}.json"
            cls.generate_document_model(field.document_type_class, document_library, location,
                                        resource_mapping, editor_root)
        elif isinstance(field, ExternalField):
            if schema_info.get("external", True):
                if field.list_length == 0:
                    ref_schema_name = f"/static/references/{field.document_type_class.__name__}/{schema_type}.json"
                    result["$ref"] = ref_schema_name
                    cls.generate_document_model(field.document_type_class, document_library, location,
                                                resource_mapping, editor_root)
                else:
                    ref_schema_name = f"/static/references/{field.document_type_class.__name__}/{schema_type}.json"
                    result["type"] = "array"
                    result["items"] = {"$ref": ref_schema_name}
                    if getattr(field.document_type_class, "_key_fields", None):
                        result["format"] = "tabs-top"
                    cls.generate_document_model(field.document_type_class, document_library, location,
                                                resource_mapping, editor_root)
            else:
                return None
        elif isinstance(field, ListField):
            result["type"] = "array"
            if isinstance(field.field, EmbeddedDocumentField):
                if getattr(field.field.document_type_class, "_key_fields", None):
                    result["format"] = "tabs-top"
                ref_schema_name = f"/static/references/{field.field.document_type_class.__name__}/{schema_type}.json"
                result["items"] = {"$ref": ref_schema_name}
                cls.generate_document_model(field.field.document_type_class, document_library, location,
                                            resource_mapping, editor_root)
            else:
                result["format"] = "table"
                result["items"] = cls._get_properties_from_simple_field(field.field, schema_info)
        else:
            result = cls._get_properties_from_simple_field(field, schema_info)
        # Step 3: Display related settings
        display = getattr(field, "display", None)
        if display and display.get("read_only", False):
            result["readOnly"] = True
        # Step 4: Prepare options
        result["options"] = {}
        return result

    @classmethod
    def _get_input_dict_from_action(cls, document_class: Type[Base], method_name: str) -> dict:
        input_dict = {}
        method = getattr(document_class, method_name, None)
        if method:
            params = signature(method).parameters
            for k, v in params.items():
                if k not in ["self", "cls"] and not k.startswith("_"):
                    if v.annotation in cls.string_dict:
                        input_dict[k] = cls.string_dict[v.annotation]
                    elif isinstance(v.annotation, type):
                        input_dict[k] = v.annotation
        return input_dict

    @classmethod
    def _get_schema_from_signature(cls, document_class: Type[Base], method_name, location: str):
        """Get json schema from input signature

        Args:
            document_class: Dict[class_name: class_definition]All document definition
            method_name: method name
            location: reference document location
        """
        param = {}
        default_type = next(iter(cls.schema_types))  # First one is default
        input_dict = cls._get_input_dict_from_action(document_class, method_name)
        input_dict_predefined = document_class.get_actions().get(method_name, {}).get("in", {})
        for input_key, input_type in input_dict.items():
            if input_key in input_dict_predefined:
                input_class_name = input_dict_predefined[input_key].__name__
                if input_type == list:
                    param[input_key] = {
                          "type": "array",
                          "items": {
                            "$ref": f"/static/references/{input_class_name}/{default_type}.json"
                          }
                        }
                else:
                    param[input_key] = {"$ref": f"/static/references/{input_class_name}/{default_type}.json"}
            elif input_type in cls.python_dict:
                param[input_key] = {"type": cls.python_dict.get(input_type)}
            elif issubclass(input_type, Base):
                param[input_key] = {"$ref": f"/static/references/{input_type.__name__}/{default_type}.json"}
            else:
                param[input_key] = {"type": "object"}  # By default object but shouldn't happen
        return param

    @classmethod
    def generate_document_model(
            cls,
            document_class: Type[Base],
            document_library: dict,
            location: str,
            resource_mapping: dict,
            editor_root: str
    ):
        """Generate Open API specs

        Args:
            document_library: Dict[class_name: class_definition]All document definition
            document_class: Document class to be parsed
            location: reference document location
            resource_mapping: full site resource mapping
            editor_root: The root url of editor

        Notes:
            schemas is a dictionary which will hold the json schema of the same object of different configuration
        """
        if document_class is None:
            return  # Bypass some control logic
        # Step 1 : Generation of Model
        required = []
        schemas = {schema_type: {} for schema_type in cls.schema_types}
        document_sample = document_class.get_sample()
        # Special: For Documents defined in resource mapping, we will put _id field
        for resource_name, resource_class in resource_mapping.items():
            if resource_class == document_class:
                for schema_type in cls.schema_types:
                    if cls.schema_types[schema_type].get("show_link", False):
                        url_root = editor_root + resource_name
                        schemas[schema_type]["_id"] = deepcopy(cls.id_field)
                        schemas[schema_type]["_id"]["links"][0]["href"] = url_root + "/_id/{{self}}"
        # Generate field information
        for schema_type in cls.schema_types:
            for key in [fn for fn in document_sample.__dir__() if not fn.startswith("_")]:
                field = object.__getattribute__(document_sample, key)
                if isinstance(field, BaseField):
                    field_info = cls._get_properties_from_field(field, document_library, schema_type, location,
                                                                resource_mapping, editor_root)
                    if field_info is not None:
                        if getattr(field, "hidden", None) and cls.schema_types[schema_type].get("show_hidden", False):
                            # Need to show hidden field
                            field_info["options"]["hidden"] = False
                        schemas[schema_type][key] = field_info
                    if field.required and key not in required:
                        required.append(key)
            if cls.schema_types[schema_type].get("key_read_only", False) and isinstance(document_sample, Document):
                for key_name in document_sample.get_meta_data()["key_fields"]:
                    schemas[schema_type][key_name]["readOnly"] = True

        # Step 2: Generate Action Maps, will only support first level actions
        methods = document_class.get_actions()
        action_schema = {}
        for method_name, method_info in methods.items():
            method = getattr(document_class, method_name)
            if not method:
                continue
            # Step 2.1 Prepare library with "in" parameter
            input_dict_predefined = method_info.get("in", {})
            for _, input_type in input_dict_predefined.items():
                cls.generate_document_model(input_type, document_library, location, resource_mapping, editor_root)
            input_dict = cls._get_input_dict_from_action(document_class, method_name)
            for input_key, input_type in input_dict.items():
                if issubclass(input_type, Base):
                    cls.generate_document_model(input_type, document_library, location, resource_mapping, editor_root)
            action_schema_properties = cls._get_schema_from_signature(document_class, method_name, location)
            action_schema[method_name] = {
                "type": "object",
                "title": f"Action: {method_name.replace('_', ' ')}",
                "description": method_info.get("description", None),
            }
            # When the only parameter is payload, we will expand the payload as first level parameter
            if list(action_schema_properties) == ["payload"]:
                action_schema[method_name]["$ref"] = action_schema_properties["payload"]["$ref"]
            else:
                action_schema[method_name]["properties"] = action_schema_properties

        # Step 3: Save the generated document model
        if document_class.__name__ in document_library:
            # Document Class already parsed, so we will pass
            return
        if document_class.__name__ not in document_library:
            document_library[document_class.__name__] = {}
        for schema_type, schema_content in schemas.items():
            document_title = document_class.__name__
            for resource_name, resource_class in resource_mapping.items():
                if resource_class == document_class:
                    document_title = resource_name.capitalize()  # We prefer using resource name as title
            document_library[document_class.__name__][schema_type] = {
                "type": "object",
                "title": cls.schema_types[schema_type].get("title", "{}").format(document_title),
                "format": "grid",
                "properties": schema_content
            }
            key_fields = getattr(document_class, "_key_fields", None)
            if key_fields and cls.schema_types[schema_type].get("list_member", False):
                # Show header when need to be shown as list {{ self.key1 }} | {{ self.key2 }}
                header_template = "|".join(["{{ self." + key + " }}" for key in key_fields])
                document_library[document_class.__name__][schema_type]["headerTemplate"] = header_template
        if action_schema:
            document_library[document_class.__name__]["_action"] = action_schema
        if required:
            for schema_type, schema_content in schemas.items():
                if not cls.schema_types[schema_type].get("no_required", False):
                    document_library[document_class.__name__][schema_type]["required"] = required

    @classmethod
    def compile_schema(
            cls,
            resource_mapping: dict,
            document_library: dict,
            location: str,
            editor_root: str = "/"
    ):
        """Compile Open API Document

        Args:
            resource_mapping: URL map given by the application
            document_library: All models will be saved here
            location: file location to where all compiled files will be saved
            editor_root: The root url of editor

        Returns:

        """
        schema_location = location.lstrip(".")

        # File system preparation
        cls.create_dir_if_not_exists(location)
        cls.create_dir_if_not_exists(f"{location}/references")
        cls.create_dir_if_not_exists(f"{location}/schemas")

        # Generate standard messages
        for message_class in cls.known_messages:
            cls.generate_document_model(message_class, document_library, schema_location, resource_mapping, editor_root)

        # Generate specification
        for resource_name, document_class in resource_mapping.items():
            cls.generate_document_model(document_class, document_library, schema_location, resource_mapping,
                                        editor_root)

        # Save all document library
        for doc_name, doc_schema in document_library.items():
            # doc_name: Class Name / doc_schema: all document schema
            cls.create_dir_if_not_exists(f"{location}/references/{doc_name}")
            action_schemas = doc_schema.pop("_action", {})
            for schema_type in doc_schema:
                # Save all in references
                with open(f"{location}/references/{doc_name}/{schema_type}.json", "w") as fp:
                    json.dump(doc_schema[schema_type], fp, ensure_ascii=False, indent=2)
                # Save another copy in schemas if the class presents in the resource mapping
                for resource_name, document_class in resource_mapping.items():
                    if document_class.__name__ == doc_name:
                        # Means it is a top-level class
                        cls.create_dir_if_not_exists(f"{location}/schemas/{resource_name}")
                        with open(f"{location}/schemas/{resource_name}/{schema_type}.json", "w") as fp:
                            json.dump(doc_schema[schema_type], fp, ensure_ascii=False, indent=2)
                        cls.create_dir_if_not_exists(f"{location}/schemas/{resource_name}/actions")
                        for method_name, method_schema in action_schemas.items():
                            cls.create_dir_if_not_exists(f"{location}/schemas/{resource_name}/actions")
                            with open(f"{location}/schemas/{resource_name}/actions/{method_name}.json", "w") as fp:
                                json.dump(method_schema, fp, ensure_ascii=False, indent=2)
