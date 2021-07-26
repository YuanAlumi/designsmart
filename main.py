from flask import Flask, request
from flask_restful import Resource, Api
import xmlrpc.client

app = Flask(__name__)
api = Api(app)

url = 'https://tecolutions-2.odoo.com'
db = 'tecolutions-2'
username = 'yuan@tecolutions.com'
password = 'abf6cd51d0a7aadc3c826502225f5f86a4a654be'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

class updateQTY(Resource):
    def get(self, newQty):
        # To update stock quantity, there are two steps to follow. 1. create a new push quantity record. 2. call change_product_qty method.
        # 1 create a new new quantity record in stock.change.product.qty model
        push_quantity = models.execute_kw(db, uid, password, 'stock.change.product.qty', 'create', [{
            'new_quantity': int(newQty), 'product_id': '1', 'product_tmpl_id': '1'}])
        # 2 call change_product_qty method to commit the change i.e., update the quantity
        models.execute_kw(db, uid, password, 'stock.change.product.qty',
                          'change_product_qty', [[push_quantity]])
        return {"Message": "You have successfully updated the quantity to {0}".format(newQty)}


api.add_resource(updateQTY, '/<string:newQty>')

if __name__ == '__main__':
    app.run(debug=True)
