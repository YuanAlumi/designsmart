# 1. Create a new stock move for project product
newStockMove = {
                'product_id': 1579,
                'company_id': 1,
                'date': '2021-08-01 09:00:00',
                'location_dest_id': 8,
                'location_id': 15,
                'name': 'New',
                'procure_method': 'make_to_stock',
                'product_uom_qty': 1,
                'product_uom': 1
                } 
models.execute_kw(db, uid, password, 'stock.move', 'create', [newStockMove])

# 2a. Create a M.O. add the id from step one to move_finished_ids (get the id)
newMO = {
        'product_id': 1579,
        'company_id': 1,
        'consumption': 'flexible',
        'date_planned_start': '2021-08-01 09:00:00',
        'location_dest_id': 8,
        'location_src_id': 8,
        'picking_type_id': 13,
        'product_qty': 1,
        'product_uom_id': 1,
        }
models.execute_kw(db, uid, password, 'mrp.production', 'create', [newMO])

# 2b. Update move_finished_ids
iD = 55
attr = {
        'move_finished_ids': [313]
       }
models.execute_kw(db, uid, password, 'mrp.production', 'write', [[iD], attr])

# 3 Create other stock moves for componenst and add the M.O. id to raw_material_production_id
newStockMove = {
                'product_id': 1578,
                'company_id': 1,
                'date': '2021-07-30 09:00:00',
                'location_dest_id': 15,
                'location_id': 8,
                'name': '[Thermal Plus Prefab Window W1800 H1200 IS OR] Thermal Plus Prefab Window W1800 H1200 IS OR',
                'procure_method': 'make_to_stock',
                'product_uom_qty': 39,
                'product_uom': 1,
                'raw_material_production_id': 56,
                'picking_type_id': 13,
                'warehouse_id': 1

                }                          
models.execute_kw(db, uid, password, 'stock.move', 'create', [newStockMove])
