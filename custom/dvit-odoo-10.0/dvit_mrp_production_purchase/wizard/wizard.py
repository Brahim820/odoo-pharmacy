from odoo import models, fields, api


class WizMrpPurchaseLine(models.TransientModel):
    _name = 'wiz.mrp.po.line'
    wiz_mrp_po_id = fields.Many2one(string="purchase wizard",comodel_name="wiz.mrp.purchase", )
    m_id = fields.Integer(string="Move ID", )

    m_desc = fields.Text(string="Notes", )
    m_product = fields.Many2one(string="Product",comodel_name="product.product")


class WizMrpPurchase(models.TransientModel):
    _name = 'wiz.mrp.purchase'
    is_tender = fields.Boolean(string="Create tender", )
    request_all = fields.Boolean(string="Request all materials",help="Request all materials or only unavailable materials.")
    vendor_id = fields.Many2one(string="Vendor",comodel_name="res.partner",domain="[('supplier', '=', 1)]",)
    wiz_po_line_ids = fields.One2many(string="Materials",comodel_name="wiz.mrp.po.line",inverse_name="wiz_mrp_po_id",store=True,
                                      # compute="create_line_ids",
                                      #  store=True,
                                      )
    notes = fields.Text('Notes')


    @api.onchange('vendor_id')
    def create_line_ids(self):
        production_id = self.env['mrp.production'].browse(self._context.get('active_id'))
        line_vals = []
        idd = self.id
        for move_id in production_id.move_raw_ids:
            line_id = self.env['wiz.mrp.po.line'].create({
                'm_id': move_id.id,
                'm_product': move_id.product_id.id,
                'm_desc': move_id.product_id.name,
                'wiz_mrp_po_id': idd,
            })
            # self.wiz_po_line_ids += line_id
            line_vals.append(line_id.id)
        self.wiz_po_line_ids =line_vals

    @api.multi
    def _prepare_po(self):
        idd = self.id
        is_tender = self.is_tender
        production_id = self.env['mrp.production'].browse(self._context.get('active_id'))
        picking_type_id = self.env['stock.picking.type'].sudo().search([
        ('warehouse_id','=',production_id.move_raw_ids[0].group_id.procurement_ids[0].warehouse_id.id),
        ('code','=','incoming')
        ])

        p_vals = {
        'origin': production_id.origin + ':' + production_id.name,
        'date_planned': production_id.date_planned_start,
        'picking_type_id': picking_type_id.id,
        'notes': self.notes,
        }

        #add if here and create PT instead of PO
        if is_tender:
            po_id = self.env['purchase.requisition'].sudo().create(p_vals)
        else:
            p_vals.update({'partner_id': self.vendor_id.id,})
            po_id = self.env['purchase.order'].sudo().create(p_vals)

        if self.request_all:
            raw_ids = production_id.move_raw_ids
        else:
            raw_ids = production_id.move_raw_ids.filtered(lambda m: m.state == 'confirmed')

        for rm_line in raw_ids:
            wiz_line = self.env['wiz.mrp.po.line'].search([
            ('m_id','=',rm_line.id),])[-1]
            m_desc = wiz_line.m_desc
            pl_vals = {
            'product_id': rm_line.product_id.id,
            'name': m_desc or 'notes not found',
            'product_qty': rm_line.product_uom_qty,
            }
            if is_tender:
                pl_vals.update({
                'schedule_date': production_id.date_planned_start,
                'product_uom_id': rm_line.product_uom.id,
                'requisition_id': po_id.id,
                })
                self.env['purchase.requisition.line'].sudo().create(pl_vals)
            else:
                pl_vals.update({
                'date_planned': production_id.date_planned_start,
                'price_unit': rm_line.product_id.standard_price,
                'product_uom': rm_line.product_uom.id,
                'order_id': po_id.id,
                })
                self.env['purchase.order.line'].sudo().create(pl_vals)

        if is_tender:
            po_id.action_in_progress()
            production_id.purchase_req_ids += po_id
        else:
            po_id.action_set_date_planned()
            production_id.purchase_ids += po_id

        return po_id

    @api.multi
    def add_po(self):
        po_id = self._prepare_po()
        for l in self.env['wiz.mrp.po.line'].search([]):
            l.unlink()
        for wiz in self.env['wiz.mrp.purchase'].search([]):
            wiz.unlink()
        return po_id
