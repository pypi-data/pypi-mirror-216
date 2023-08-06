import os
os.environ['MONGOEASY_CONNECTION_STRING'] = 'mongodb://localhost:27017'
os.environ['MONGOEASY_DATABASE_NAME'] = 'mongeasy_pytest'
from pymongo import MongoClient
import pytest


from mongeasy import create_document_class, registry, disconnect, Query


@pytest.fixture(scope='function')
def clean_mongo():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['mongeasy_pytest']

    # Clean all collections in the test database
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})

def test_connect_plugin(clean_mongo):
    
    from mongeasy import create_document_class, registry, disconnect, Query
    Connection = create_document_class('Connection', 'connection')
    class ConnectPlugin:
        def __init__(self):
            self.status = {
                'before_connect': False,
                'after_connect': False,
                'before_close': False,
                'after_close': False,
            }

        def before_connect(self):
            self.status['before_connect'] = True

        def after_connect(self):
            self.status['after_connect'] = True

        def before_close(self):
            self.status['before_close'] = True

        def after_close(self):
            self.status['after_close'] = True

    cp = ConnectPlugin()
    registry.register_plugin(cp)
    disconnect()
    assert cp.status['before_connect'] == False
    assert cp.status['after_connect'] == False
    assert cp.status['before_close'] == True
    assert cp.status['after_close'] == True


def test_init_document_plugin(clean_mongo):
        
        from mongeasy import create_document_class, registry, disconnect, Query
        User = create_document_class('User', 'users')
        class InitDocumentPlugin:
            def __init__(self):
                self.status = {
                    'before_init_document': False,
                    'after_init_document': False,
                }
    
            def before_init_document(self, *args, **kwargs):
                self.status['before_init_document'] = True
    
            def after_init_document(self, data):
                self.status['after_init_document'] = True
    
        idp = InitDocumentPlugin()
        registry.register_plugin(idp)
        u = User(first_name='John', last_name='Doe')
        assert idp.status['before_init_document'] == True
        assert idp.status['after_init_document'] == True
                 