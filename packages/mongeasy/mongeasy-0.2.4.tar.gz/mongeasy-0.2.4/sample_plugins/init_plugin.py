class SampleInitPlugin:
    def before_init_document(self, *args, **kwargs):
        print(f"before_init_document_plugin: before_init_document, data: {args}, {kwargs}")
        
    def after_init_document(self, data):
        print(f"after_init_document_plugin: after_init_document, data: {data}")
