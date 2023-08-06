import pluggy


hookspec = pluggy.HookspecMarker("mongeasy")
hookimpl = pluggy.HookimplMarker("mongeasy")


class MongeasySpec:

    # Connection hooks
    @hookspec
    def before_connect(self, *args, **kwargs):
        """
        Called before connecting to the database.
        """

    @hookspec
    def after_connect(self, connection, *args, **kwargs):
        """
        Called after connecting to the database.
        """

    # Document Lifecycle hooks
    @hookspec
    def before_init_document(self, *args, **kwargs):
        """
        Called before initializing a document.
        """

    @hookspec
    def after_init_document(self, document, *args, **kwargs):
        """
        Called after initializing a document.
        """

    # Document Save/Update hooks
    @hookspec
    def before_save_document(self, document, *args, **kwargs):
        """
        Called before saving a document.
        """

    @hookspec
    def after_save_document(self, document, *args, **kwargs):
        """
        Called after saving a document.
        """

    # Document Delete hooks
    @hookspec
    def before_delete_document(self, document, *args, **kwargs):
        """
        Called before deleting a document.
        """

    @hookspec
    def after_delete_document(self, document, *args, **kwargs):
        """
        Called after deleting a document.
        """

    # Document Query hooks
    @hookspec
    def before_query_document(self, query, *args, **kwargs):
        """
        Called before querying a document.
        """

    @hookspec
    def after_query_document(self, result, *args, **kwargs):
        """
        Called after querying a document.
        """

    # Aggregation hooks
    @hookspec
    def before_aggregate(self, *args, **kwargs):
        """
        Called before aggregating.
        """

    @hookspec
    def after_aggregate(self, result, *args, **kwargs):
        """
        Called after aggregating.
        """

    # Error Handling hooks
    @hookspec
    def on_error(self, error, *args, **kwargs):
        """
        Called when an error occurs.
        """


pm = pluggy.PluginManager("mongeasy")
pm.add_hookspecs(MongeasySpec)

def get_plugin_manager():
    pm = pluggy.PluginManager("mongeasy")
    pm.add_hookspecs(MongeasySpec)
    pm.load_setuptools_entrypoints("mongeasy")
    return pm