import pickle
from typing import Type, Union
from importlib import import_module
from xia_fields import BaseField, StringField, BooleanField, DictField, ByteField
from xia_engine import MetaDocument, RamEngine
from xia_engine import Base, BaseDocument, Document, EmbeddedDocument
from xia_engine import EmbeddedDocumentField, ListField, ExternalField, ListRuntime


class BaseModel(Document):
    _key_fields = ["domain_name", "model_name"]
    _model_library = {}  #: Keep all compiled modules
    _engine = RamEngine

    domain_name: str = StringField(description="Data Domain Name")
    model_name: str = StringField(description="Data Model Name")

    @classmethod
    def cache_model(cls, domain_name: str, model_name: str, model_class: Type[Document]):
        """Put precompiled class into cache in order that it could be retrieved later

        Args:
            domain_name (str): Data Domain Name
            model_name (str): Model Class Name
            model_class: Model class
        """
        cls._model_library[(domain_name, model_name)] = model_class

    @classmethod
    def get_class(cls, domain_name: str, model_name: str, model_module: str = "",
                  no_cache: bool = False, no_runtime: bool = False):
        """

        Args:
            domain_name (str): Data Domain Name
            model_name (str): Model Class Name
            model_module (str): Module to load document
            no_cache (bool): Do not get from cache
            no_runtime (bool): Do not get from Python Runtime
        """
        if not no_cache:
            new_class = cls.load_class_from_library(domain_name, model_name)
            if new_class:
                # Case 1: Check the model_library, return the compiled one
                return new_class
        if not no_runtime and model_module:
            new_class = cls.load_class_from_runtime(model_module, model_name)
            if new_class:
                # Case 2: Check if we could load from repository
                cls._model_library[(domain_name, model_name)] = new_class
                return new_class
        saved_model = cls.load(domain_name=domain_name, model_name=model_name)
        if saved_model:
            return saved_model.load_class()

    @classmethod
    def load_class_from_library(cls, domain_name: str, model_name: str) -> Type[Base]:
        """Get class from compiled library

        Args:
            domain_name (str): Data Domain Name
            model_name (str): Model Class Name

        Returns:
            Document class
        """
        return cls._model_library.get((domain_name, model_name), None)

    @classmethod
    def load_class_from_runtime(cls, module_name, class_name) -> Union[Type[Base], None]:
        """Get class from imported modules (Python runtime)

        Args:
            module_name (str): Module to load document
            class_name (str): Model Class Name

        Returns:
            Document class if found else None
        """
        if module_name:
            try:
                model_module = import_module(module_name)
            except ModuleNotFoundError:
                return None
            model_class = getattr(model_module, class_name, None)
            return model_class
        return None

    def load_class(self) -> Type[Base]:
        """Get runtime class from loaded data

        Returns:
            Runtime class
        """


