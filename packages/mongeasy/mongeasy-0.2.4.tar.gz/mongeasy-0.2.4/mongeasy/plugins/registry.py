from enum import Enum
from functools import wraps
from pkg_resources import iter_entry_points
import yaml


class Hook(Enum):
    BEFORE_CONNECT = 'before_connect'
    AFTER_CONNECT = 'after_connect'
    BEFORE_INIT_DOCUMENT = 'before_init_document'
    AFTER_INIT_DOCUMENT = 'after_init_document'
    BEFORE_SAVE_DOCUMENT = 'before_save_document'
    AFTER_SAVE_DOCUMENT = 'after_save_document'
    BEFORE_DELETE_DOCUMENT = 'before_delete_document'
    AFTER_DELETE_DOCUMENT = 'after_delete_document'
    BEFORE_QUERY_DOCUMENT = 'before_query_document'
    AFTER_QUERY_DOCUMENT = 'after_query_document'
    VALIDATE_DOCUMENT = 'validate_document'
    ON_DOCUMENT_VALIDATION_ERROR = 'on_document_validation_error'
    ON_PLUGIN_LOAD = 'on_plugin_load'
    ON_PLUGIN_UNLOAD = 'on_plugin_unload'
    ON_PLUGIN_ERROR = 'on_plugin_error'
    BEFORE_CLOSE = 'before_close'
    AFTER_CLOSE = 'after_close'

class PluginRegistry:

    def __init__(self):
        self._plugins = []

    def register_plugin(self, plugin):
        try:
            self._plugins.append(plugin)
            if hasattr(plugin, Hook.ON_PLUGIN_LOAD.value):
                plugin.on_plugin_load()
        except Exception as e:
            self.dispatch(Hook.ON_PLUGIN_ERROR, plugin, e)

    def unregister_plugin(self, plugin):
        try:
            self._plugins.remove(plugin)
            if hasattr(plugin, Hook.ON_PLUGIN_UNLOAD.value):
                plugin.on_plugin_unload()
        except Exception as e:
            self.dispatch(Hook.ON_PLUGIN_ERROR, plugin, e)

    def dispatch(self, hook, *args, **kwargs):
        if not isinstance(hook, Hook):
            raise ValueError(f"Invalid hook: {hook}")
        for plugin in self._plugins:
            hook_method = getattr(plugin, hook.value, None)
            if callable(hook_method):
                try:
                    hook_method(*args, **kwargs)
                except Exception as e:
                    if hook == Hook.VALIDATE_DOCUMENT:
                        self.dispatch(Hook.ON_DOCUMENT_VALIDATION_ERROR, plugin, e)
                    else:
                        self.dispatch(Hook.ON_PLUGIN_ERROR, plugin, e)


    def discover(self):
        for entry_point in iter_entry_points('mongeasy.plugins'):
            plugin = entry_point.load()
            self.register(plugin())

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

            self.apply_config(config)

    def apply_config(self, config):
        # TODO: Validate config
        for plugin in self._plugins:
            plugin_name = type(plugin).__name__
            if plugin_name in config:
                for key, value in config[plugin_name].items():
                    if hasattr(plugin, key):
                        setattr(plugin, key, value)
                    else:
                        self.dispatch(Hook.ON_PLUGIN_ERROR, plugin,
                                        Exception(f"Invalid config key: {key} for plugin {plugin_name}"))


def plugin_dispatcher(hooks):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            from mongeasy import registry
            # Pre-hooks
            for hook in hooks:
                if hook.get('when') == 'pre' and (hook.get('condition') is None or hook['condition'](func.__name__)):
                    registry.dispatch(hook['hook'],self, *args, **kwargs)

            # Call the actual function
            result = func(self, *args, **kwargs)

            # Post-hooks
            for hook in hooks:
                if hook.get('when') == 'post' and (hook.get('condition') is None or hook['condition'](func.__name__)):
                    if func.__name__ == "__init__":
                        # If the method is __init__, pass self as the data
                        registry.dispatch(hook['hook'],self)
                    else:
                        registry.dispatch(hook['hook'], self, *args, **kwargs) 
            
            return result
        return wrapper
    return decorator