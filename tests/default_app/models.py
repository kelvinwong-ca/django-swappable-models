from django.db import models
import swapper


class BaseType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Type(BaseType):

    class Meta:
        swappable = swapper.swappable_setting("default_app", "Type")


class Item(models.Model):
    type = models.ForeignKey(swapper.get_model_name('default_app', "Type"))
    name = models.CharField(max_length=255)
    description = models.TextField()


class BaseParent(models.Model):
    # minimal base implementation ...
    class Meta:
        abstract = True


class Parent(BaseParent):
    # default (swappable) implementation ...

    class Meta:
        swappable = swapper.swappable_setting('default_app', 'Parent')


class BaseChild(models.Model):
    parent = models.ForeignKey(swapper.get_model_name('default_app', 'Parent'))
    # minimal base implementation ...

    class Meta:
        abstract = True


class Child(BaseChild):
    # default (swappable) implementation ...

    class Meta:
        swappable = swapper.swappable_setting('default_app', 'Child')
