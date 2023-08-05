from odoo import models, fields, api

def calculate_route_from_pricelist(pricelist_id):
        # Tarifas
        VENTA_DEPOSITO_LIBRERIA            = 1
        VENTA_DIRECTA_FINAL                = 2
        VENTA_DIRECTA_LIBRERIA             = 3
        VENTA_DEPOSITO_DISTRI              = 4
        VENTA_DIRECTA_BIBLIOTECA_SOCIAL    = 5
        VENTA_DIRECTA_BIBLIOTECA_MUNICIPAL = 6
        VENTA_DEPOSITO_ESPAI_LLAVORS       = 7
        VENTA_DIRECTA_ODILO                = 8
        VENTA_DIRECTA_BIBLIOTECA15         = 9
        VENTA_DIRECTA_ALTRES_LLETRES       = 10

        # Rutas
        RUTA_DIRECTA  = 3
        RUTA_DEPOSITO = 6

        route = None
        if (pricelist_id == VENTA_DEPOSITO_LIBRERIA or
            pricelist_id == VENTA_DEPOSITO_DISTRI or
            pricelist_id == VENTA_DEPOSITO_ESPAI_LLAVORS):
            route = RUTA_DEPOSITO
        elif (pricelist_id == VENTA_DIRECTA_FINAL or
                pricelist_id == VENTA_DIRECTA_LIBRERIA or
                pricelist_id == VENTA_DIRECTA_BIBLIOTECA_SOCIAL or
                pricelist_id == VENTA_DIRECTA_ODILO or
                pricelist_id == VENTA_DIRECTA_BIBLIOTECA15 or
                pricelist_id == VENTA_DIRECTA_ALTRES_LLETRES or
                pricelist_id == VENTA_DIRECTA_BIBLIOTECA_MUNICIPAL):
            route = RUTA_DIRECTA
        return route

class EditorialSaleOrder(models.Model):
    """ Extend sale.order template for editorial management """

    _description = "Editorial Sale Order"
    _inherit = 'sale.order' # odoo/addons/sale/models/sale.py

    @api.onchange('order_line')
    def default_pricelist_when_order_line(self):
        for order in self:
            if self.order_line:
                route = calculate_route_from_pricelist(self.pricelist_id.id)
                if route != None:
                    for line in self.order_line:
                        line.route_id = route

    @api.onchange('pricelist_id')
    def default_pricelist_when_pricelist_id(self):
        for order in self:
            if self.order_line:
                route = calculate_route_from_pricelist(self.pricelist_id.id)
                if route != None:
                    for line in self.order_line:
                        line.route_id = route
                        line.price_unit = line._get_display_price(line.product_id)

class EditorialSaleOrderLine(models.Model):
    """ Extend sale.order.line template for editorial management """
    _description = "Editorial Sale Order Line"
    _inherit = 'sale.order.line' # odoo/addons/sale/models/sale.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)
    product_list_price = fields.Float(string='PVP', related='product_id.list_price', readonly=True)
