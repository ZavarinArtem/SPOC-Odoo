# -*- coding: utf-8 -*-
# from odoo import http


# class StockPickingInfoLot(http.Controller):
#     @http.route('/stock_picking_info_lot/stock_picking_info_lot', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_info_lot/stock_picking_info_lot/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_info_lot.listing', {
#             'root': '/stock_picking_info_lot/stock_picking_info_lot',
#             'objects': http.request.env['stock_picking_info_lot.stock_picking_info_lot'].search([]),
#         })

#     @http.route('/stock_picking_info_lot/stock_picking_info_lot/objects/<model("stock_picking_info_lot.stock_picking_info_lot"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_info_lot.object', {
#             'object': obj
#         })
