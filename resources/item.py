from email import message
from flask import  request
import uuid
from db import items
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemGetSchema, ItemOptionalQuerySchema, ItemQuerySchema, ItemSchema, SuccessMessageSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):

    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self, args):
        id = args.get('id')  
        if id is None:
            return items
        for item in items:
            if item['id'] == id:
                return [item]
        abort(404, message="Record doesn't exist")

    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self, request_data, args):
        id = args.get('id')
        for item in items:
            if item['id'] == id:
                item['item']['name'] = request_data['name']
                item['item']['price'] = request_data['price']
                return {'message': "Item updated successfully"}
        abort(404, message="Item not found")

    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    def post(self, request_data):
        item = {
            'id':uuid.uuid4().hex,
            'item': {
                "name": request_data["name"],
                "price": request_data["price"]
            }
        }
        items.append(item)

        return {"message": "Item added succesfully"}, 201

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        for item in items:
                if item['id'] == id:
                    items.remove(item)
                    return {'message': 'Item deleted'}
                    
        abort(404, message="Given id doesn't exist.")
