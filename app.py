from flask import Flask, request
import uuid
from db import items

app = Flask(__name__)





@app.get('/items')     
def get_items():
    return {"items": items}

@app.get('/item')     
def get_item():
    id = request.args.get('id')
    try:
        return items[id]
    except KeyError:
        return {'message': "Record doesn't exist"}, 404

@app.post('/item')
def add_item():
    request_data = request.get_json()
    if "name" not in request_data or "price" not in request_data:
        return {"message":"'name' and 'price' must be included in body"}, 400
    items[uuid.uuid4().hex] = request_data
    return {"message": "Item added succesfully"}, 201


@app.put('/item')
def update_item():
    
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


@app.delete('/item')     
def delete_item():
    id = request.args.get('id')
    if id == None:
        return {"message":"Given id not found"}, 404
    if id in items.keys():
        del items[id]
        return {'message': 'Item deleted successfully'}
    return {'message': "Record doesn't exist"}, 404