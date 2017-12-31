import warnings
from . import base


class TestType(base.SchemaTestCase):

    def test_single_type(self):
        schema = {'type': 'null'}
        self.add_schema(schema)
        self.add_schema(schema)
        self.assertResult(schema)

    def test_single_type_unicode(self):
        schema = {u'type': u'string'}
        self.add_schema(schema)
        self.assertResult(schema)

    def test_redundant_integer_type(self):
        self.add_schema({'type': 'integer'})
        self.add_schema({'type': 'number'})
        self.assertResult({'type': 'number'})

    def test_no_type(self):
        schema1 = {"title": "ambiguous schema"}
        schema2 = {"grail": "We've already got one"}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.add_schema(schema1)
            self.add_schema(schema2)
        self.assertResult(dict(**schema1, **schema2))


class TestAnyOf(base.SchemaTestCase):

    def test_multi_type(self):
        self.add_schema({'type': 'boolean'})
        self.add_schema({'type': 'null'})
        self.add_schema({'type': 'string'})
        self.assertResult({'type': ['boolean', 'null', 'string']})

    def test_anyof_generated(self):
        schema1 = {"type": "null", "title": "African or European Swallow?"}
        schema2 = {"type": "boolean", "title": "Gruyere"}
        self.add_schema(schema1)
        self.add_schema(schema2)
        self.assertResult({"anyOf": [
            schema1,
            schema2
        ]})

    def test_anyof_seeded(self):
        schema1 = {"type": "null", "title": "African or European Swallow?"}
        schema2 = {"type": "boolean", "title": "Gruyere"}
        self.add_schema({"anyOf": [
            {"type": "null"},
            schema2
        ]})
        self.add_schema(schema1)
        self.assertResult({"anyOf": [
            schema1,
            schema2
        ]})

    def test_list_plus_tuple(self):
        schema1 = {"type": "array", "items": {"type": "null"}}
        schema2 = {"type": "array", "items": [{"type": "null"}]}
        self.add_schema(schema1)
        self.add_schema(schema2)
        self.assertResult({"anyOf": [
            schema1,
            schema2
        ]})

    def test_multi_type_and_anyof(self):
        schema1 = {'type': ['boolean', 'null', 'string']}
        schema2 = {"type": "boolean", "title": "Gruyere"}
        self.add_schema(schema1)
        self.add_schema(schema2)
        self.assertResult({"anyOf": [
            {'type': ['null', 'string']},
            schema2
        ]})
