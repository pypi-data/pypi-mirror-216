class SampleDeletePlugin:
    def before_delete_document(self, *args, **kwargs):
        print(f"before_delete_document_plugin: before_delete_document")
        
    
    def after_delete_document(self, *args, **kwargs):
        print(f"after_delete_document_plugin: after_delete_document")