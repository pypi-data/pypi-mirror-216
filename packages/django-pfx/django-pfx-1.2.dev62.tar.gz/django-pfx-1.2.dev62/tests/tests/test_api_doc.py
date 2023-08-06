from django.test import TestCase, override_settings

from apispec.yaml_utils import load_operations_from_docstring as from_doc

from pfx.pfxcore.management.commands.makeapidoc import (
    get_spec,
    path_parameters,
)
from pfx.pfxcore.test import TestAssertMixin
from tests.views import AuthorRestView


class ApiDocTest(TestAssertMixin, TestCase):
    def test_default_generation(self):
        spec = get_spec().to_dict()
        self.assertEqual(spec['openapi'], "3.0.2")
        info = spec['info']
        self.assertEqual(info['title'], "PFX API")
        self.assertEqual(info['version'], "1.0.0")

    @override_settings(PFX_OPENAPI_TEMPLATE=dict(
        title="MyAPI",
        info=dict(description="A test API")))
    def test_default_customized_generation(self):
        spec = get_spec().to_dict()
        self.assertEqual(spec['openapi'], "3.0.2")
        info = spec['info']
        self.assertEqual(info['title'], "MyAPI")
        self.assertEqual(info['version'], "1.0.0")
        self.assertEqual(info['description'], "A test API")

    def test_paths_generation(self):
        def assertMethods(paths, p, methods):
            self.assertEqual(set(paths[p].keys()), methods)

        spec = get_spec().to_dict()
        paths = spec['paths']
        assertMethods(paths, '/authors', {'get', 'post'})
        assertMethods(paths, '/authors/{pk}', {'get', 'put', 'delete'})
        assertMethods(paths, '/authors/slug/{slug}', {'get'})
        assertMethods(paths, '/authors/cache/{pk}', {'get'})

        tags = spec['tags']
        tags_keys = [t['name'] for t in tags]
        self.assertIn("Authentication", tags_keys)
        self.assertIn("Author", tags_keys)
        self.assertIn("Book", tags_keys)
        self.assertIn("Book Type", tags_keys)
        self.assertIn("Locale", tags_keys)
        self.assertJE(paths['/authors'], 'get.tags', ["Author"])
        self.assertJE(paths['/authors'], 'post.tags', ["Author"])
        self.assertJE(paths['/auth/login'], 'post.tags', ["Authentication"])

        # Check a inherited get with default description
        get = self.get_val(paths, '/authors/{pk}.get')
        self.assertJE(get, 'summary', "Get author")
        self.assertJE(get, 'parameters.@0', {
            '$ref': "#/components/parameters/DateFormat"})
        self.assertJE(get, 'parameters.@1.in', "path")
        self.assertJE(get, 'parameters.@1.name', "pk")
        self.assertJE(get, 'parameters.@1.schema.type', "integer")
        self.assertJE(get, 'parameters.@1.required', True)
        self.assertJE(get, 'parameters.@1.description', "the author pk")
        # Check a inherited get with custom description
        self.assertJE(
            paths, '/authors-annotate/{pk}.get.summary',
            "Get custom author")
        # Check a slug
        get = self.get_val(paths, '/authors/slug/{slug}.get')
        self.assertJE(get, 'summary', "Get author by slug")
        self.assertJE(get, 'parameters.@0', {
            '$ref': "#/components/parameters/DateFormat"})
        self.assertJE(get, 'parameters.@1.in', "path")
        self.assertJE(get, 'parameters.@1.name', "slug")
        self.assertJE(get, 'parameters.@1.schema.type', "string")
        self.assertJE(get, 'parameters.@1.required', True)
        self.assertJE(get, 'parameters.@1.description', "the author slug name")

        # Check list parameters with auto generated filters
        get = self.get_val(paths, '/authors.get')
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/ListCount'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/ListItems'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/ListSearch'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/ListOrder'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/Subset'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/SubsetPage'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/SubsetPageSize'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/SubsetPageSubset'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/SubsetOffset'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/ListCount'})
        self.assertJIn(get, 'parameters', {
            '$ref': '#/components/parameters/SubsetLimit'})
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "science_fiction",
            "description": "Filter by science fiction"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "heroic_fantasy",
            "description": "Filter by heroic fantasy"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "types",
            "description": "Filter by types"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "last_name",
            "description": "Filter by last name"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "first_name",
            "description": "Filter by first name"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "gender",
            "description": "Filter by gender"
        })
        self.assertJIn(get, 'parameters', {
            "in": "query",
            "name": "last_name_choices",
            "description": "Filter by tolkien or asimov"
        })

        schema_key = self.get_val(
            paths,
            '/authors/{pk}.get.responses.200.content.application/json.schema'
        )['$ref'].split('/')[-1]
        self.assertIn("Author", schema_key)
        props = spec['components']['schemas'][schema_key]['properties']
        self.assertJE(props, 'first_name.type', 'string')
        self.assertJE(props, 'name_length.type', 'number')
        self.assertJE(props, 'name_length.readonly', True)
        self.assertJE(props, 'gender.type', 'string')
        self.assertJE(props, 'gender.enum', ['male', 'female'])
        self.assertJE(props, 'types.type', 'array')
        self.assertJE(props, 'types.items.type', 'object')
        self.assertJE(props, 'created_at.type', 'string')
        self.assertJE(props, 'created_at.format', 'date')
        self.assertJE(props, 'created_at.nullable', True)

        schema_key = self.get_val(
            paths,
            '/authors.get.responses.200.content.application/json.schema'
        )['$ref'].split('/')[-1]
        self.assertIn("Author", schema_key)
        props = spec['components']['schemas'][schema_key]['properties']
        self.assertJE(props, 'items.type', 'object')
        self.assertJE(props, 'items.format', 'Author')
        self.assertSize(props, 'items.properties', 3)
        props = self.get_val(props, 'items.properties')
        self.assertJE(props, 'first_name.type', 'string')
        self.assertJE(props, 'last_name.type', 'string')
        self.assertJE(props, 'gender.type', 'string')
        self.assertJE(props, 'gender.enum', ['male', 'female'])

    def test_view_get_urls(self):
        def assertMethods(urls, p, methods):
            self.assertEqual(next(filter(
                lambda u: u['path'] == p, urls))['methods'], methods)

        urls = AuthorRestView.get_urls()

        # Methods from RestView
        assertMethods(urls, '/authors', dict(get='get_list', post='post'))
        assertMethods(urls, '/authors/<int:id>', dict(
            delete='delete', get='get', put='put'))
        # A method from SlugDetailRestViewMixin
        assertMethods(urls, '/authors/slug/<slug:slug>', dict(
            get='get_by_slug'))
        # A method from AuthorRestView itself
        assertMethods(urls, '/authors/cache/<int:id>', dict(get='cache_get'))

    def test_path_parameter_untyped(self):
        param = next(path_parameters(from_doc(""), '/path/<my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_str(self):
        param = next(path_parameters(from_doc(""), '/path/<str:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_int(self):
        param = next(path_parameters(from_doc(""), '/path/<int:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "integer")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_slug(self):
        param = next(path_parameters(from_doc(""), '/path/<slug:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_uuid(self):
        param = next(path_parameters(from_doc(""), '/path/<uuid:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_path(self):
        param = next(path_parameters(from_doc(""), '/path/<path:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_custom(self):
        """Test with a custom path type.
        Actually you cannot register your custom path type. Every custom
        type will be considered as string."""
        param = next(path_parameters(from_doc(""), '/path/<custom:my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJENotExists(param, 'description')

    def test_path_parameter_description(self):
        param = next(path_parameters(from_doc(
            """Test
            ---
            get:
                parameters extras:
                    my_param: a test description
            """).get('get'), '/path/<my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "string")
        self.assertJE(param, 'required', True)
        self.assertJE(param, 'description', 'a test description')

    def test_path_parameter_extras(self):
        param = next(path_parameters(from_doc(
            """Test
            ---
            get:
                parameters extras:
                    my_param:
                        description: a test description
                        schema:
                            type: number
            """).get('get'), '/path/<my_param>'))
        self.assertJE(param, 'in', "path")
        self.assertJE(param, 'name', "my_param")
        self.assertJE(param, 'schema.type', "number")
        self.assertJE(param, 'required', True)
        self.assertJE(param, 'description', 'a test description')
