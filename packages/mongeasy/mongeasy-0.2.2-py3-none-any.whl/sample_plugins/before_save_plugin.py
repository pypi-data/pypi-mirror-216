class SampleSavePlugin:
    def before_save_document(self, data):
        print("before_save_plugin: before_save")
        return data