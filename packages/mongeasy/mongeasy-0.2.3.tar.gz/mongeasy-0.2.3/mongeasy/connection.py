import os
import import_string
import yaml
import pymongo
from mongeasy.exceptions import MongeasyDBConnectionError
from mongeasy.plugins.registry import Hook


class MongeasyConnection:
    def __init__(self, uri=None, database=None, connection_options=None, registry=None):
        self.uri = uri
        self.database = database
        self.connection_options = {} if connection_options is None else connection_options
        self.connection_options.setdefault('maxPoolSize', 100)
        self.connection_options.setdefault('retryWrites', True)
        self.connection_options.setdefault('retryReads', True)
        self.check_env()
        self.check_conf_file()

        if self.uri is None:
            raise ValueError("No connection string provided.")
        if self.database is None:
            raise ValueError("No database name provided.")
        
        self.registry = registry

        if registry is not None:
                registry.dispatch(Hook.BEFORE_CONNECT)

        try:
            self.client = pymongo.MongoClient(self.uri, **self.connection_options)
            self.db = self.client[self.database]
        except (pymongo.errors.ConnectionFailure,
                pymongo.errors.ServerSelectionTimeoutError,
                pymongo.errors.ConfigurationError,
                pymongo.errors.InvalidURI) as e:
            raise MongeasyDBConnectionError(f'Failed to connect to database: {e}')
        if registry is not None:
                registry.dispatch(Hook.AFTER_CONNECT)
        
    def check_env(self):
        if self.uri is None:
            self.uri = os.environ.get('MONGOEASY_CONNECTION_STRING')
        if self.database is None:
            self.database = os.environ.get('MONGOEASY_DATABASE_NAME')
        if self.connection_options is None:
            self.connection_options = os.environ.get('MONGOEASY_CONNECTION_OPTIONS')

    def check_conf_file(self):
        config_path = os.path.join(os.getcwd(), 'mongeasy_config.yml')

        # Check if the configuration file exists
        if os.path.exists(config_path):
            # Read the configuration from the file
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config is None:
                    config = {}
                db_config = config.get('db_config', {})

            if db_config != {}:
    
                if self.uri is None:
                    self.uri = db_config.get('uri', None)
                if self.database is None:
                    self.database = db_config.get('database', None)
                if self.connection_options is None:
                    self.connection_options = db_config.get('connection_options', None)

            # Handle plugins
            from mongeasy import registry
            plugins_paths = config.get('plugins', [])
            for plugin_path in plugins_paths:
                plugin = import_string(plugin_path)()
                registry.register_plugin(plugin)


    def connect(self, uri=None, database=None, connection_options=None):
        if uri is not None:
            self.uri = uri
        if database is not None:
            self.database = database
        if connection_options is not None:
            self.connection_options = connection_options

        self.client = pymongo.MongoClient(self.uri, **self.connection_options)
        self.db = self.client[self.database]
        return self.db

    def disconnect(self):
        if self.registry is not None:
                self.registry.dispatch(Hook.BEFORE_CLOSE)
        self.client.close()
        if self.registry is not None:
                self.registry.dispatch(Hook.AFTER_CLOSE)
