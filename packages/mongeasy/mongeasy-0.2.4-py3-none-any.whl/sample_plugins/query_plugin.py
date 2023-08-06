class SampleQueryPlugin:
    def before_query_document(self, cls, *args, **kwargs):
        print(f"before_query_document_plugin: before_query_document, data: {cls}, {args}, {kwargs}")
        
    
    def after_query_document(self, cls, *args, **kwargs):
        print(f"after_query_document_plugin: after_query_document, data: {cls}, {args}, {kwargs}")