class DataField(EmbeddedDocument):
    _key_fields = ["field_name"]

    field_name: str = StringField(description="Field name", required=True, sample="field_1")
    description: str = StringField(description="Field description", sample="This is a common field")
    module_name: str = StringField(description="module name of the field", required=True, default="xia_fields")
    class_name: str = StringField(description="Field class Name", required=True, sample="StringField")
    field_params: bytes = ByteField(description="Parameters of Field")
    list_params: dict = ByteField(description="Parameters of List Field")

    @classmethod
    def _get_param_from_value(cls, value):
        if isinstance(value, Base):
            return value.get_display_data()
        elif isinstance(value, list):
            return [cls._get_param_from_value(v) for v in value]
        elif isinstance(value, tuple) and len(value) == 2:
            # Try best to keep runtime value
            if isinstance(value[1], ListRuntime):
                return cls._get_param_from_value(value[0]), None
            else:
                return cls._get_param_from_value(value[0]), cls._get_param_from_value(value[1])
        else:
            return value

    @classmethod
    def _get_params_from_field(cls, field_object: BaseField):
        params = {}
        for key in [k for k in field_object.__dir__() if not k.startswith("_")]:
            value = getattr(field_object, key)
            if value is not None and not hasattr(field_object.__class__, key):
                # Remove None, class attributes
                if callable(value) and not (isinstance(value, type) and issubclass(value, (Base, BaseField))):
                    continue  # Remove methods
                if field_object.runtime and key == "sample":
                    continue  # Runtime field's sample value is not stored
                params[key] = cls._get_param_from_value(value)
        return params

    @classmethod
    def dump_field(cls, field_name: str, field_object: BaseField, domain_name: str, data_model, dumped: dict):
        module_name = field_object.__class__.__module__
        class_name = field_object.__class__.__name__
        params = cls._get_params_from_field(field_object)
        list_params = None
        description = params.pop("description", "")
        if isinstance(field_object, ListField):
            list_params = params
            field_class = list_params["field_class"]
            list_params["field_class"] = {"module": field_class.__module__, "class": field_class.__name__}
            field_params = cls._get_params_from_field(params.pop("field"))
        else:
            field_params = params

        if "document_type_class" in field_params:
            document_class = field_params.pop("document_type_class")
            field_params["document_type"] = {"module": document_class.__module__, "class": document_class.__name__}
            data_model.dump_models(document_class, dumped, domain_name)
        if list_params is not None:
            dumped_field = cls(field_name=field_name, module_name=module_name, class_name=class_name,
                               field_params=pickle.dumps(field_params), description=description,
                               list_params=pickle.dumps(list_params))
        else:
            dumped_field = cls(field_name=field_name, module_name=module_name, class_name=class_name,
                               description=description, field_params=pickle.dumps(field_params))
        return dumped_field

    @classmethod
    def load_field_class(cls, data_model: BaseModel, module_name: str, class_name: str):
        """Get class of field EmbeddedDocumentField or ExternalField

        Args:
            class_name: Class Name
            module_name: Module Name
            data_model: document model

        Returns
            Document class
        """
        doc_class = data_model.load_class_from_library(data_model.domain_name, class_name)
        if doc_class:
            return doc_class
        doc_class = data_model.load_class_from_runtime(module_name, class_name)
        if doc_class:
            return doc_class
        doc_model = data_model.load(domain_name=data_model.domain_name, model_name=class_name)
        if not doc_model:
            raise ValueError(f"Document class {data_model.domain_name}-{module_name}-{class_name} not found")
        doc_class = doc_model.load_class()
        if not doc_class:
            raise ValueError(f"Document class {data_model.domain_name}-{module_name}-{class_name} not found")
        return doc_class

    def load_field(self, data_model: BaseModel):
        field_module = import_module(self.module_name)
        field_class = getattr(field_module, self.class_name)
        field_params = pickle.loads(self.field_params)
        if "document_type" in field_params:
            module_name = field_params["document_type"]["module"]
            class_name = field_params["document_type"]["class"]
            field_params["document_type"] = self.load_field_class(data_model, module_name, class_name)
        if isinstance(self.list_params, bytes):
            list_params = pickle.loads(self.list_params)
            item_class = list_params.pop("field_class")
            module_name = item_class["module"]
            class_name = item_class["class"]
            item_class = data_model.load_class_from_runtime(module_name, class_name)
            if not item_class:
                raise ValueError(f"List item class {module_name}-{class_name} not found")
            item_object = item_class(**field_params)
            field = field_class(description=self.description, field=item_object, **list_params)
        else:
            field = field_class(description=self.description, **field_params)
        return field


