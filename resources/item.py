from flask import  request
import uuid
from db import items
from flask.views import MethodView
from flask_smorest import Blueprint

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

    def put(self):
        id = request.args.get('id')
        if id == None:
            return {"message":"Given id not found"}, 404 
        if id in items.keys():
            request_data = request.get_json()
            if "name" not in request_data or "price" not in request_data:
                return {"message":"'name' and 'price' must be included in body"}, 400
            items[id] =  request.get_json()
            return {'message': "Item updated successfully"}
        return {'message': " Item Not Found"}, 404

    def post(self):
        request_data = request.get_json()
        if "name" not in request_data or "price" not in request_data:
            return {"message":"'name' and 'price' must be included in body"}, 400
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
