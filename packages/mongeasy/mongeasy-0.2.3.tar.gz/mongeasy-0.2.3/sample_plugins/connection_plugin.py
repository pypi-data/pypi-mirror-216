class SampleConnectionPlugin:
    def before_connect(self):
        print("before_connect_plugin: before_connect")
    
    def after_connect(self):
        print("after_connect_plugin: after_connect")
    
    def before_close(self):
        print("before_close_plugin: before_close")
    
    def after_close(self):
        print("after_close_plugin: after_close")