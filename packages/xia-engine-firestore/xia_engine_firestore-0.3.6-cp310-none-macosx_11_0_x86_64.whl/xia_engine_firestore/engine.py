from typing import Type
from google.cloud import firestore
from google.cloud.exceptions import GoogleCloudError
from google.cloud.firestore_v1.field_path import FieldPath
from xia_engine import Engine, BaseDocument
from xia_engine import result_limiter


class FirestoreEngine(Engine):
    """XIA Document Engine based on Firestore
    """
    engine_param = "firestore"
    engine_connector = firestore.Client

    OPERATORS = {"__lt__": "<", "__le__": "<=", "__gt__": ">", "__ge__": ">=", "__ne__": "!=",
                 "__contains__": "array_contains", "__in__": "in", "__not_in__": "not-in"}

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        if doc_id is None:
            ts, doc_ref = db_con.collection(collection_name).add(db_content)
            return doc_ref.id
        else:
            doc_ref = db_con.collection(collection_name).document(doc_id)
            doc_ref.set(db_content)
            return doc_ref.id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str):
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        doc_ref = db_con.collection(collection_name).document(doc_id).get()
        if doc_ref.exists:
            doc_dict = doc_ref.to_dict()
            doc_dict["_id"] = doc_ref.id
            return doc_dict

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict):
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        doc_ref = db_con.collection(collection_name).document(doc_id)
        doc_ref.set(db_content)
        return doc_ref.id

    @classmethod
    def _get_update_config(cls, **kwargs):
        update_config = {}
        for key, value in kwargs.items():
            field, operator = cls.parse_update_option(key)
            if operator is None:
                update_config[field] = value
            elif operator == "append":
                if isinstance(value, list):
                    update_config[field] = firestore.ArrayUnion(value)
                else:
                    update_config[field] = firestore.ArrayUnion([value])
            elif operator == "remove":
                if isinstance(value, list):
                    update_config[field] = firestore.ArrayRemove(value)
                else:
                    update_config[field] = firestore.ArrayRemove([value])
            elif operator == "delete":
                update_config[field] = firestore.DELETE_FIELD
        return update_config

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs):
        collection_name = _document_class.get_collection_name(cls)
        if not _doc_id:
            raise ValueError(f"Document id must be provided to update collection {collection_name}")
        db_con = cls.get_connection(_document_class)
        update_config = cls._get_update_config(**kwargs)
        doc_ref = db_con.collection(collection_name).document(_doc_id).get()
        if doc_ref.exists:
            doc_ref.reference.update(update_config)
            doc_dict = doc_ref.reference.get().to_dict()
            doc_dict["_id"] = doc_ref.id
            return doc_dict
        raise ValueError(f"Document id {_doc_id} not found in the collection {collection_name}")

    @classmethod
    def _search_append_criteria(cls, sub_collection, list_presents: bool, **kwargs):
        for key, value in kwargs.items():
            if not isinstance(value, (str, int, float, list)):
                raise TypeError(f"Value {value} is not supported during load")
            if isinstance(value, list):
                if list_presents:
                    raise ValueError("Firestore doesn't support two list operation at the same time")
                sub_collection = sub_collection.where(key, "array_contains_any", value)
                list_presents = True
            else:
                field, operator, order = cls.parse_search_option(key)
                sub_collection = sub_collection.where(field, operator, value)
        return sub_collection, list_presents

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        if not args:
            return []
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        sub_collection = collection = db_con.collection(collection_name)
        for doc_id in args:
            # Try to find the document with the primary key / value combinaison
            found = False
            if document_class._key_fields:
                try:
                    kwargs = document_class.id_to_dict(doc_id)
                    for key, value in kwargs.items():
                        sub_collection = sub_collection.where(key, "==", value)
                    for doc_ref in sub_collection.stream():
                        doc_dict = doc_ref.to_dict()
                        doc_dict["_id"] = doc_ref.id
                        yield doc_ref.id, doc_dict
                        found = True
                except Exception:
                    pass
            if not found:
                doc_ref = collection.document(doc_id).get()
                if doc_ref.exists:
                    doc_dict = doc_ref.to_dict()
                    doc_dict["_id"] = doc_ref.id
                    yield doc_ref.id, doc_dict

    @classmethod
    @result_limiter
    def search(cls, _document_class: Type[BaseDocument], *args, _acl_queries: list = None, _limit: int = 50, **kwargs):
        _acl_queries = [{}] if not _acl_queries else _acl_queries
        if args:
            # Search by a list of document id => Firestore accept only one list so we do loop at id, likely one item.
            for doc_id, doc_dict in cls.fetch(_document_class, *args):
                if cls._acl_query_filter(BaseDocument, _acl_queries, doc_dict):
                    yield doc_dict  # Pass dummy Document instance because no conversion is needed for RamEngine
        else:
            collection_name = _document_class.get_collection_name(cls)
            db_con = cls.get_connection(_document_class)
            sub_collection = db_con.collection(collection_name)
            list_presents = False
            sub_collection, list_presents = cls._search_append_criteria(sub_collection, list_presents, **kwargs)
            # A cheap optimization: If _acl_queries has only one entry, we could append it safely
            if len(_acl_queries) == 1:
                sub_collection, _ = cls._search_append_criteria(sub_collection, list_presents, **_acl_queries[0])
            for doc_ref in sub_collection.stream():
                doc_dict = doc_ref.to_dict()
                if cls._acl_query_filter(BaseDocument, _acl_queries, doc_dict):
                    doc_dict["_id"] = doc_ref.id
                    yield doc_dict  # Pass dummy Document instance because no conversion is needed for RamEngine

    @staticmethod
    def _update_doc_id(transaction, old_doc_ref, new_doc_ref):
        doc = old_doc_ref.get(transaction=transaction)
        new_doc_ref.set(doc.to_dict())
        old_doc_ref.delete()

    @classmethod
    def update_doc_id(cls, document_class: Type[BaseDocument], db_content: dict, old_id: str, new_id: str):
        db_con = cls.get_connection(document_class)
        collection_name = document_class.get_collection_name(cls)
        batch = db_con.batch()
        old_doc_ref = db_con.collection(collection_name).document(old_id)
        new_doc_ref = db_con.collection(collection_name).document(new_id)
        batch.set(new_doc_ref, db_content)
        batch.delete(old_doc_ref)

        try:
            batch.commit()
            return new_id
        except GoogleCloudError:
            return old_id

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        doc = db_con.collection(collection_name).document(doc_id).get()
        if doc.exists:
            doc.reference.delete()

    @classmethod
    def batch(cls, operations: list, originals: dict):
        if not operations:
            return True, ""  # Empty operation list and nothing to do
        db_con = cls.get_connection(operations[0]["cls"])  # Get the address of the first database connection
        db_batch = db_con.batch()
        for operation in operations:
            collection_name = operation["cls"].get_collection_name(cls)
            doc_ref = db_con.collection(collection_name).document(operation["doc_id"])
            if operation["op"] in ["I", "S"]:
                db_batch.set(doc_ref, operation["content"])
            elif operation["op"] == "U":
                db_batch.update(doc_ref, cls._get_update_config(**operation["content"]))
            elif operation["op"] == "D":
                db_batch.delete(doc_ref)
        try:
            db_batch.commit()
        except Exception as e:
            return False, str(e)
        return True, ""

    @classmethod
    def drop(cls, document_class: Type[BaseDocument]):
        collection_name = document_class.get_collection_name(cls)
        db_con = cls.get_connection(document_class)
        docs = db_con.collection(collection_name).list_documents(page_size=1000)
        deleted = 0
        for doc in docs:
            doc.delete()
            deleted = deleted + 1
        if deleted >= 1000:
            return cls.drop(document_class)

    @classmethod
    def truncate(cls, document_class: Type[BaseDocument]):
        return cls.drop(document_class)
