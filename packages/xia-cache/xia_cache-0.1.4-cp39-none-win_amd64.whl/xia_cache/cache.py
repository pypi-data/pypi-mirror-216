from typing import Type
from xia_engine import BaseDocument
from xia_engine import BaseCache, RamEngine, MetaCache


class Cache(BaseCache):
    """"""


class MetaRamCache(MetaCache):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls._storage = {}
        return cls

class LruRamCache(Cache, metaclass=MetaRamCache):
    lru_cache_size = 1024  # Max cache could be hold

    _storage = {}  # Object stored here

    engine_param = "lru_ram_cache"

    @classmethod
    def drop(cls, document_class: Type[BaseDocument]):
        collection_name = document_class.get_collection_name(cls)
        return RamEngine._drop(cls._storage, collection_name)

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        collection_name = document_class.get_collection_name(cls)
        doc_id = RamEngine._create(cls._storage, collection_name, db_content, doc_id)
        if len(cls._storage[collection_name]) > cls.lru_cache_size:
            cls._storage[collection_name].popitem(last=False)
        cls.record_size(collection_name)
        return doc_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        collection_name = document_class.get_collection_name(cls)
        doc_dict = RamEngine._get(cls._storage, collection_name, doc_id)
        if doc_dict is not None:
            cls._storage[collection_name].move_to_end(doc_id)
            cls.record_hit(collection_name)
        else:
            cls.record_miss(collection_name)
        return doc_dict

    @classmethod
    def _fetch(cls, storage: dict, collection_name: str, *args):
        if collection_name not in storage:
            return []
        database = storage[collection_name].copy()
        for doc_id in args:
            if doc_id in database:
                doc_dict = database[doc_id]
                if doc_dict is not None:
                    doc_dict["_id"] = doc_id
                yield doc_id, doc_dict

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        collection_name = document_class.get_collection_name(cls)
        hit_count = 0
        for doc_id, doc_dict in cls._fetch(cls._storage, collection_name, *args):
            cls._storage[collection_name].move_to_end(doc_id)
            cls.record_hit(collection_name)
            hit_count += 1
            yield doc_id, doc_dict
        for _ in range(len(args) - hit_count):
            cls.record_miss(collection_name)

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        collection_name = document_class.get_collection_name(cls)
        doc_id = RamEngine._set(cls._storage, collection_name, doc_id, db_content)
        if len(cls._storage[collection_name]) > cls.lru_cache_size:
            cls._storage[collection_name](last=False)
        cls.record_size(collection_name)
        return doc_id

    @classmethod
    def update(cls, document_class: Type[BaseDocument], doc_id: str, **kwargs) -> dict:
        collection_name = document_class.get_collection_name(cls)
        return RamEngine._update(cls._storage, collection_name, doc_id, **kwargs)

    @classmethod
    def search(cls, document_class: Type[BaseDocument], *args, **kwargs):
        collection_name = document_class.get_collection_name(cls)
        for doc_dict in RamEngine._search(cls._storage, collection_name, *args, **kwargs):
            cls._storage[collection_name].move_to_end(doc_dict["_id"])
            if len(cls._storage[collection_name]) > cls.lru_cache_size:
                cls._storage[collection_name](last=False)
            yield doc_dict

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        collection_name = document_class.get_collection_name(cls)
        return RamEngine._delete(cls._storage, collection_name, doc_id)
