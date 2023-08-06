import json
from hashlib import sha1


class Schema:
    @classmethod
    def id(cls):
        return cls.__name__


class ModelSchema(Schema):
    def __init__(self, model, fields):
        self.model = model
        self.fields = fields

    def id(self):
        hash = sha1(json.dumps(self.to_schema()).encode()).hexdigest()[:10]
        return f"{self.model.__name__}.{hash}"

    def to_ref(self):
        return {
            'description': str(self.model._meta.verbose_name),
            'content': {'application/json': {'schema': self.id()}}}

    def to_schema(self):
        properties = {}
        for name, field in self.fields.items():
            properties[name] = field.to_apidoc()
        return dict(properties=properties)


class ModelListSchema(ModelSchema):
    def to_ref(self):
        return {
            'description': str(self.model._meta.verbose_name_plural),
            'content': {'application/json': {'schema': self.id()}}}

    def to_schema(self):
        model = super().to_schema()
        return dict(properties=dict(
            items=dict(
                type='object', format=str(self.model._meta.verbose_name),
                **model),
            meta=dict(type='object')))
