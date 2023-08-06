from pydantic import ValidationError

class PydanticValidatorPlugin:
    def __init__(self, schema):
        self.schema = schema

    def validate_document(self, *args, **kwargs):
        print(f"Validating document {kwargs}")
        try:
            self.schema(**kwargs)
        except ValidationError as e:
            print(f"Validation error for document {kwargs}: {e}")
            return False
        return True
    
    def on_document_validation_error(self, document, error):
        print(f"Validation error for document {document}: {error}")
        raise error