from .settings import *
INSTALLED_APPS += ('tests.alt_app',)
DEFAULT_APP_TYPE_MODEL = "alt_app.Type"
DEFAULT_APP_PARENT_MODEL = "alt_app.Parent"
DEFAULT_APP_CHILD_MODEL = "alt_app.Child"
DEFAULT_APP_CUSTOMER_MODEL = "alt_app.Customer"
DEFAULT_APP_ACCOUNT_MODEL = "alt_app.Account"
SWAP = True
