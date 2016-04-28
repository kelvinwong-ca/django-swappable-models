from .settings import *
INSTALLED_APPS += ('tests.alt_app',)
DEFAULT_APP_TYPE_MODEL = "alt_app.Type"
DEFAULT_APP_PARENT_MODEL = "alt_app.Parent"
DEFAULT_APP_CHILD_MODEL = "alt_app.Child"
SWAP = True