class DataModel(BaseModel):
    _privilege_keys = {"visibility": ["visibility"]}

    model_module: str = StringField(description="Data Model Module")
    parent_domain: str = StringField(description="Parent class domain name")
    parent_module: str = StringField(description="Parent class module name")
    parent_class: str = StringField(description="Parent class name", required=True)
    visibility: str = StringField(description="Data Model Visibility", default="protected",
                                  choices=["public", "protected", "private"])

    collection_name: str = StringField(description="Collection Name")
    description: str = StringField(description="Data Model Description")
    logger_name: str = StringField(description="Data logger name")
    table_name: str = DictField(description="Embedded Document Table Name Dictionary")
    key_fields: list = ListField(field=StringField(), description="Key fields")
    fields_map: dict = DictField(description="Embedded Document Field Maps")
    cluster_fields: list = ListField(field=StringField(), description="Cluster Fields")
    partition_info: dict = DictField(description="Partition Information")
    privilege_keys: dict = DictField(description="Privilege key for authorization check")

    field_list: list = ListField(EmbeddedDocumentField(document_type=DataField), default=[])

    @classmethod
    def get_document_meta(cls, model_sample: Document):
        return {
            "description": getattr(model_sample, "_description", ""),
            "domain_name": getattr(model_sample, "_domain_name", ""),
            "logger_name": getattr(model_sample, "_logger_name", ""),
            "collection_name": model_sample.get_collection_name(RamEngine),
            "key_fields": getattr(model_sample, "_key_fields", []),
            "cluster_fields": getattr(model_sample, "_cluster_fields", []),
            "partition_info": getattr(model_sample, "_partition_info", {}),
            "privilege_keys": getattr(model_sample, "_privilege_keys", {}),
        }

    @classmethod
    def get_embedded_meta(cls, model_sample: EmbeddedDocument):
        meta = {
            "domain_name": getattr(model_sample, "_domain_name", ""),
            "table_name": getattr(model_sample, "_table_name", None),
            "key_fields": getattr(model_sample, "_key_fields", None),
            "fields_map": getattr(model_sample, "_fields_map", None),
        }
        return {k: v for k, v in meta.items() if v is not None}

    @classmethod
    def dump_models(cls, model_class: Type[Base], dumped: dict = None, domain_name: str = ""):
        """Dump models to

        Args:
            model_class: The model to be parsed
            dumped: Dumped document model
            domain_name: current domain name

        Returns:
            Dictionary of models
        """
        dumped = {} if dumped is None else dumped
        if model_class.__name__ in dumped:
            return dumped
        model_name = model_class.__name__
        model_module = model_class.__module__
        parent_class = model_class.__bases__[0]  # Only get the first
        parent_module = parent_class.__module__
        parent_class = parent_class.__name__  # We do only need name

        doc_sample = model_class.get_sample()
        meta_info = {}
        if issubclass(model_class, EmbeddedDocument):
            meta_info = cls.get_embedded_meta(doc_sample)
        elif issubclass(model_class, Document):
            meta_info = cls.get_document_meta(doc_sample)

        predefined_domain_name = meta_info.pop("domain_name", "")
        domain_name = predefined_domain_name if predefined_domain_name else domain_name
        if not domain_name:  # Only raise error for the 1st dumping model
            raise ValueError(f"Domain Name is mandatory for dumping model {model_class.__name__}")
        # Get Fields
        field_list = []
        for key in [k for k in doc_sample.__dir__() if not k.startswith("_")]:
            field = object.__getattribute__(doc_sample, key)
            if isinstance(field, BaseField):
                field_list.append(DataField.dump_field(key, field, domain_name, cls, dumped))
        dumped_model = cls(
            domain_name=domain_name, model_name=model_name, model_module=model_module,
            parent_module=parent_module, parent_class=parent_class, **meta_info,
            field_list=field_list
        )
        dumped[model_class.__name__] = dumped_model
        return dumped

    @classmethod
    def upsert_models(cls, model_class: Type[Base], dumped: dict = None, domain_name: str = ""):
        for model_name, data_model in cls.dump_models(model_class, dumped, domain_name).items():
            doc_id = data_model.calculate_id()
            data_model._id = doc_id  # Assign an id
            data_model.save()

    def load_embedded_meta(self) -> dict:
        meta_info = {
            "_domain_name": getattr(self, "domain_name", ""),
            "_table_name": getattr(self, "table_name", None),
            "_key_fields": getattr(self, "key_fields", None),
            "_fields_map": getattr(self, "fields_map", None),
        }
        return {k: v for k, v in meta_info.items() if v is not None}

    def load_document_meta(self):
        meta_info = {
            "_description": getattr(self, "description", ""),
            "_domain_name": getattr(self, "domain_name", ""),
            "_logger_name": getattr(self, "logger_name", ""),
            "_meta": {"collection_name": self.get_collection_name(RamEngine)},
            "_key_fields": getattr(self, "key_fields", []),
            "_cluster_fields": getattr(self, "cluster_fields", []),
            "_partition_info": getattr(self, "partition_info", {}),
            "_privilege_keys": getattr(self, "privilege_keys", {}),
        }
        return meta_info

    def load_class(self) -> Type[Base]:
        # Case 3: Create one with saved parameters
        class_parameters = {}
        for field in self.field_list:
            field_object = field.load_field(self)
            class_parameters[field.field_name] = field_object
        parent_module = import_module(self.parent_module)
        parent_class = getattr(parent_module, self.parent_class)
        if issubclass(parent_class, Document):
            meta_info = self.load_embedded_meta()
        elif issubclass(parent_class, EmbeddedDocument):
            meta_info = self.load_document_meta()
        else:
            meta_info = {}
        class_parameters.update(meta_info)
        new_class = MetaDocument(
            self.model_name,
            (parent_class, ),
            class_parameters
        )
        # Save to library
        self._model_library[(self.domain_name, self.model_name)] = new_class
        return new_class
