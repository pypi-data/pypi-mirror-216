from __future__ import annotations
from typing import Type, Union
from importlib import import_module
from xia_fields import StringField, DictField, BaseField, BooleanField, JsonField
from xia_engine import RamEngine
from xia_engine import EmbeddedDocumentField, ListField
from xia_engine import Base, BaseDocument, Document, EmbeddedDocument
from xia_models.model import DataModel


class TableAddress(EmbeddedDocument):
    """Table Address Sub-Object

    Table Data might be saved in several tables (special in the case of SQL Databases)
    """
    _key_fields = ["sub_model_name"]

    sub_model_name: str = StringField(description="Data Model Name in the data model")
    table_name: str = StringField(description="Table Name")


class TableCatalog(EmbeddedDocument):
    """Table Catalogue Object in list of dictionary type

    Rules:
        * Catalog saved in class: {"field_1": None, "field_2": {"field_3": True}}
        * Catalog saved in data model: [
            {"internal_name": "`field_1`", "field_name": "field_1", "value": None}
            {"internal_name": "`field_2`.`field_3`", "field_name": "field_2.field_3, "value": True}
        ]
    """
    _key_fields = ["field_name"]

    field_name = StringField(description="Field Name", sample="field_name")
    path = StringField(description="Internal Path Name", sample="`field_name`")
    lazy_mode = BooleanField(description="Lazy Mode Configuration")

    @classmethod
    def catalog_to_model(cls, catalog_dict: Union[dict, None], current_path: str = ""):
        if not catalog_dict:
            return None
        catalog_list = []
        for key, value in catalog_dict.items():
            new_key = "`" + key + "`"
            child_path = (current_path + "." + new_key) if current_path else new_key
            if isinstance(value, dict):
                catalog_list += cls.catalog_to_model(value, child_path)
            else:
                catalog_item = {"field_name": child_path.replace("`", ""), "path": child_path, "lazy_mode": value}
                catalog_list.append(catalog_item)
        if current_path == "":
            catalog_list = [TableCatalog.from_display(**item) for item in catalog_list]
        return catalog_list

    @classmethod
    def catalog_to_class(cls, catalog_list: Union[list, None]):
        if not catalog_list:
            return None
        catalog_dict = {}
        for item in catalog_list:
            current_dict = catalog_dict
            paths = item.path.split("`.`")
            paths[0] = paths[0].lstrip().lstrip("`")
            paths[-1] = paths[-1].rstrip().rstrip("`")
            for path in paths[:-1]:
                if path not in current_dict:
                    current_dict.update({path: {}})
                current_dict = current_dict[path]
            current_dict[paths[-1]] = item.lazy_mode
        return catalog_dict


