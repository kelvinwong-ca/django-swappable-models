from django.test import TestCase
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import swapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from django.db import migrations
except ImportError:
    DJ17 = False
else:
    DJ17 = True


class SwapperTestCase(TestCase):

    # Tests that should work whether or not default_app.Type is swapped
    def test_fields(self):
        Type = swapper.load_model('default_app', 'Type')
        fields = dict(
            (field.name, field)
            for field in Type._meta.fields
        )
        self.assertIn('name', fields)

    def test_create(self):
        Type = swapper.load_model('default_app', 'Type')
        Item = swapper.load_model('default_app', 'Item')

        Item.objects.create(
            type=Type.objects.create(name="Type 1"),
            name="Item 1",
        )

        self.assertEqual(Item.objects.count(), 1)

        item = Item.objects.all()[0]
        self.assertEqual(item.type.name, "Type 1")

    def test_not_installed(self):
        Invalid = swapper.load_model("invalid_app", "Invalid", required=False)
        self.assertIsNone(Invalid)
        with self.assertRaises(ImproperlyConfigured):
            swapper.load_model("invalid_app", "Invalid", required=True)

    # Tests that only work if default_app.Type is swapped
    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_setting(self):
        self.assertTrue(swapper.is_swapped("default_app", "Type"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Type"),
            "alt_app.Type"
        )

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_fields(self):
        Type = swapper.load_model('default_app', 'Type')
        fields = dict(
            (field.name, field)
            for field in Type._meta.fields
        )
        self.assertIn('code', fields)

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_create(self):
        Type = swapper.load_model('default_app', 'Type')
        Item = swapper.load_model('default_app', 'Item')

        Item.objects.create(
            type=Type.objects.create(
                name="Type 1",
                code="type-1",
            ),
            name="Item 1",
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.all()[0]
        self.assertEqual(item.type.code, "type-1")

    @unittest.skipUnless(
        settings.SWAP and DJ17,
        "requires swapped models & Django 1.7"
    )
    def test_swap_dependency(self):
        self.assertEqual(
            swapper.dependency("default_app", "Type"),
            ("alt_app", "__first__")
        )

    # Tests that only work if default_app.Type is *not* swapped
    @unittest.skipIf(settings.SWAP, "requires non-swapped models")
    def test_default_setting(self):
        self.assertFalse(swapper.is_swapped("default_app", "Type"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Type"),
            "default_app.Type"
        )

    @unittest.skipUnless(
        not settings.SWAP and DJ17,
        "requires non-swapped models & Django 1.7"
    )
    def test_default_dependency(self):
        self.assertEqual(
            swapper.dependency("default_app", "Type"),
            ("default_app", "__first__")
        )


class SwapperExampleTestCase(TestCase):

    # Tests that should work whether or not default_app.Parent is swapped
    def test_fields_on_parent(self):
        Parent = swapper.load_model('default_app', 'Parent')
        fields = dict(
            (field.name, field)
            for field in Parent._meta.fields
        )
        self.assertTrue(len(fields.keys()) > 0)  # sinlge autofield

    def test_create_instances(self):
        Parent = swapper.load_model('default_app', 'Parent')
        Child = swapper.load_model('default_app', 'Child')

        c = Child.objects.create(
            parent=Parent.objects.create(),
        )

        self.assertTrue(c.pk is not None)

        parents = Parent.objects.filter(pk=c.parent.id)
        self.assertEqual(len(parents), 1)

    # Tests that only work if default_app.Parent is swapped
    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_setting_parent(self):
        self.assertTrue(swapper.is_swapped("default_app", "Parent"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Parent"),
            "alt_app.Parent"
        )

    # Tests that only work if default_app.Child is swapped
    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_setting_child(self):
        self.assertTrue(swapper.is_swapped("default_app", "Child"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Child"),
            "alt_app.Child"
        )

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_fields_parent(self):
        Parent = swapper.load_model('default_app', 'Parent')
        fields = dict(
            (field.name, field)
            for field in Parent._meta.fields
        )
        self.assertIn('name', fields)

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_fields_child(self):
        Child = swapper.load_model('default_app', 'Child')
        fields = dict(
            (field.name, field)
            for field in Child._meta.fields
        )
        self.assertIn('name', fields)

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_create_swapped_child(self):
        Parent = swapper.load_model('default_app', 'Parent')
        Child = swapper.load_model('default_app', 'Child')
        LESLIE = "Leslie"

        c = Child.objects.create(
            parent=Parent.objects.create(
                name="Chris",
            ),
            name=LESLIE,
        )

        self.assertTrue(c.pk is not None)

        parents = Parent.objects.filter(pk=c.parent.id)
        self.assertEqual(len(parents), 1)
        self.assertEqual(c.name, LESLIE)

    @unittest.skipUnless(
        settings.SWAP and DJ17,
        "requires swapped models & Django 1.7"
    )
    def test_swap_dependency_parent(self):
        self.assertEqual(
            swapper.dependency("default_app", "Parent"),
            ("alt_app", "__first__")
        )

    # Tests that only work if default_app.Type is *not* swapped
    @unittest.skipIf(settings.SWAP, "requires non-swapped models")
    def test_default_setting_parent(self):
        self.assertFalse(swapper.is_swapped("default_app", "Parent"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Parent"),
            "default_app.Parent"
        )

    @unittest.skipUnless(
        not settings.SWAP and DJ17,
        "requires non-swapped models & Django 1.7"
    )
    def test_default_dependency_parent(self):
        self.assertEqual(
            swapper.dependency("default_app", "Parent"),
            ("default_app", "__first__")
        )
