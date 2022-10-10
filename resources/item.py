from flask import  request
import uuid
from db import items
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import ItemSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):
    def get(self):
        id = request.args.get('id')
        if id is None:
            return {"items": items}
        try:
            return items[id]
        except KeyError:
            return {'message': "Record doesn't exist"}, 404 

    @blp.arguments(ItemSchema)
    def put(self, request_data):
        id = request.args.get('id')
        if id == None:
            return {"message":"Given id not found"}, 404 
        if id in items.keys():
            items[id] =  request_data
            return {'message': "Item updated successfully"}
        return {'message': " Item Not Found"}, 404

    @blp.arguments(ItemSchema)
    def post(self, request_data):
        items[uuid.uuid4().hex] = request_data
        return {"message": "Item added succesfully"}, 201

    def delete(self):
        id = request.args.get('id')
        if id == None:
            return {"message":"Given id not found"}, 404
        if id in items.keys():
            del items[id]
            return {'message': 'Item deleted successfully'}
        return {'message': "Record doesn't exist"}, 404
