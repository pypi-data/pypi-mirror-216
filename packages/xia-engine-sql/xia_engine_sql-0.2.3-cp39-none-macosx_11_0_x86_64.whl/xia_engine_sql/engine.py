import json
import uuid
from typing import Type, Union
from functools import lru_cache
import sqlite3
from xia_fields import BaseField
from xia_fields import BooleanField, FloatField, StringField, ByteField, IntField, DecimalField, DateTimeField
from xia_fields import JsonField, TimestampField, DateField, TimeField, CompressedStringField
from xia_engine import Engine, RamEngine, BaseDocument, BaseEmbeddedDocument, EmbeddedDocument
from xia_engine import ListField, EmbeddedDocumentField, ExternalField


def encode_list(value):
    if not isinstance(value, list):
        return value
    if len(value) == 0:
        return None
    elif all(isinstance(item, (str, float, int, bool, type(None))) for item in value):
        return json.dumps(value, ensure_ascii=False)
    else:
        return value


def decode_list(value):
    if value is None or not isinstance(value, str) or not value.startswith("[") and value.endswith("]"):
        return value
    return json.loads(value)


class SqlEngine(Engine):
    KEY_SEPARATOR = "|"  #: Use to generate ID by concatenate keys
    FIELD_SEPARATOR = "_"  #: Use to generate the field name in embedded documents
    TABLE_NAME_SEPARATOR = "_"  #: Use to separate the table name of embedded documents

    OPERATORS = {"__eq__": "=", "__lt__": "<", "__le__": "<=", "__gt__": ">", "__ge__": ">=", "__ne__": "!=",
                 "__in__": "IN", "__not_in__": "NOT IN"}

    key_required = True  #: SQL Engine only compatible with document with predefined primary keys
    support_unknown = False  #: SQL Engine doesn't support saving unknown fields

    store_embedded_as_table = True  #: Store embedded document as table
    engine_param: str = None  #: Engine parameter name
    engine_connector: callable = None  #: Connector function
    engine_default_connector_param: dict = {}  #: default connection parameter
    lq = '"'  #: Left quote for identifier
    rq = '"'  #: Left quote for identifier
    paramstyle = "pyformat"  # pyformat %(place_holder)s or named :place_holder

    engine_unique_check = True  #: Unique check is commonly applied in SQL Engine

    # Type dictionary to do conversion stuff
    type_dict = {}

    # Variable Name: @table_name@, @field_types@, @key_list@
    create_sql_template = "CREATE TABLE {} ( {}, PRIMARY KEY( {} ))"
    # Variable Name: @table_name@
    drop_sql_template = "DROP TABLE {}"
    # Variable Name: @fields@, @table_name@, @where_condition@
    select_sql_template = "SELECT {} FROM {} WHERE {}"
    # Variable Name: @table_name@, @fields@, @value_holders@
    insert_sql_template = "INSERT INTO {} ({}) VALUES ( {} )"
    # Variable Name: @table_name@, @where_key_holders@
    delete_sql_template = "DELETE FROM {} WHERE {}"
    # Variable Name: @table_name@
    truncate_sql_template = "TRUNCATE TABLE {}"
    # Variable; @table_name@, @field_type@
    add_column_sql_template = "ALTER TABLE {} ADD {}"

    # Variable; @data_model@, @analytic_request@
    analytic_sql_template = """WITH data_model AS ({}) {}"""

    @classmethod
    def _sql_safe(cls, statement: str) -> str:
        return statement.replace(';', '')

    @classmethod
    def _paramstyle(cls, place_holder: str):
        if cls.paramstyle == "named":
            return ":" + place_holder
        elif cls.paramstyle == "pyformat":
            return "%(" + place_holder + ")s"
        else:
            raise ValueError("param style: " + cls.paramstyle + " is not supported")

    @classmethod
    def _translate_line(cls, payload: dict, fields_map: dict):
        """Translate line for fields mapping

        Args:
            payload: The data to be translated
            fields_map: The column change rule

        Returns:
            Translated dictionary
        """
        return {fields_map.get(key, key): value for key, value in payload.items()}

    @classmethod
    def _fill_null_line(cls, payload: dict, field_list: list):
        """Fill the payload with None value (for execute manay statement)

        Args:
            payload: The data to be translated
            field_list: Full field line

        Returns:
            Filled entry
        """
        return {field: payload.get(field, None) for field in field_list}

    @classmethod
    def _parse_embedded_document(cls,
                                 field_name: str,
                                 embedded: Type[BaseEmbeddedDocument],
                                 parent_table_name: str,
                                 parent_key_fields: dict,
                                 sql_model: dict,
                                 data_model: dict,
                                 catalog: Union[dict, None]):
        """Parse embedded document

        Args:
            field_name: Embedded Document field name
            embedded: Embedded Document Class
            parent_table_name: Parent Table Name
            parent_key_fields: Parent table key fields
            sql_model: Used to generate SQL statements
            data_model: Used to parse data
            catalog: Data catalog

        Embedded documents table creation rules:
            * table_name: The new table name
            * key_fields: key to be added in the
            * fields_map: new field name
            * New tables will be created only if having table names
        """
        document_sample = embedded.get_sample()
        meta_data = embedded.get_meta_data()
        catalog = {} if catalog is None else catalog  # input parameter no mutable
        if "key_fields" in meta_data:
            # Case 1: New table should be created
            table_name = meta_data.get("table_name", {}).get(parent_table_name, "")
            table_name = table_name if table_name else parent_table_name + cls.TABLE_NAME_SEPARATOR + embedded.__name__
            # Step 1.1 Parent key fields might have a new name.
            # ATTENTION, order of parent key must be the first ! Critical for load process
            table_keys = {}
            for parent_key, parent_key_field in parent_key_fields.items():
                table_keys[meta_data.get("fields_map", {}).get(parent_key, parent_key)] = parent_key_field
            sql_model[table_name] = {}
            data_model["children"][field_name] = {
                "table_name": table_name, "keys": meta_data["key_fields"], "children": {}, "components": {},
                "fields_map": meta_data.get("fields_map", {})
            }
            # Step 1.2 Parent key fields should be included in the children's structure
            for parent_key, parent_key_field in table_keys.items():
                # Pass catalog = None because we must include parent key
                cls._parse_sql_field(parent_key, parent_key_field, table_name, parent_key_fields, True,
                                     sql_model, data_model["children"][field_name], None)
            # Step 1.3 Adding local keys
            for key_field in meta_data["key_fields"]:
                key_field_name = meta_data.get("fields_map", {}).get(key_field, key_field)
                key_field_info = object.__getattribute__(document_sample, key_field)
                table_keys[key_field_name] = key_field_info
            # Step 1.4 Iterating all fields
            for key in document_sample.__dir__():
                field = object.__getattribute__(document_sample, key)
                if not key.startswith("_") and isinstance(field, BaseField):
                    new_field_name = meta_data.get("fields_map", {}).get(key, key)
                    is_key = True if key in meta_data.get("key_fields", {}) else False
                    cls._parse_sql_field(new_field_name, field, table_name, table_keys, is_key,
                                         sql_model, data_model["children"][field_name], catalog)
        else:
            # Case 2: Use the same table
            data_model["components"][field_name] = {
                "fields_map": meta_data.get("fields_map", {}), "children": {}, "components": {}
            }
            for key in document_sample.__dir__():
                field = object.__getattribute__(document_sample, key)
                if not key.startswith("_") and isinstance(field, BaseField):
                    if isinstance(field, (ListField, EmbeddedDocumentField)):
                        sub_fld_name = key
                    else:
                        sub_fld_name = meta_data.get("fields_map", {}).get(key, field_name + cls.FIELD_SEPARATOR + key)
                    data_model["components"][field_name]["fields_map"][key] = sub_fld_name
                    if key in catalog:  # Need to adjust the catalog to use the new field name
                        catalog = catalog.copy()  # Do not touch the original catalog
                        catalog[sub_fld_name] = catalog.pop(key)
                    is_key = True if key in meta_data.get("key_fields", {}) else False
                    cls._parse_sql_field(sub_fld_name, field, parent_table_name, parent_key_fields, is_key,
                                         sql_model, data_model["components"][field_name], catalog)

    @classmethod
    def _parse_sql_field(cls, field_name: str, field: BaseField, parent_table_name: str,
                         key_fields: dict, is_key: bool, sql_model: dict, data_model: dict, catalog: Union[dict, None]):
        """ Par a field into SQL compatible objects

        Args:
            field_name: field name
            field: field object
            parent_table_name: the parent table name (holder of embedded document)
            key_fields: key fields of tables
            is_key: If the field is key
            sql_model: SQL model to be updated
            data_model: Data model to be used to parse data
            catalog: data catalog
        """
        if catalog and field_name not in catalog and not is_key:
            # Ignore case: Not in catalog and not a key fields
            return
        catalog = {} if catalog is None else catalog  # input parameter no mutable
        if isinstance(field, ListField):
            item_field = field.field
            if isinstance(item_field, EmbeddedDocumentField):
                # Case 1: Embedded Document Field as list
                cls._parse_embedded_document(field_name, item_field.document_type_class,
                                             parent_table_name, key_fields, sql_model, data_model,
                                             catalog.get(field_name, None))
                return
            # Case 2: Other list field should be treated as string (jsonify before saving to database)
            field_info = {"key": is_key, "info": item_field, "type": cls.type_dict[StringField]}
        elif isinstance(field, EmbeddedDocumentField):
            # Case 3: Normal EmbeddedDocument field
            cls._parse_embedded_document(field_name, field.document_type_class, parent_table_name,
                                         key_fields, sql_model, data_model, catalog.get(field_name, None))
            return
        elif isinstance(field, ExternalField):
            # Case 4: External Field => Nothing to do at Engine level
            return
        else:
            field_info = {"key": is_key, "info": field}
            for dict_class, field_type in cls.type_dict.items():
                if isinstance(field, dict_class):
                    field_info["type"] = field_type
        sql_model[parent_table_name][field_name] = field_info

    @classmethod
    @lru_cache(maxsize=1024)
    def _parse_sql_model(cls, document_class: Type[BaseDocument]):
        """Parse SQL Model

        Args:
            document_class (object): Meta class to extract information

        Returns:
            A dictionary about all table to be created:
                {"table_name": {"field_name": {"key": boolean, "info": Field Object, "type": SQL Type}}}
            A dictionary to be used to parse data
        """
        document_sample = document_class.get_sample()
        table_name = document_class.get_collection_name(document_class._engine)
        sql_model = {table_name: {}}
        key_fields = document_class.get_meta_data()["key_fields"]
        catalog = document_class.get_address(cls).get("_catalog", None)
        key_fields = {key_field: object.__getattribute__(document_sample, key_field) for key_field in key_fields}
        data_model = {"": {"table_name": table_name, "keys": list(key_fields), "children": {}, "components": {}}}
        for key in list(key_fields) + [item for item in document_sample.__dir__() if item not in key_fields]:
            # Parse key fields at first
            field = object.__getattribute__(document_sample, key)
            if not key.startswith("_") and isinstance(field, BaseField):
                is_key = True if key in key_fields else False
                cls._parse_sql_field(key, field, table_name, key_fields, is_key, sql_model, data_model[""], catalog)
        return sql_model, data_model

    @classmethod
    def parse_data(cls, db_content: dict, data_model: dict, key_value: dict, data_content: dict):
        """Split database content to multiple table update instruction

        Args:
            db_content: Data base content of document
            data_model: Parsed data model
            key_value: The key value should be added
            data_content: Data content to be added

        Returns:
            Parsed data content
        """
        current_key_value = key_value.copy()
        current_key_value.update({key: db_content[key] for key in data_model.get("keys", [])})
        if data_model.get("fields_map", {}):  # Translate key values
            current_key_value = cls._translate_line(current_key_value, data_model["fields_map"])
        for child_name, child_model in data_model.get("children", {}).items():
            child_content = db_content.pop(child_name, None)
            if child_content:
                if child_model["table_name"] not in data_content:
                    data_content[child_model["table_name"]] = []
                if isinstance(child_content, list):
                    for child_line in child_content:
                        cls.parse_data(child_line, child_model, current_key_value, data_content)
                elif isinstance(child_content, dict):
                    cls.parse_data(child_content, child_model, current_key_value, data_content)
        # After treating children's value, could get all values
        # Part 1: Key value
        data_line = current_key_value.copy()
        # Part 2: Flatten fields on embedded fields
        for component_name, component_model in data_model.get("components", {}).items():
            component_content = db_content.pop(component_name, None)
            if component_content:
                data_line.update(cls._translate_line(component_content, component_model.get("fields_map", {})))
                component_data = cls.parse_data(component_content, component_model, current_key_value, data_content)
        # Part 3: Normal fields
        if data_model.get("fields_map", {}):
            data_line.update(cls._translate_line(db_content, data_model["fields_map"]))
        else:
            data_line.update(db_content)
        if "table_name" in data_model:  # Children case
            data_content[data_model["table_name"]].append(data_line)
            return data_content
        else:  # Component cases
            return data_line

    @classmethod
    def _parse_content_component(cls, data_content: dict, result: dict, target_line: dict, data_model: dict,
                                 key_values: dict):
        """ Should take care component of component cases

        Args:
            result: a flat result line
            target_line: target (component of dictionary to assign value)
            data_model: component data model
        """
        for component_name, component_model in data_model.get("components", {}).items():
            target_line[component_name] = {}
            # Parse inner components
            cls._parse_content_component(data_content, result, result[component_name], component_model, key_values)
            # Par inner children
            child_kv = key_values.copy()
            child_kv.update({k: result.get(k, None) for k in data_model.get("keys", [])})
            cls._parse_content_children(data_content, target_line[component_name], component_model, child_kv)
            for origin, target in component_model.get("fields_map", {}).items():
                if target in result:
                    target_line[component_name][origin] = result.pop(target)

    @classmethod
    def _parse_content_children(cls, data_content: dict, result: dict, data_model: dict, key_values: dict):
        for child_name, child_info in data_model.get("children", {}).items():
            child_kv = key_values.copy()
            child_kv.update({k: result.get(k, None) for k in data_model.get("keys", [])})
            child_kv = {child_info.get("fields_map", {}).get(k, k): v for k, v in child_kv.items()}
            result[child_name] = cls.parse_content(data_content, child_info, child_kv)

    @classmethod
    def parse_content(cls, data_content: dict, data_model: dict, key_values: dict):
        """Parse database result to db content (json format)

        Args:
            data_content: dictionary of entries for each table
            data_model: Parsed data model
            key_values: Key value to be filtered

        Result:
            db form of data
        """
        results = data_content.get(data_model["table_name"], [])
        results = [result for result in results if all([kv in result.items() for kv in key_values.items()])]
        for result in results:
            # Step 1: Recover components
            cls._parse_content_component(data_content, result, result, data_model, key_values)
            # Step 2: Recover children
            cls._parse_content_children(data_content, result, data_model, key_values)
            # Cleanse
            cleared = {k: v for k, v in result.items() if v is not None and k not in key_values}
            reversed_map = {v: k for k, v in data_model.get("fields_map", {}).items()}
            translated = cls._translate_line(cleared, reversed_map)
            result.clear()
            result.update(translated)
        return results

    @classmethod
    def _get_insert_sql(cls, table_name: str, table_model: dict):
        return cls.insert_sql_template.format(
            cls._sql_safe(table_name),
            cls._sql_safe(", ".join([cls.lq + item + cls.rq for item in table_model])),
            cls._sql_safe(", ".join([cls._paramstyle(item) for item in table_model]))
        )

    @classmethod
    def _get_join_sql(cls, data_model: dict, parent_key: list):
        join_statements = []
        for child_name, child_info in data_model["children"].items():
            join_statement = 'LEFT OUTER JOIN ' + cls.lq + child_info["table_name"] + cls.rq + ' ON '
            join_parts = []
            for key in parent_key + data_model.get("keys", []):
                join_part = cls.lq + data_model["table_name"] + cls.rq + '.' + cls.lq + key + cls.rq + ' = ' + cls.lq
                join_part += child_info["table_name"] + cls.rq + '.' + cls.lq
                join_part += child_info.get("fields_map", {}).get(key, key) + cls.rq
                join_parts.append(join_part)
            join_statement += " AND ".join(join_parts)
            join_statements.append(join_statement)
            if child_info.get("children"):
                new_keys = [child_info.get("fields_map", {}).get(k, k) for k in parent_key + data_model.get("keys", [])]
                join_statements.extend(cls._get_join_sql(child_info, new_keys))
        return join_statements

    @classmethod
    def _get_sql_field_from_field(cls, data_model: dict, field_name: str):
        """Get SQL field from field name from search string

        Args:
            data_model: Parsed data model
            field_name: field name as a.b.c
        """
        fields = field_name.split(".")
        current_data_mode = data_model
        table_name = current_data_mode["table_name"]
        field_name = ""
        for field in fields:
            if field in current_data_mode.get("children", {}):
                current_data_mode = current_data_mode["children"][field]
                table_name = current_data_mode["table_name"]
            elif field in current_data_mode.get("components", {}):
                current_data_mode = current_data_mode["components"][field]
            else:
                field_name = current_data_mode.get("fields_map", {}).get(field, field)
        return cls.lq + table_name + cls.rq + '.' + cls.lq + field_name + cls.rq

    @classmethod
    def _get_condition_sql(cls, data_model, key, value):
        field, operator, order = cls.parse_search_option(key)
        sql_path = cls._get_sql_field_from_field(data_model, field)
        place_holder = str(uuid.uuid4()).replace("-", "")
        place_values = {place_holder: value}
        place_holder = cls._paramstyle(place_holder)
        if isinstance(value, list):
            place_values = {str(uuid.uuid4()).replace("-", ""): place_value for place_value in value}
            place_holder = "(" + ", ".join([cls._paramstyle(place_value) for place_value in place_values]) + ")"
        return " ".join([sql_path, operator, place_holder]), place_values

    @classmethod
    def get_model_sql(cls, document_class: Type[BaseDocument], model_condition: dict, acl_condition: dict = None):
        """Get SQL to be executed by using provided data model

        Args:
            document_class: document_class
            model_condition: Search criteria defined by model
            acl_condition: Search condition given by acl

        Returns:
            SQL statement and the values to be put in the place holder
        """
        sql_model, data_model = cls._parse_sql_model(document_class)
        data_model = data_model[""]
        acl_condition = {} if not acl_condition else acl_condition
        join_statements = cls._get_join_sql(data_model, [])
        where_statements = ["1 = 1"]
        place_values = {}
        for key, value in list(model_condition.items()) + list(acl_condition.items()):
            where_statement, temp_values = cls._get_condition_sql(data_model, key, value)
            where_statements.append(where_statement)
            place_values.update(temp_values)
        search_statement = cls.select_sql_template.format(
            cls._sql_safe("*"),
            cls._sql_safe(cls.lq + data_model["table_name"] + cls.rq + ' ' + "\n".join(join_statements)),
            cls._sql_safe(" AND ".join(where_statements))
        )
        return search_statement, place_values

    @classmethod
    def get_search_sql(cls, document_class: Type[BaseDocument], _acl_queries: list, _limit: int, **kwargs):
        """Get SQL to be executed by using provided data model

        Args:
            document_class: document_class
            _acl_queries: User Access List Queries
            _limit: Data limit
            **kwargs: Search criteria

        Returns:
            SQL statement and the values to be put in the place holder
        """
        _acl_queries = [{}] if not _acl_queries else _acl_queries
        sql_model, data_model = cls._parse_sql_model(document_class)
        data_model = data_model[""]
        root_keys = [cls.lq + data_model["table_name"] + cls.rq + '.' + cls.lq + key + cls.rq
                     for key in data_model["keys"]]
        join_statements = cls._get_join_sql(data_model, [])
        where_statements = ["1 = 1"]
        place_values = {}
        for key, value in kwargs.items():
            where_statement, temp_values = cls._get_condition_sql(data_model, key, value)
            where_statements.append(where_statement)
            place_values.update(temp_values)
        # _acl_query statements apply
        query_conditions = []
        for query in _acl_queries:
            conditions = []
            for key, value in query.items():
                sql_value = value if isinstance(value, (int, float)) else "'" + value + "'"
                key_value = cls.lq + key + cls.rq
                conditions.append(f"{key_value} = {sql_value}")
            if conditions:
                query_conditions.append(" AND ".join(conditions))
        if query_conditions:
            where_statements.append(f"({' OR '.join(query_conditions)})")
        search_statement = cls.select_sql_template.format(
            cls._sql_safe("DISTINCT " + ", ".join(root_keys)),
            cls._sql_safe(cls.lq + data_model["table_name"] + cls.rq + ' ' + "\n".join(join_statements)),
            cls._sql_safe(" AND ".join(where_statements))
        )
        search_statement += " LIMIT " + cls._sql_safe(str(_limit))
        return search_statement, place_values

    @classmethod
    def _create_sql_field_list(cls, field_list):
        """Field list in create sql template

        Args:
            field_list: list of field information
        """
        raise NotImplementedError

    @classmethod
    def _create_sql_key_list(cls, field_dict: dict):
        """Primary list in create sql template

        Args:
            field_dict: list of field information
        """
        key_list = ", ".join([cls.lq + name + cls.rq for name, info in field_dict.items() if info['key']])
        return key_list

    @classmethod
    def create_collection(cls, document_class: Type[BaseDocument]):
        sql_model, data_model = cls._parse_sql_model(document_class)
        for table_name, table_model in sql_model.items():
            cls.create_table(table_name, sql_model[table_name], document_class)

    @classmethod
    def create_table(cls, table_name: str, field_dict: dict, document_class: Type[BaseDocument]):
        """Create table

        Args:
            table_name: table name to be created
            field_dict: dictionary of field information
            document_class: document_class
        """
        cur = cls.get_connection(document_class).cursor()
        create_statement = cls.create_sql_template.format(
            cls._sql_safe(table_name),
            cls._sql_safe(",\n ".join(cls._create_sql_field_list(field_dict))),
            cls._sql_safe(cls._create_sql_key_list(field_dict))
        )
        cur.execute(create_statement)
        cur.close()

    @classmethod
    def _create(cls, db_con: object, document_class: Type[BaseDocument], db_content: dict):
        """Create new entry of database (one entry)

        Args:
            db_con: Database Connection
            document_class: document_class
            db_content: Data in db form

        Returns:
            Created document id
        """
        raise NotImplementedError

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        db_con = cls.get_connection(document_class)
        cls._create(db_con, document_class, db_content)
        db_con.commit()  # Commit at the end
        return doc_id

    @classmethod
    def scan(cls, _document_class: Type[BaseDocument], _acl_queries: list = None, _limit: int = 1000, **kwargs):
        db_con = cls.get_connection(_document_class)
        sql_model, data_model = cls._parse_sql_model(_document_class)
        # Search by criteria.
        search_sql, place_values = cls.get_search_sql(_document_class, _acl_queries=_acl_queries,
                                                      _limit=_limit, **kwargs)
        cur = db_con.cursor()
        cur.execute(search_sql, place_values)
        results = cur.fetchall()
        if results:
            key_values_list = [dict(zip(data_model[""]["keys"], result)) for result in results]
            return [_document_class.dict_to_id(kv) for kv in key_values_list]
        else:
            return []

    @classmethod
    def search(cls, _document_class: Type[BaseDocument], *args, _acl_queries: list = None,
               _limit: int = 50, **kwargs):
        db_con = cls.get_connection(_document_class)
        sql_model, data_model = cls._parse_sql_model(_document_class)
        data_content = {}
        if args:
            # Search by a list of document id => search by primary key.
            for doc_id in [arg for arg in args if arg]:
                key_values = _document_class.id_to_dict(doc_id)
                for table_name, table_model in sql_model.items():
                    where_conditions = []
                    for idx, item in enumerate(key_values):
                        # TODO: Better way of deal key fields mapping
                        where_condition = cls.lq + list(table_model)[idx] + cls.rq + ' = ' + cls._paramstyle(item)
                        where_conditions.append(where_condition)
                    select_key_statement = cls.select_sql_template.format(
                        "*",
                        cls._sql_safe(table_name),
                        cls._sql_safe(" AND ".join(where_conditions))
                    )
                    cur = db_con.cursor()
                    cur.execute(select_key_statement, key_values)
                    results = cur.fetchall()
                    data_content[table_name] = [dict(zip(list(table_model), result)) for result in results]
                doc_dicts = cls.parse_content(data_content, data_model[""], {})
                for doc_dict in doc_dicts:
                    doc_dict["_id"] = _document_class.dict_to_id(key_values)
                    yield doc_dict
        else:
            # Search by criteria.
            id_args = cls.scan(_document_class, **kwargs)
            for doc_dict in cls.search(_document_class, *id_args):
                yield doc_dict

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str):
        for doc_dict in cls.search(document_class, doc_id):
            return doc_dict

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        cls._delete(db_con, document_class, doc_id)
        doc_id = cls._create(db_con, document_class, db_content)
        db_con.commit()
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        old_content = cls.get(_document_class, _doc_id)
        if not old_content:
            return {}
        ram_doc_id = RamEngine.create(_document_class, old_content)
        new_content = RamEngine.update(_document_class, ram_doc_id, **kwargs)
        RamEngine.delete(_document_class, ram_doc_id)
        cls.set(_document_class, _doc_id, new_content)
        return new_content

    @classmethod
    def _delete(cls, db_con, document_class: Type[BaseDocument], doc_id: str):
        sql_model, data_model = cls._parse_sql_model(document_class)
        key_values = document_class.id_to_dict(doc_id)
        for table_name, table_model in sql_model.items():
            where_conditions = []
            for idx, item in enumerate(key_values):
                # TODO: Better way of deal key fields mapping
                where_condition = cls.lq + list(table_model)[idx] + cls.rq + ' = ' + cls._paramstyle(item)
                where_conditions.append(where_condition)
            delete_key_statement = cls.delete_sql_template.format(
                cls._sql_safe(table_name),
                cls._sql_safe(" AND ".join(where_conditions))
            )
            cur = db_con.cursor()
            cur.execute(delete_key_statement, key_values)

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        if not doc_id:
            return  # Nothing to delete
        db_con = cls.get_connection(document_class)
        cls._delete(db_con, document_class, doc_id)
        db_con.commit()

    @classmethod
    def drop(cls, document_class: Type[BaseDocument]):
        cur = cls.get_connection(document_class).cursor()
        sql_model, _ = cls._parse_sql_model(document_class)
        for table_name in sql_model:
            drop_statement = cls.drop_sql_template.format(cls._sql_safe(table_name))
            cur.execute(drop_statement)
        cur.close()

    @classmethod
    def truncate(cls, document_class: Type[BaseDocument]):
        cur = cls.get_connection(document_class).cursor()
        sql_model, _ = cls._parse_sql_model(document_class)
        for table_name in sql_model:
            drop_statement = cls.truncate_sql_template.format(cls._sql_safe(table_name))
            cur.execute(drop_statement)
        cur.close()

    @classmethod
    def _check_analytic_statement(cls, analytic_statement: str, data_model_name: str):
        data_sources = analytic_statement.split("FROM")
        if len(data_sources) <= 1:
            raise ValueError("Need from clause in analytic statement")
        for data_source in data_sources[1:]:
            if not data_source.strip().startswith(data_model_name):
                raise ValueError("Analytic module cannot get data from other data model")
        if not analytic_statement.strip().startswith("SELECT"):
            raise ValueError("Only DML is supported for analytic module")

    @classmethod
    def compile(cls, document_class: Type[BaseDocument], analytic_request: dict, acl_condition=None):
        """Compile the analysis request

        Args:
            document_class (`subclass` of `BaseDocument`): Document definition
            analytic_request: analytic request
            acl_condition: Extra where condition given by user acl objects

        Returns:
            A analytic model which could be executed by the engine
        """
        analytic_model = super().compile(document_class, analytic_request, acl_condition)
        if not analytic_model:
            # Using default compiler
            sql_statement = analytic_request.get("sql", "")
            sql_statement = sql_statement.split(";")[0] + ";"  # Multiple instruction is not supported in native mode
            data_model_name = analytic_request.get("model", "data_model")
            cls._check_analytic_statement(sql_statement.upper(), data_model_name.upper())
            model_condition = analytic_request.get("payload", {})
            source_statement, source_values = cls.get_model_sql(document_class, model_condition, acl_condition)
            if sql_statement:
                final_statement = cls.analytic_sql_template.format(source_statement, sql_statement)
                return {cls: {"sql": final_statement, "values": source_values}}
            return {cls: {}}
        return analytic_model

    @classmethod
    def analyze(cls, document_class: Type[BaseDocument], analytic_model: dict) -> list:
        """Run the analytic model

        Args:
            analytic_model: Analyze model
            document_class: (`subclass` of `BaseDocument`): Document definition

        Returns:
            Result as list of dictionary
        """
        analytic_statement = analytic_model.get(cls, {}).get("sql", None)
        if analytic_statement:
            db_con = cls.get_connection(document_class)
            cur = db_con.cursor()
            cur.execute(analytic_statement, analytic_model.get(cls, {}).get("values", {}))
            columns = [item[0] for item in cur.description]
            results = [dict(zip(columns, line)) for line in cur.fetchall()]
            cur.close()
            return results
        return []


