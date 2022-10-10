from marshmallow import Schema, fields 


class ItemSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)
 