from flask import Flask, request
from flask_restful import Resource, Api
import xmlrpc.client

app = Flask(__name__)
api = Api(app)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

class CreateMo(Resource):
    def get(self, newQty):
        ## initiating connection with Odoo cloud instance
        url = 'https://alumi-test-20210818.odoo.com'
        db = 'alumi-test-20210818'
        username = 'yuan.gao@alumi.co.nz'
        password = '1554ccddf4f8a56a776aa0ce5b1342fdf541bedb'
        ## Enable XMLRPC protocol in Python. 
        import xmlrpc.client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        ## create new XMLRPC model
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password,
        'res.partner', 'check_access_rights',
        ['write'], {'raise_exception': False})

        ## Input variables
        prjPrdName = 'Love Maimai'
        bomLineProdId = 1586
        bomLineProdTmplId = 2264

        ## Project Level Product
        ## Create a new product project
        product = [{'display_name': prjPrdName,
        'name': prjPrdName,
        'categ_id': 206,
        'uom_id': 1,
        'uom_po_id': 1,
        'type': 'product',
        'purchase_ok': False,
        'property_stock_production': 15,
        'property_stock_inventory': 14,
        'has_available_route_ids': True,
        'purchase_method': 'receive',
        'purchase_line_warn': 'no-message',
        'route_ids': [15, 1],
        'sale_line_warn': 'no-message'}]
        prjProdId = models.execute_kw(db, uid, password, 'product.product', 'create', product)

        ## Check an existing project product.
        prjPrdDetail = models.execute_kw(db, uid, password,
        'product.product', 'search_read',
        [[['id', '=', prjProdId]]])
        prjPrdTmplId = prjPrdDetail[0]['product_tmpl_id'][0]


        ##BOM
        ## Create a new BOM
        bom = [{'product_tmpl_id': prjPrdTmplId, ## This is the product_tmpl_id of the project product.
        'product_qty': 1.0,
        'product_uom_id': 1,
        'product_uom_category_id': 1,
        'ready_to_produce': 'asap',
        'picking_type_id': 13,}]
        bomId = models.execute_kw(db, uid, password, 'mrp.bom', 'create', bom)

        ##BOM Line
        ## Create a new BoM Line
        bomLine = [{'product_id': bomLineProdId, ## product id of the BOM line component
        'product_tmpl_id': bomLineProdTmplId, ## product template id the BOM line component
        'product_qty': 1.0,
        'product_uom_id': 1,
        'product_uom_category_id': 1,
        'bom_id': bomId ## id of the BOM
        }]
        bomLineId = models.execute_kw(db, uid, password, 'mrp.bom.line', 'create', bomLine)
        


api.add_resource(CreateMo, '/<string:newQty>')

if __name__ == '__main__':
    app.run(debug=True)
