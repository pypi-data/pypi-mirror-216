class SampleValidatePlugin:
    def validate_document(self, *args, **kwargs):
        print(f"validate_document_plugin: validate_document, data: {args}, {kwargs}")
        
    
    def on_document_validation_error(self, *args, **kwargs):
        print(f"on_document_validation_error_plugin: on_document_validation_error, data: {args}, {kwargs}")
