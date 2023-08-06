"""
This module contains the Document class for interacting with MongoDB collections.

MIT License

Copyright (c) 2023 Joakim Wassberg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom
the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime
from copy import copy, deepcopy
from typing import Union, List, Dict, Any
import logging
import json
import bson
from mongeasy.exceptions import MongeasyDBCollectionError, MongeasyFieldError, MongeasyDBDocumentError, MongeasyIndexException
from mongeasy.plugins.registry import Hook, plugin_dispatcher
from mongeasy.base_dict import BaseDict
from mongeasy.core import Query
from mongeasy.resultlist import ResultList
from mongeasy.lazy_resultlist import LazyResultList
import pymongo


class Document(BaseDict):
    """
    This class acts as the base class for collection classes. Each instance of the subclasses
    will represent a single document
    """
    collection = None
    registry = None
    logger = logging.getLogger('mongeasy')

    @plugin_dispatcher([
        {'hook': Hook.BEFORE_INIT_DOCUMENT, 'when': 'pre'},
        {'hook': Hook.AFTER_INIT_DOCUMENT, 'when': 'post'},
        {'hook': Hook.VALIDATE_DOCUMENT, 'when': 'pre'},
        
    ])
    def __init__(self, *args,  **kwargs):
        super().__init__()
        
        # Handle positional arguments
        if len(args) == 1 and isinstance(args[0], dict):
            as_dict = copy(args[0])
        elif len(args) == 0:
            as_dict = copy(kwargs)
        else:
            raise TypeError(f'Document() takes 1 positional argument or keyword arguments but {len(args) + len(kwargs)} were given')

        # If _id is not present we add the _id attribute
        if '_id' not in as_dict:
            self._id = None
        else:
            try:
                self._id = bson.ObjectId(str(as_dict['_id']))
            except bson.errors.InvalidId:
                raise MongeasyFieldError(f'Invalid _id: {as_dict["_id"]}')

        # Update the object
        self.__dict__.update(as_dict)

    def has_changed(self) -> dict:
        """
        Checks if any of the fields in this document has changed
        :return: dict, a dict with the changed fields, empty if no fields have changed
        """
        if self._id is None:
            return self.__dict__

        changed_fields = {}
        for key, value in self.__dict__.items():
            if key != '_id':
                try:
                    result = self.collection.find_one({'_id': self._id}, {key: 1})
                except (pymongo.errors.OperationFailure, pymongo.errors.ServerSelectionTimeoutError) as e:
                    Document.logger.error(f"Error querying the database: {e}")
                    return {}

                if result and key in result and result[key] != value:
                    changed_fields[key] = value
        return changed_fields

    def is_saved(self) -> bool:
        """
        Checks if this document has been saved to the database
        :return: bool, True if the document has been saved, False otherwise
        """
        return not bool(self.has_changed())
    
    @plugin_dispatcher([
        {'hook': Hook.BEFORE_SAVE_DOCUMENT, 'when': 'pre'},
        {'hook': Hook.AFTER_SAVE_DOCUMENT, 'when': 'post'},
        {'hook': Hook.VALIDATE_DOCUMENT, 'when': 'pre'},
        ])
    def save(self):
        """
        Saves the current object to the database
        :return: The saved object
        """
        if self.collection is None:
            Document.logger.error("The collection does not exist")
            raise MongeasyDBCollectionError('The collection does not exist')

        # Call the before_save hook
        # if self.registry:
        #     self.registry.dispatch(Hook.BEFORE_SAVE_DOCUMENT, self)


        # If _id is None, this is a new document
        if self._id is None:
            del self._id
            res = self.collection.insert_one(self.__dict__)
            self._id = res.inserted_id
            
            # if self.registry:
            #     self.registry.dispatch(Hook.AFTER_SAVE_DOCUMENT, self)
            return self

        # if no fields have changed, return the document unchanged
        if not (changed_fields := self.has_changed()):
            # if self.registry:
            #     self.registry.dispatch(Hook.AFTER_SAVE_DOCUMENT, self)
            return self

        # update the document
        update_result = self.collection.update_one({'_id': self._id}, {'$set': changed_fields})
        if update_result.matched_count == 0:
            Document.logger.error(f"Document with _id {self._id} does not exist")
            raise MongeasyDBDocumentError(f"Document with _id {self._id} does not exist")
        else:
            # if self.registry:
            #     self.registry.dispatch(Hook.AFTER_SAVE_DOCUMENT, self)
            return self

    def reload(self):
        """
        Fetches the latest state of the document from the database and updates the current instance with the changes.
        """
        if self._id is None:
            raise MongeasyDBDocumentError('Cannot reload unsaved document')

        # fetch the latest state of the document from the database
        db_doc = self.collection.find_one({'_id': self._id})
        if db_doc is None:
            raise MongeasyDBDocumentError(f"Document with _id {self._id} does not exist")

        self_before_reload = deepcopy(self)
        # update the current instance with the changes
        for key, value in db_doc.items():
            if isinstance(value, dict) and not isinstance(value, Document):
                # convert any embedded dictionary to an instance of BaseDict
                self[key] = BaseDict(value)
            else:
                self[key] = value


    def delete_field(self, field: str):
        """
        Removes a field from this document
        :param field: str, the field to remove
        :return: None
        """
        try:
            self.collection.update_one({'_id': self._id}, {"$unset": {field: ""}})
        except Exception as e:
            Document.logger.error(f"Error deleting field '{field}' from document with id '{self._id}': {e}")
        else:
            Document.logger.info(f"Field '{field}' deleted from document with id '{self._id}'")

    @plugin_dispatcher([
        {'hook': Hook.BEFORE_DELETE_DOCUMENT, 'when': 'pre'},
        {'hook': Hook.AFTER_DELETE_DOCUMENT, 'when': 'post'},
        ])
    def delete(self):
        """
        Delete the current object from the database
        :return: None
        """
        if self.collection is None:
            raise MongeasyDBCollectionError('The collection does not exist')

        if self._id is None:
            raise MongeasyDBDocumentError('Cannot delete unsaved document')

        self.collection.delete_one({'_id': self._id})

    def to_json(self):
        """
        Serialize the document to JSON
        :return: str, the JSON representation of the document
        """
        json_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, bson.ObjectId):
                json_dict[key] = str(value)
            elif isinstance(value, datetime):
                json_dict[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                json_dict[key] = value
        return json.dumps(json_dict)

    @classmethod
    def raw_query(cls, query: Union[Dict, Query], *args, **kwargs) -> pymongo.cursor.Cursor:
        """
        Performs a raw query on the collection
        :param query: The query to perform
        :return: Cursor, the cursor to the query results
        """
        if isinstance(query, Query):
            query = query.to_mongo_query()
        if cls.collection is None:
            raise MongeasyDBCollectionError('The collection does not exist')

        return cls.collection.find(query, *args, **kwargs)

    @classmethod
    def raw_aggregate(cls, pipeline: List[Dict], *args, **kwargs) -> pymongo.cursor.Cursor:
        """
        Performs a raw aggregation on the collection
        :param pipeline: The aggregation pipeline to perform
        :return: Cursor, the cursor to the aggregation results
        """
        if cls.collection is None:
            raise MongeasyDBCollectionError('The collection does not exist')

        return cls.collection.aggregate(pipeline, *args, **kwargs)

    @classmethod
    def create_index(cls, keys: List[str], index_type: str = 'asc', unique: bool = False, name: Union[str, None] = None) -> None:
        """
        Creates an index on the specified keys
        :param keys: The keys to index on
        :param index_type: The index type, either 'asc' (default) or 'desc'
        :param unique: Whether the index should be unique
        :param name: The name of the index
        :return: None
        """
        # Check that keys is a non-empty list of strings
        if not isinstance(keys, list) or not all(isinstance(key, str) for key in keys) or len(keys) == 0:
            raise MongeasyIndexException('keys must be a non-empty list of strings')

        # Check that index_type is either 'asc' or 'desc'
        if index_type not in ['asc', 'desc']:
            raise MongeasyIndexException('index_type must be either "asc" or "desc"')

        # Check that name is either None or a non-empty string
        if name is not None and not isinstance(name, str):
            raise MongeasyIndexException('name must be either None or a non-empty string')

        index_name = name or '_'.join(keys) + '_' + index_type.lower()
        index_type = pymongo.ASCENDING if index_type == 'asc' else pymongo.DESCENDING
        cls.collection.create_index([(key, index_type) for key in keys], name=index_name, unique=unique)

    @classmethod
    def get_by_id(cls, _id:str) -> Union['Document', None]:
        """
        Get a document by its _id
        :param _id: str, the id of the document
        :return: The retrieved document or None
        """
        try:
            return cls(cls.collection.find_one({'_id': bson.ObjectId(_id)}))
        except bson.errors.InvalidId:
            return None

    @classmethod
    def insert_many(cls, items: List[dict]) -> None:
        """
        Inserts a list of dictionaries into the database
        :param items: list of dict, items to insert
        :return: None
        """
        for item in items:
            try:
                cls(item).save()
            except pymongo.errors.PyMongoError as e:
                Document.logger.exception(f"Error inserting item: {item}. Exception: {e}")

    @classmethod
    @plugin_dispatcher([
        {'hook': Hook.BEFORE_QUERY_DOCUMENT, 'when': 'pre'},
        {'hook': Hook.AFTER_QUERY_DOCUMENT, 'when': 'post'},
        ])
    def find(cls, *args, lazy=False, **kwargs):
        """
        Find a document that matches the keywords
        :param arg: positional arguments
        :param lazy: Whether to use lazy loading. Default is False.
        :param kwargs: keyword arguments or dict to match
        :return: ResultList or LazyResultList
        """
        # Handle positional arguments
        if len(args) == 1 and isinstance(args[0], dict):
            as_dict = copy(args[0])
        if len(args) == 1 and isinstance(args[0], Query):
            as_dict = args[0].to_mongo_query()
        elif len(args) == 0:
            as_dict = copy(kwargs)

        cursor = cls.collection.find(as_dict)
        if lazy:
            return LazyResultList(cursor, cls)
        else:
            return ResultList(cls(item) for item in cursor)


    @classmethod
    def find_in(cls, field:str, values:list) -> ResultList:
        """
        Find a document that matches the keywords
        :param field: str, the field to search in
        :param values: list, the values to search for
        :return: ResultList
        """
        return ResultList(cls(item) for item in cls.collection.find({field: {"$in": values}}))

    @classmethod
    def all(cls) -> ResultList:
        """
        Returns all documents in the collection
        :return: ResultList
        """
        return ResultList(cls(item) for item in cls.collection.find({}))

    @classmethod
    def all_iter(cls) -> dict:
        """
        Retrieve all documents from the collection as an iterator
        :yields: dict representation of next document
        """
        for item in cls.collection.find({}):
            yield cls(**item)

    @classmethod
    @plugin_dispatcher([
        {'hook': Hook.BEFORE_DELETE_DOCUMENT, 'when': 'pre'},
        {'hook': Hook.AFTER_DELETE_DOCUMENT, 'when': 'post'},
    ])
    def delete_many(cls, *args, **kwargs) -> None:
        """
        Delete the document that matches the keywords

        :param args: positional arguments
        :param kwargs: keyword arguments or dict to match
        :return: None
        """
        # Handle positional arguments
        if len(args) == 1 and isinstance(args[0], dict):
            as_dict = copy(args[0])
        elif len(args) == 0:
            as_dict = copy(kwargs)
        cls.collection.delete_many(as_dict)

    @classmethod
    def document_count(cls) -> int:
        """
        Returns the total number of documents in the collection
        :return: int
        """
        return cls.collection.count_documents({})
