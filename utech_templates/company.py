from openerp.osv import fields, osv

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
                'federal_id': fields.char('Federal ID', size=32),
                'duns': fields.char('Duns', size=32),
     }

    

res_company()


class sale_order(osv.osv):
    _inherit="sale.order"
    _columns={
              'attention':fields.char('Attention', size=64, required=False),
              'ship_via':fields.char('Ship Via', size=64, required=False),
              }
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        invoice_vals['sale_id'] = order.id
        return invoice_vals
        
sale_order()

class account_invoice(osv.osv):
    _inherit="account.invoice"
    _columns={
              'sale_id' : fields.many2one('sale.order', "Sale Reference"),
              }
    
account_invoice()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):
        """ Inherit the original function of the 'stock' module in order to override some
            values if the picking has been generated by a sales order
        """
        invoice_vals = super(stock_picking, self)._prepare_invoice(cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.sale_id:
            invoice_vals['sale_id'] = picking.sale_id.id
        return invoice_vals
stock_picking()

class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"

    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        result = super(sale_advance_payment_inv, self)._prepare_advance_invoice_vals(cr, uid, ids, context=context)
        res = []
        for sale_id, inv_values in result:
            inv_values['sale_id'] = sale_id
            res.append((sale_id, inv_values))
        return res
        
sale_advance_payment_inv()