class DataAddress(Document):
    """Address Object

    Usage:
        * It helps to get the information of where and which data is stored

    Rules:
        * A data model could be saved at several address
        * An address could be used by several application
        * An application could hold several address

    Examples:
        * Model A Save a part of its data in SqliteEngine with address "adr1":
            * In Model A _address object will be maintained with key "adr1":
            ```
            _address = {"sqlite": {"_db": "adr1", other parameters}}
            ```
            * In SqliteEngine,

    """
    _key_fields = ["domain_name", "model_name", "address_name"]
    _model_library = {}  #: Keep all compiled addressed modules
    _engine = RamEngine

    domain_name: str = StringField(description="Data Domain Name")
    model_name: str = StringField(description="Data Model Name")
    address_name: str = StringField(description="Address Name", sample="sqlite_db1")
    param_name: str = StringField(description="Database Parameter Name", sample="sqlite")
    engine_module: str = StringField(description="Engine Module", sample="xia_engine_sql")
    engine_class: str = StringField(description="Engine Class", sample="SqliteEngine")
    catalog: list = ListField(EmbeddedDocumentField(document_type=TableCatalog), description="Data catalog")
    scope: list = JsonField(description="Data scope", sample='[{"fn": "field", "op": "in", "val": ["0001", "0002"]}]')
    tables: list = ListField(EmbeddedDocumentField(document_type=TableAddress), description="Table name of sub model")

    connector_module: str = StringField(description="Connector Module", sample="xia_engine_sql")
    connector_class: str = StringField(description="Connector Class", sample="SqliteConnector")
    connector_param: str = DictField(description="Connector Parameters")
    other_param: str = DictField(description="Other Engine Parameters")

    @classmethod
    def cache_addressed_model(cls, domain_name: str, model_name: str, address_name: str, model_class: Type[Document]):
        """Put a precompiled data model into cache so it could be retrieved later

        Args:
            domain_name: Data Domain name
            model_name: Data model name
            address_name: Address name
            model_class: Model class
        """
        cls._model_library[(domain_name, model_name, address_name)] = model_class

    @classmethod
    def get_addressed_model(cls, domain_name: str, model_name: str, address_name: str,
                            model_manager: Type[DataModel], default_address: DataAddress = None):
        """Get a data model with address configuration

        Args:
            domain_name: Data Domain name
            model_name: Data model name
            address_name: Address name
            model_manager: The API to get the data model
            default_address: Default Address Object (when the specific cannot be found by using API)

        Returns:
            DataModel with Address
        """
        if (domain_name, model_name, address_name) in cls._model_library:
            return cls._model_library[(domain_name, model_name, address_name)]
        else:
            model_data = model_manager.load(domain_name=domain_name, model_name=model_name)
            model_class = model_data.load_class()
            if not model_class:
                raise ValueError(f"Model not found: {domain_name}/{model_name}")
            class_address = cls.load(domain_name=domain_name, model_name=model_name, address_name=address_name)
            if not class_address and not default_address:
                raise ValueError(f"Address not found / no default: {domain_name}/{model_name}/{address_name}")
            class_address = class_address if class_address else default_address
            class_address.assign_address(model_class)
            cls._model_library[(domain_name, model_name, address_name)] = model_class
            return model_class

    @classmethod
    def _update_table_name_to_field(cls,
                                    parent_name: str,
                                    separator: str,
                                    document_class: Type[Base],
                                    table_name_dict: dict,
                                    create_table: bool = True):
        """Update Embedded Document's field type

        Args:
            parent_name: parent table name
            separator: table seperator
            document_class: Document to be parsed
            table_name_dict: the predefined table_name dictionary
            create_table: Create table for this component
        """
        doc_sample = document_class.get_sample()
        predefined_table_name = table_name_dict.get(document_class.__name__, None)
        if parent_name == "":  # Root document
            current_table_name = default_table_name = document_class.get_collection_name()
        elif not create_table:
            current_table_name = default_table_name = parent_name  # No table to be created, so keeping the name
        else:
            current_table_name = default_table_name = parent_name + separator + document_class.__name__
        # Step 1: Check if it is needed to update table name settings
        if create_table and predefined_table_name and predefined_table_name != default_table_name:
            if getattr(document_class, "_table_name", None):
                document_class._table_name[parent_name] = predefined_table_name
            else:
                document_class._table_name = {parent_name: predefined_table_name}
            current_table_name = predefined_table_name
        # Step 2: Parse sub objects
        for key in [k for k in doc_sample.__dir__() if not k.startswith("_")]:
            field = object.__getattribute__(doc_sample, key)
            if isinstance(field, EmbeddedDocumentField):
                sub_doc_class = field.document_type_class
                # For the embedded document, we need to do iteration but shouldn't create a table
                cls._update_table_name_to_field(current_table_name, separator, sub_doc_class, table_name_dict, False)
            elif isinstance(field, ListField) and isinstance(field.field, EmbeddedDocumentField):
                sub_doc_class = field.field.document_type_class
                cls._update_table_name_to_field(current_table_name, separator, sub_doc_class, table_name_dict)
            else:
                continue

    @classmethod
    def _update_table_name_dict_from_field(cls,
                                           parent_name: str,
                                           separator: str,
                                           document_class: Type[Base],
                                           table_name_dict: dict):
        """Using when dumping address. Save Runtime data to Model data

        Args:
            parent_name: Parent table name
            separator: Default table name separator
            document_class:
            table_name_dict:

        Returns:
            table name dictionary
        """
        doc_sample = document_class.get_sample()
        for key in [k for k in doc_sample.__dir__() if not k.startswith("_")]:
            field = object.__getattribute__(doc_sample, key)
            if isinstance(field, EmbeddedDocumentField):
                sub_doc_class = field.document_type_class
                table_name = parent_name  #: No need to create table so keeping the old name
            elif isinstance(field, ListField) and isinstance(field.field, EmbeddedDocumentField):
                sub_doc_class = field.field.document_type_class
                table_name = sub_doc_class.get_meta_data().get("table_name", {}).get(parent_name, "")
                if not table_name:  # Generate table name by using defaults
                    table_name = parent_name + separator + sub_doc_class.__name__
                table_name_dict[sub_doc_class.__name__] = table_name
            else:
                continue
            cls._update_table_name_dict_from_field(table_name, separator, sub_doc_class, table_name_dict)
        return table_name_dict

    @classmethod
    def dump_address(cls, model_class: Type[BaseDocument], replica_name: str = None, domain_name: str = ""):
        """Dump address of a given model

        Args:
            model_class: The model to be parsed
            replica_name: The replica name to be used. When set to none => will use the default engine
            domain_name: The default domain name

        Returns:
            Dictionary of models
        """
        domain_name = model_class.get_meta_data().get("domain_name", domain_name)
        if not domain_name:
            raise ValueError(f"Domain Name is mandatory for dumping model {model_class.__name__}")
        model_engine = model_class._engine if not replica_name else model_class.get_replica_engines()[replica_name]
        address_param = model_class.get_address(replica_name if replica_name else model_engine)
        # Step 1: Common Fields
        object_params = {
            "domain_name": domain_name,
            "model_name": model_class.__name__,
            "address_name": address_param.pop("_db", None),
            "param_name": model_engine.engine_param,
            "engine_module": model_engine.__module__,
            "engine_class": model_engine.__name__,
            "catalog": TableCatalog.catalog_to_model(address_param.pop("_catalog", None)),
            "scope": address_param.pop("_scope", None),
        }
        # Step 2: Get table field maps
        table_dict = address_param.pop("_tables", None)
        if not table_dict:
            root_name = model_class.get_collection_name(model_engine)
            table_dict = {model_class.__name__: root_name}
            if model_engine.store_embedded_as_table:
                seperator = model_engine.TABLE_NAME_SEPARATOR
                cls._update_table_name_dict_from_field(root_name, seperator, model_class, table_dict)
        # Need a trans-code from {module: table_name} to a list
        tables = [{"sub_model_name": k, "table_name": v} for k, v in table_dict.items()]
        object_params["tables"] = tables

        # Step 3: Connector Parameters
        connector_param, other_param = {}, {}
        for key, value in address_param.items():
            if key.startswith("_"):
                other_param[key] = value
            else:
                connector_param[key] = value
        if connector_param:
            object_params["connector_param"] = connector_param
        if other_param:
            object_params["other_param"] = other_param
        # Step 4: Connector Class Type
        engine_connector_class = model_engine.engine_connector_class
        if engine_connector_class:
            object_params["connector_module"] = engine_connector_class.__module__
            object_params["connector_class"] = engine_connector_class.__name__

        # Last step: Object Creation
        result = cls.from_display(**object_params)
        return result

    @classmethod
    def upsert_address(cls, model_class: Type[BaseDocument], remove_unused: bool = False, domain_name: str = ""):
        """Update or insert model address

        Args:
            model_class: Document class
            remove_unused: Delete unused address attached to the model
            domain_name: The default domain name
        """
        address_book, to_be_deleted = {}, []
        domain_name = model_class.get_meta_data().get("domain_name", domain_name)
        if not domain_name:
            raise ValueError(f"Domain Name is mandatory for upsert model {model_class.__name__}")
        engine_address = cls.dump_address(model_class, domain_name=domain_name)
        address_book[engine_address.calculate_id()] = engine_address
        for replica_name in model_class.get_replica_engines():
            replica_address = cls.dump_address(model_class, replica_name, domain_name=domain_name)
            address_book[replica_address.calculate_id()] = replica_address
        # Update part
        for saved_address in cls.objects(domain_name=domain_name, model_name=model_class.__name__):
            address_item = address_book.pop(saved_address.get_id(), None)
            if address_item is None and remove_unused:
                to_be_deleted.append(saved_address)
            else:
                address_item._id = saved_address.get_id()
                address_item.save()
        # Insert part
        for address_item in address_book.values():
            address_item.save()
        # Delete part
        for delete_item in to_be_deleted:
            delete_item.delete()

    def assign_address(self, model_class: Type[BaseDocument], replica_name: str = None):
        """Attribute address to model

        Args:
            model_class: Model class to be imported
            replica_name: The replica name to be used. When set to none => will use the default engine
        """
        # Step 1: Check the correct class:
        if self.model_name != model_class.__name__:
            raise ValueError(f"Wrong model class: {self.model_name} != {model_class.__name__}")
        # Step 2: Check engine class and attribute the new one if not the same
        try:
            engine_module = import_module(self.engine_module)
            engine_class = getattr(engine_module, self.engine_class)
        except (ModuleNotFoundError, AttributeError):
            raise ValueError(f"Cannot import engine {self.engine_module}.{self.engine_class}")
        if replica_name:
            model_class.set_replica_engine(replica_name, engine_class)
        elif engine_class != model_class._engine:
            model_class._engine = engine_class
        # Step 3: Import Connector class
        if self.connector_module and self.connector_class:
            try:
                connector_module = import_module(self.connector_module)
                connector_class = getattr(connector_module, self.connector_class)
            except (ModuleNotFoundError, AttributeError):
                raise ValueError(f"Cannot import connector {self.connector_module}.{self.connector_class}")
            engine_class.engine_connector_class = connector_class
        # Step 4 Connection Parameter and other parameter import:
        address_dict = self.other_param if self.other_param else {}
        address_dict.update(self.connector_param if self.connector_param else {})
        # Step 5: Update embedded document table_setting
        if self.tables:
            # Transcode from table list to {module: table_name}
            table_dict = {}
            for table_config in self.tables:
                table_dict[table_config.sub_model_name] = table_config.table_name
            if engine_class.store_embedded_as_table:
                self._update_table_name_to_field("", engine_class.TABLE_NAME_SEPARATOR, model_class, table_dict)
            address_dict.update({"_tables": table_dict})
        # Step 6:
        address_dict.update({"_db": self.address_name,
                             "_catalog": TableCatalog.catalog_to_class(self.catalog),
                             "_scope": self.scope})
        if replica_name:
            model_class.set_address(replica_name, address_dict)
        else:
            engine_class.engine_param = self.param_name
            model_class.set_address(engine_class, address_dict)
