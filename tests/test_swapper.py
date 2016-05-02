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
        self.assertTrue(len(fields.keys()) > 0)  # single autofield

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


class ManyToManyTestCase(TestCase):

    # Tests that work whether or not default_app models are swapped
    def test_fields(self):
        Customer = swapper.load_model('default_app', 'Customer')
        fields = dict(
            (field.name, field)
            for field in Customer._meta.fields
        )
        self.assertIn('name', fields)

    def test_create_instances(self):
        Customer = swapper.load_model('default_app', 'Customer')
        Account = swapper.load_model('default_app', 'Account')

        c = Customer.objects.create()
        a = Account.objects.create()
        a.customers.add(c)
        a.save()

        from django.conf import settings as s
        print(s.INSTALLED_APPS)
        print(s.DEFAULT_APP_CUSTOMER_MODEL)
        print(s.DEFAULT_APP_ACCOUNT_MODEL)
        print(swapper.get_model_name('default_app', 'Customer'))
        print(swapper.get_model_name('default_app', 'Account'))
        print(repr(swapper.load_model('default_app', 'Account')))
        self.assertTrue(a.pk is not None)

        customers = a.customers.all()
        print('Accounts back customers query', customers.query)
        self.assertEqual(len(customers), 1)
        import pudb; pudb.set_trace()
        accounts = c.account_set.all()
        print('Customer back accounts query', accounts.query)
        self.assertEqual(len(accounts), 1)

    # Tests that only work if default_app.Account is swapped
    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_setting(self):
        self.assertTrue(swapper.is_swapped("default_app", "Customer"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Customer"),
            "alt_app.Customer"
        )
        self.assertTrue(swapper.is_swapped("default_app", "Account"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Account"),
            "alt_app.Account"
        )

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_fields(self):
        Customer = swapper.load_model('default_app', 'Customer')
        fields = dict(
            (field.name, field)
            for field in Customer._meta.fields
        )
        self.assertIn('vip', fields)
        Account = swapper.load_model('default_app', 'Account')
        fields = dict(
            (field.name, field)
            for field in Account._meta.fields
        )
        self.assertIn('active', fields)
