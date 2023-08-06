"""
This module contains the dynamic class generation of document classes.

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
import inspect
from typing import Union
from .utils.utils import pascal_to_snake
from .document import Document
from .exceptions import MongeasyValidationException, MongeasyFieldError
from .plugins.registry import PluginRegistry


def create_document_class(class_name: str, collection_name: str = None, base_classes: tuple = ()):
    """
    Dynamically create a document class and register it in the calling module's namespace.
    Args:
        class_name (str): Name of the class to create.
        collection_name (str, optional): Name of the collection. Defaults to None. 
            If None, the collection name will be the snake_case version of the class name with an 's' appended.
        base_classes (tuple, optional): Optional base classes to be added to the document class. Defaults to ().

    Returns:
        _type_: The newly created document class.
    """
    # Get the calling module
    frame = inspect.currentframe().f_back
    calling_module = inspect.getmodule(frame)

    # Dynamically generate the document class
    from . import connection
    if collection_name is None:
        collection_name = pascal_to_snake(class_name) + 's'
    
    # Create the collection object
    collection = connection.db[collection_name]
    from mongeasy import registry
    doc_class = type(class_name, base_classes + (Document, ), {'collection':collection, 'registry':registry})

    # Register the document class in the calling module's namespace
    setattr(calling_module, class_name, doc_class)
    
    return doc_class
