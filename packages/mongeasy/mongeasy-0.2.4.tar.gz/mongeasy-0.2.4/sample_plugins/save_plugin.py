

class SampleSavePlugin:
    def before_save_document(self, *args, **kwargs):
        print(f"before_save_plugin: before_save, data: {args}, {kwargs}")
        
    
    def after_save_document(self, data):
        print(f"after_save_plugin: after_save, data: {data}")
        

        






