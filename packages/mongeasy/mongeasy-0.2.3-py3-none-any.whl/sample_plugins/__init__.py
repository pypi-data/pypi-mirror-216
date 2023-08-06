# from mongeasy.plugins.registry import PluginRegistry
# from .before_save_plugin import SampleSavePlugin, SampleConnectionPlugin, SampleInitDocument, SampleDeleteDocument, SampleQueryDocument, SampleValidateDocument, PydanticValidator

# from mongeasy import registry
# from pydantic import BaseModel

# class UserSchema(BaseModel):
#     first_name: str
#     last_name: str
#     email: str
#     age: int

# registry.register_plugin(PydanticValidator(UserSchema))
# registry.register_plugin(SampleSavePlugin())    
#registry.register_plugin(SampleInitDocument())    
#registry.register_plugin(SampleValidateDocument())
# registry.register_plugin(SampleConnectionPlugin())    
# registry.register_plugin(SampleDeleteDocument())   
# registry.register_plugin(SampleQueryDocument())   