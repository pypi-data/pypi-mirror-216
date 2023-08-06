"""Top-level package for Mongeasy."""

__author__ = """Joakim Wassberg"""
__email__ = 'joakim.wassberg@arthead.se'

from mongeasy.connection import MongeasyConnection
from mongeasy.exceptions import MongeasyDBConnectionError
from mongeasy.dynamics import create_document_class
from mongeasy.core import Query
from mongeasy.plugins.registry import PluginRegistry, Hook, plugin_dispatcher

registry = PluginRegistry()
connection = MongeasyConnection(registry=registry)


def connect(connection_str: str=None, db_name: str=None):
    connection.connect(connection_str, db_name)

def disconnect():
    connection.disconnect()
#