class SqliteConnectParam(EmbeddedDocument):
    database: str = StringField(description="The path to the database file to be opened.", default=":memory:")
    timeout: float = FloatField(description="How many seconds the connection should wait before raising an exception",
                                default=5.0)
    detect_types: int = IntField(description="Control whether and how data types not natively supported by SQLite are "
                                             "looked up to be converted to Python types",
                                 default=0)
    isolation_level: str = StringField(description="Controlling whether and how transactions are implicitly opened.",
                                       choices=["DEFERRED", "EXCLUSIVE", "IMMEDIATE", None],
                                       default="DEFERRED")
    check_same_thread: str = BooleanField(description="If False, the connection may be accessed in multiple threads",
                                          default=False)
    cached_statements: int = IntField(description="The number of statements that sqlite3 should internally cache",
                                      default=128)
    uri: str = BooleanField(description="If set to True, database is interpreted as a URI with a file path",
                            default=False)


class SqliteEngine(SqlEngine):
    """SQLite Engine

    Connection Parameters:
        * Should be hold in the class attribute class._sqlite = {"db": "", "path": ""}
            * db: Database name, default database name is ""
            * kwargs: Parameter to be used
    """

    _database = {}

    engine_param = "sqlite"
    engine_connector = sqlite3.connect
    engine_default_connector_param = {"database": ":memory:"}
    engine_connector_class = SqliteConnectParam
    paramstyle = "named"

    # Simple Dictionary Match
    type_dict = {
        # Extension Type Part
        TimestampField: "REAL",
        DateField: "INTEGER",
        TimeField: "REAL",
        DateTimeField: "REAL",
        # Generic Type Part
        FloatField: "REAL",
        IntField: "INTEGER",
        DecimalField: "TEXT",
        BooleanField: "INTEGER",
        StringField: "TEXT",
        CompressedStringField: "BLOB",
        ByteField: "BLOB",
        JsonField: "TEXT",
    }

    # Encoder / Decoder
    encoders = {
        DateField: lambda x: 2440588 + x,
        TimeField: lambda x: x / 86400.0 + 0.5,
        ListField: encode_list
    }

    decoders = {
        DateField: lambda x: x - 2440588,
        TimeField: lambda x: (x - 0.5) * 86400.0,
        ListField: decode_list
    }

    # IF NOT EXISTS key word supports ignore table already exists error
    create_sql_template = "CREATE TABLE IF NOT EXISTS {} ( {}, PRIMARY KEY( {} ))"
    # IF EXISTS key word supports drop an not-existed table
    drop_sql_template = "DROP TABLE IF EXISTS {}"
    # SQLite specific TRUNCATE optimizer to the DELETE statement
    truncate_sql_template = "DELETE FROM {}"

    @classmethod
    def _create_sql_field_list(cls, field_dict: dict):
        field_types = []
        for field_name, field_info in field_dict.items():
            field_line_list = [cls.lq + cls._sql_safe(field_name) + cls.lq + ' ' + field_info["type"]]
            if field_info["info"].default is not None:
                if isinstance(field_info["info"].default, str):
                    field_line_list.append("DEFAULT '" + cls._sql_safe(field_info["info"].default) + "'")
                elif isinstance(field_info["info"].default, (int, float)):
                    field_line_list.append("DEFAULT " + str(field_info["info"].default))
            field_line = ' '.join(field_line_list)
            field_types.append(field_line)
        return field_types

    @classmethod
    def _create(cls, db_con: sqlite3.Connection, document_class: Type[BaseDocument], db_content: dict):
        sql_model, data_model = cls._parse_sql_model(document_class)
        data_content = {document_class.get_collection_name(document_class._engine): []}
        data_content = cls.parse_data(db_content, data_model[""], {}, data_content)
        for table_name, insert_content in data_content.items():
            table_model = sql_model[table_name]
            insert_statement = cls._get_insert_sql(table_name, table_model)
            insert_content = [cls._fill_null_line(line, list(table_model)) for line in data_content[table_name]]
            try:
                db_con.cursor().executemany(insert_statement, insert_content)
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    # Crisis 1: No table found, so we need to add a table
                    cls.create_table(table_name, sql_model[table_name], document_class)
                    db_con.cursor().executemany(insert_statement, insert_content)
                elif "no column named" in str(e):
                    # Crisis 2: Some extra column found
                    for column_info in cls._create_sql_field_list(sql_model[table_name]):
                        add_col_statement = cls.add_column_sql_template.format(
                            cls._sql_safe(table_name),
                            cls._sql_safe(column_info)
                        )
                        try:
                            db_con.cursor().execute(add_col_statement)
                        except sqlite3.OperationalError:  # could ignore errors if column exists
                            pass
                    db_con.cursor().executemany(insert_statement, insert_content)
                else:
                    raise e
