from django.db import models
from tests.default_app.models import (
    BaseType, BaseParent, BaseChild, BaseCustomer, BaseAccount)


class Type(BaseType):
    code = models.SlugField()

    class Meta:
        app_label = 'alt_app'


class Parent(BaseParent):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'alt_app'


class Child(BaseChild):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'alt_app'


class Customer(BaseCustomer):
    vip = models.BooleanField(default=False)

    class Meta:
        app_label = 'alt_app'


class Account(BaseAccount):
    active = models.BooleanField(default=True)

    class Meta:
        app_label = 'alt_app'
