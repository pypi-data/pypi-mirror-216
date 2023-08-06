from __future__ import annotations

import json
import logging
import os
from typing import Dict, Type, List

import pydash
from couchdb import ResourceConflict
from pydantic import BaseModel, Field

import couchdb
from pydantic_db_backend.backend import BackendBase, BackendModel
from pydantic_db_backend.exceptions import RevisionConflict, NotFound, AlreadyExists
from pydantic_db_backend.utils import CustomJSONEncoder

log = logging.getLogger(__name__)


class CouchDbBackend(BackendBase):
    # _collections: Dict[Type[BaseModel], str] = {}
    _indexes: Dict[str, List[dict]] = {}
    _connections: Dict[str, CouchDbConnectionModel] = {}

    @classmethod
    def startup(cls, alias: str | None = "default", uri: str | None = None):
        super().startup()
        if uri is None:
            uri = os.environ.get('COUCHDB_URI', None)
            if uri is None:
                raise EnvironmentError("COUCHDB_URI not set.")

        cls._connections[alias] = CouchDbConnectionModel(
            alias=alias,
            uri=uri,
            server=couchdb.Server(uri)
        )

    @classmethod
    def to_db(cls, instance: BackendModel, json_dict: bool | None = True) -> dict:
        document = super().to_db(instance)
        document = pydash.omit(document | {"_id": document['uid'], "_rev": document['revision']}, "uid", "revision")
        return document

    @classmethod
    def from_db(cls, model: Type[BackendModel], document: dict, json_dict: bool | None = True) -> BackendModel:
        document = pydash.omit(
            document | {
                "uid": document['_id'],
                "revision": document['_rev']
            },
            "_id", "_rev"
        )
        return super().from_db(model, document)

    # noinspection PyMethodOverriding
    @classmethod
    def create_index(cls, collection_name: str, index_name: str, index_spec: list, db: couchdb.Database):
        super().create_index(collection_name, index_name, index_spec)
        i = (collection_name, index_name)
        indexes = db.index()
        if i not in indexes:
            indexes[i] = index_spec

    @classmethod
    def get_db(cls, model: Type[BackendModel]) -> couchdb.Database:
        db_name = cls.collection_name(model)

        with cls.alias() as alias:
            con = cls._connections[alias]

            if db_name in con.server:
                db = con.server[db_name]
            else:
                db = con.server.create(db_name)
            cls.indexes(model, dict(db=db))
        return db

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        db = cls.get_db(model)
        entry = db.get(uid)
        if entry is None:
            raise NotFound(uid)
        return cls.from_db(model, entry)

    @classmethod
    def post_document(cls, model: Type[BackendModel], document: dict) -> Dict:
        db = cls.get_db(model)
        try:
            db.save(pydash.omit(document, "_rev"))
        except ResourceConflict as e:
            raise AlreadyExists(uid=document["_id"])
        return db.get(document['_id'])

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        document = cls.to_db(instance)

        document = cls.post_document(instance.__class__, document)
        return cls.from_db(instance.__class__, document)

    @classmethod
    def put_instance(cls, instance: BackendModel, ignore_revision_conflict: bool = False) -> BackendModel:
        db = cls.get_db(instance.__class__)
        if instance.uid in db:
            document = cls.to_db(instance)
            while True:
                try:
                    id, rev = db.save(document)
                    document['_rev'] = rev
                    return cls.from_db(instance.__class__, document)

                except ResourceConflict as e:
                    new_rev = db.get(instance.uid)['_rev']
                    if ignore_revision_conflict:
                        document['_rev'] = new_rev
                        continue
                    raise RevisionConflict(new_rev)

        else:
            return cls.post_instance(instance)

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        db = cls.get_db(model)
        if uid in db:
            del db[uid]
        else:
            raise NotFound(uid=uid)

    @classmethod
    def get_uids(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict = None,
        sort: List = None
    ) -> List[str]:
        if query_filter is None:
            query_filter = {}

        # convert to json and back again, to have iso datetime strings
        query_filter = json.loads(json.dumps(query_filter, cls=CustomJSONEncoder))

        db = cls.get_db(model)

        find_dict = {
            "selector": query_filter,
            "skip": skip,
            "limit": limit
        }
        if sort is not None:
            find_dict["sort"] = sort

        result = [x["_id"] for x in (db.find(find_dict))]
        return result

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict = None,
        sort: List = None
    ) -> List[BackendModel]:
        ids = cls.get_uids(model=model, skip=skip, limit=limit, query_filter=query_filter, sort=sort)
        return [cls.get_instance(model, uid=x) for x in ids]

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        with cls.alias() as alias:
            server = cls._connections[alias].server
            name = cls.collection_name(model)
            if name in server:
                server.delete(name)

        super().delete_collection(model)


class CouchDbConnectionModel(BaseModel):
    alias: str
    uri: str
    server: couchdb.Server
    dbs: Dict[str, couchdb.Database] = Field(default_factory=dict)

    class Config():
        arbitrary_types_allowed = True
