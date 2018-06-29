# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################


from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)


class MarketplaceConfigSettings(models.TransientModel):
    _name = 'marketplace.config.settings'
    _inherit = "res.config.settings"

    @api.model
    def _default_category(self):
        obj = self.env["product.category"].search([('name', '=', _('All'))])
        return obj[0] if obj else self.env["product.category"]

    @api.model
    def get_journal_id(self):
        obj = self.env["account.journal"].search([('name', '=', _('Vendor Bills'))])
        return obj[0] if obj else self.env["account.journal"]

    auto_product_approve = fields.Boolean(string="Auto Product Approve")
    internal_categ = fields.Many2one(
        "product.category", string="Internal Category", required="1")
    warehouse_location_id = fields.Many2one(
        "stock.location", string="Warehouse Location", domain="[('usage', '=', 'internal')]", required="1")
    default_warehouse = fields.Many2one(
        "stock.warehouse", string="Warehouse", required="1")
    seller_payment_limit = fields.Integer(string="Seller Payment Limit")
    next_payment_requset = fields.Integer(string="Next Payment Request")
    group_mp_product_variant = fields.Boolean(
        string="Allow sellers for several product attributes, defining variants (Example: size, color,...)",
        group='odoo_marketplace.marketplace_seller_group',
        implied_group='product.group_product_variant'
    )
    group_mp_shop_allow = fields.Boolean(
        string="Allow sellers to manage seller shop.",
        group='odoo_marketplace.marketplace_seller_group',
        implied_group='odoo_marketplace.group_marketplace_seller_shop'
    )
    group_mp_product_pricelist = fields.Boolean(
        string="Allow sellers for Advanced pricing on product using pricelist.",
        group='odoo_marketplace.marketplace_seller_group',
        implied_group='product.group_product_pricelist'
    )

    # Inventory related field
    auto_approve_qty = fields.Boolean(string="Auto Quantity Approve")

    # Seller related field
    auto_approve_seller = fields.Boolean(string="Auto Seller Approve")
    global_commission = fields.Float(string="Global Commission")

    invoicing_type = fields.Selection(
        [('by_customer_and_seller', 'Based On Customer And Seller')], string="Invoicing Type", required=True)
    # invoicing_type = fields.Selection([('by_customer_and_seller','Based On Customer And Seller'),('by_customer','Based On Customer'),('by_seller','Based On Seller')], string="Invoicing Type")

    # Mail notification related fields
    enable_notify_admin_4_new_seller = fields.Boolean(string="Enable")
    enable_notify_seller_4_new_seller = fields.Boolean(string="Enable")
    enable_notify_admin_on_seller_approve_reject = fields.Boolean(
        string="Enable")
    enable_notify_seller_on_approve_reject = fields.Boolean(string="Enable")
    enable_notify_admin_on_product_approve_reject = fields.Boolean(
        string="Enable")
    enable_notify_seller_on_product_approve_reject = fields.Boolean(
        string="Enable")
    enable_notify_seller_on_new_order = fields.Boolean(string="Enable")

    notify_admin_4_new_seller = fields.Many2one(
        "mail.template", string="Notification for Admin", domain="[('model_id.model','=','res.partner')]")
    notify_seller_4_new_seller = fields.Many2one(
        "mail.template", string="Notification for Seller", domain="[('model_id.model','=','res.partner')]")
    notify_admin_on_seller_approve_reject = fields.Many2one(
        "mail.template", string="Notification for Admin", domain="[('model_id.model','=','res.partner')]")
    notify_seller_on_approve_reject = fields.Many2one(
        "mail.template", string="Notification for Seller", domain="[('model_id.model','=','res.partner')]")
    notify_admin_on_product_approve_reject = fields.Many2one(
        "mail.template", string="Notification for Admin", domain="[('model_id.model','=','product.template')]")
    notify_seller_on_product_approve_reject = fields.Many2one(
        "mail.template", string="Notification for Seller", domain="[('model_id.model','=','product.template')]")
    notify_seller_on_new_order = fields.Many2one(
        "mail.template", string="Notification for Seller", domain="[('model_id.model','=','sale.order.line')]")

    # Seller shop/profile releted field
    product_count = fields.Boolean(
        string="Show seller's product count on website.")
    sale_count = fields.Boolean(string="Show seller's sales count on website.")
    shipping_address = fields.Boolean(
        string="Show seller's shipping address on website.")
    seller_since = fields.Boolean(string="Show seller since Date on website.")
    seller_t_c = fields.Boolean(
        string="Show seller's Terms & Conditions on website.")
    seller_contact_btn = fields.Boolean(
        string='Show "Contact Seller" Button on website.')
    seller_review = fields.Boolean(
        string='Show Seller Review on website.')
    return_policy = fields.Boolean(
        string="Show seller's Retrun Policy on website.")
    shipping_policy = fields.Boolean(
        string="Show Seller's Shipping Policy on website.")
    recently_product = fields.Integer(
        string="# of products for recently added products menu. ")
    # Seller Review settings field
    review_load_no = fields.Integer(
        string="No. of Reviews to load", help="Set default numbers of review to show on website.")
    review_auto_publish = fields.Boolean(
        string="Auto Publish", help="Publish Customer's review automatically.")
    show_seller_list = fields.Boolean(
        string='Show Sellers List on website.')
    show_seller_shop_list = fields.Boolean(
        string='Show Seller Shop List on website.')
    landing_page_banner = fields.Binary(string="Landing Page Banner")
    seller_payment_journal_id = fields.Many2one("account.journal", string="Seller Payment Journal", required=True, default=get_journal_id, domain="[('type', '=', 'purchase')]")
    mp_currency_id = fields.Many2one('res.currency', "Marketplace Currency")

    # TranslateMarketplaceConfigSettings obj
    trans_mp_config_setting_id = fields.Many2one(
        "translate.marketplace.config.settings", string="Translate Config Settings")

    show_visit_shop = fields.Boolean("Show visit shop link on product page")
    show_sell_menu_header = fields.Boolean("Show Sell menu in header")
    show_sell_menu_footer = fields.Boolean("Show Sell menu in footer")

    seller_payment_product_id = fields.Many2one("product.product", string="Seller Payment Product", required=True, domain="[('sale_ok', '=', False),('purchase_ok', '=', False),('type','=','service')]")

    @api.onchange("warehouse_location_id")
    def on_change_location_id(self):
        wl_obj = self.env["stock.location"].sudo().browse(
            self.warehouse_location_id.id)
        wh_obj = self.env["stock.warehouse"]
        whs = wh_obj.search([('view_location_id.parent_left', '<=', wl_obj.parent_left),
                             ('view_location_id.parent_right', '>=', wl_obj.parent_left)], limit=1)
        if whs:
            self.default_warehouse = whs.id
        # else:
        #     self.default_warehouse = self.env["stock.warehouse"]

    @api.one
    def set_default_values(self):

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'auto_product_approve', self.auto_product_approve)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'internal_categ', self.internal_categ.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'default_warehouse', self.default_warehouse.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'warehouse_location_id', self.warehouse_location_id.id)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'auto_approve_qty', self.auto_approve_qty)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'auto_approve_seller', self.auto_approve_seller)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'global_commission', self.global_commission)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'invoicing_type', self.invoicing_type)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_payment_limit', self.seller_payment_limit)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'next_payment_requset', self.next_payment_requset)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_admin_4_new_seller', self.enable_notify_admin_4_new_seller)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_seller_4_new_seller', self.enable_notify_seller_4_new_seller)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_admin_on_seller_approve_reject', self.enable_notify_admin_on_seller_approve_reject)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_seller_on_approve_reject', self.enable_notify_seller_on_approve_reject)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_admin_on_product_approve_reject', self.enable_notify_admin_on_product_approve_reject)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_seller_on_product_approve_reject', self.enable_notify_seller_on_product_approve_reject)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'enable_notify_seller_on_new_order', self.enable_notify_seller_on_new_order)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_admin_4_new_seller', self.notify_admin_4_new_seller.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_seller_4_new_seller', self.notify_seller_4_new_seller.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_admin_on_seller_approve_reject', self.notify_admin_on_seller_approve_reject.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_seller_on_approve_reject', self.notify_seller_on_approve_reject.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_admin_on_product_approve_reject', self.notify_admin_on_product_approve_reject.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_seller_on_product_approve_reject', self.notify_seller_on_product_approve_reject.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'notify_seller_on_new_order', self.notify_seller_on_new_order.id)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'product_count', self.product_count)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'sale_count', self.sale_count)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'shipping_address', self.shipping_address)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_since', self.seller_since)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_t_c', self.seller_t_c)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_contact_btn', self.seller_contact_btn)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_review', self.seller_review)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'return_policy', self.return_policy)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'shipping_policy', self.shipping_policy)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'recently_product', self.recently_product)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'review_load_no', self.review_load_no)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'review_auto_publish', self.review_auto_publish)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'landing_page_banner', self.landing_page_banner)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'show_seller_list', self.show_seller_list)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'show_seller_shop_list', self.show_seller_shop_list)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'trans_mp_config_setting_id', self.trans_mp_config_setting_id.id)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_payment_journal_id', self.seller_payment_journal_id.id)
        seller_paymnet = self.env["seller.payment"].search([])
        if not seller_paymnet:
            self.env['ir.values'].sudo().set_default(
                'marketplace.config.settings', 'mp_currency_id', self.mp_currency_id.id)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'show_visit_shop', self.show_visit_shop)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'show_sell_menu_header', self.show_sell_menu_header)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'show_sell_menu_footer', self.show_sell_menu_footer)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'group_mp_product_variant', self.group_mp_product_variant)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'group_mp_shop_allow', self.group_mp_shop_allow)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'group_mp_product_pricelist', self.group_mp_product_pricelist)

        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'seller_payment_product_id', self.seller_payment_product_id.id)
        return True

    @api.model
    def get_default_values(self, fields=None):
        try:
            trans_mp_config_setting_obj = self.env["translate.marketplace.config.settings"].browse([int(self.env['ir.values'].get_default(
                'marketplace.config.settings', 'trans_mp_config_setting_id'))])
        except Exception, e:
            _logger.info(
                "---Marketplace Miscellaneous setting is not configure -----------------------------")
            trans_mp_config_setting_obj = False

        temp_1 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_email_template_for_admin_by_seller')[1]
        temp_2 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_email_template_for_seller_by_admin')[1]
        temp_3 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_email_template_for_seller_status_change_to_admin')[1]
        temp_4 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_email_template_for_seller_status_change_to_seller')[1]
        temp_5 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_template_for_product_status_changeto_admin')[1]
        temp_6 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_template_for_product_status_change_to_seller')[1]
        temp_7 = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_template_for_order_to_seller')[1]

        auto_product_approve = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'auto_product_approve')
        internal_categ = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'internal_categ') or self._default_category().id
        default_warehouse = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'default_warehouse')
        warehouse_location_id = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'warehouse_location_id') or self._default_location().id

        auto_approve_qty = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'auto_approve_qty')

        auto_approve_seller = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'auto_approve_seller')
        global_commission = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'global_commission')
        invoicing_type = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'invoicing_type') or "by_customer_and_seller"
        seller_payment_limit = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_payment_limit')
        next_payment_requset = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'next_payment_requset')

        enable_notify_admin_4_new_seller = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_admin_4_new_seller')
        enable_notify_seller_4_new_seller = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_seller_4_new_seller')
        enable_notify_admin_on_seller_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_admin_on_seller_approve_reject')
        enable_notify_seller_on_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_seller_on_approve_reject')
        enable_notify_admin_on_product_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_admin_on_product_approve_reject')
        enable_notify_seller_on_product_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_seller_on_product_approve_reject')
        enable_notify_seller_on_new_order = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'enable_notify_seller_on_new_order')

        notify_admin_4_new_seller = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_admin_4_new_seller') or temp_1
        notify_seller_4_new_seller = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_seller_4_new_seller') or temp_2
        notify_admin_on_seller_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_admin_on_seller_approve_reject') or temp_3
        notify_seller_on_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_seller_on_approve_reject') or temp_4
        notify_admin_on_product_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_admin_on_product_approve_reject') or temp_5
        notify_seller_on_product_approve_reject = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_seller_on_product_approve_reject') or temp_6
        notify_seller_on_new_order = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'notify_seller_on_new_order') or temp_7

        product_count = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'product_count')
        sale_count = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'sale_count')
        shipping_address = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'shipping_address')
        seller_since = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_since')
        seller_t_c = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_t_c')
        seller_contact_btn = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_contact_btn')
        seller_review = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_review')
        return_policy = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'return_policy')
        shipping_policy = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'shipping_policy')
        recently_product = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'recently_product')
        review_load_no = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'review_load_no')
        review_auto_publish = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'review_auto_publish')
        landing_page_banner = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'landing_page_banner')
        show_seller_list = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'show_seller_list')
        show_seller_shop_list = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'show_seller_shop_list')
        trans_mp_config_setting_id = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'trans_mp_config_setting_id')
        seller_payment_journal_id = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_payment_journal_id') or self.get_journal_id().id
        mp_currency_id = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'mp_currency_id') or self.env.user.company_id.currency_id.id

        show_visit_shop = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'show_visit_shop')
        show_sell_menu_header = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'show_sell_menu_header')
        show_sell_menu_footer = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'show_sell_menu_footer')
        group_mp_product_variant = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'group_mp_product_variant')
        group_mp_shop_allow = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'group_mp_shop_allow')
        group_mp_product_pricelist = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'group_mp_product_pricelist')

        seller_payment_product_id = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'seller_payment_product_id')
        return {
            'auto_product_approve': auto_product_approve,
            'internal_categ': internal_categ,
            'default_warehouse': default_warehouse,
            'warehouse_location_id': warehouse_location_id,
            'auto_approve_qty': auto_approve_qty,

            'auto_approve_seller': auto_approve_seller,
            'global_commission': global_commission,
            'invoicing_type': invoicing_type,
            'seller_payment_limit': seller_payment_limit,
            'next_payment_requset': next_payment_requset,

            'enable_notify_admin_4_new_seller': enable_notify_admin_4_new_seller,
            'enable_notify_seller_4_new_seller': enable_notify_seller_4_new_seller,
            'enable_notify_admin_on_seller_approve_reject': enable_notify_admin_on_seller_approve_reject,
            'enable_notify_seller_on_approve_reject': enable_notify_seller_on_approve_reject,
            'enable_notify_admin_on_product_approve_reject': enable_notify_admin_on_product_approve_reject,
            'enable_notify_seller_on_product_approve_reject': enable_notify_seller_on_product_approve_reject,
            'enable_notify_seller_on_new_order': enable_notify_seller_on_new_order,

            'notify_admin_4_new_seller': notify_admin_4_new_seller,
            'notify_seller_4_new_seller': notify_seller_4_new_seller,
            'notify_admin_on_seller_approve_reject': notify_admin_on_seller_approve_reject,
            'notify_seller_on_approve_reject': notify_seller_on_approve_reject,
            'notify_admin_on_product_approve_reject': notify_admin_on_product_approve_reject,
            'notify_seller_on_product_approve_reject': notify_seller_on_product_approve_reject,
            'notify_seller_on_new_order': notify_seller_on_new_order,

            'product_count': product_count,
            'sale_count': sale_count,
            'shipping_address': shipping_address,
            'seller_since': seller_since,
            'seller_t_c': seller_t_c,
            'seller_contact_btn': seller_contact_btn,
            'return_policy': return_policy,
            'shipping_policy': shipping_policy,
            'recently_product': recently_product,
            'review_load_no': review_load_no,
            'review_auto_publish': review_auto_publish,
            'seller_review': seller_review,
            'landing_page_banner': landing_page_banner,
            'show_seller_list': show_seller_list,
            'show_seller_shop_list': show_seller_shop_list,
            'trans_mp_config_setting_id': trans_mp_config_setting_id,
            "seller_payment_journal_id" : seller_payment_journal_id,
            "mp_currency_id": mp_currency_id,

            'show_visit_shop': show_visit_shop,
            'show_sell_menu_header': show_sell_menu_header,
            'show_sell_menu_footer': show_sell_menu_footer,
            'group_mp_product_variant': group_mp_product_variant,
            'group_mp_shop_allow': group_mp_shop_allow,
            'group_mp_product_pricelist': group_mp_product_pricelist,

            'seller_payment_product_id': seller_payment_product_id,
        }

    @api.model
    def mp_config_translatable(self):
        try:
            trans_mp_config_setting_obj = self.env["translate.marketplace.config.settings"].browse([int(self.env['ir.values'].get_default(
                'marketplace.config.settings', 'trans_mp_config_setting_id'))])
        except Exception, e:
            _logger.info(
                "---Marketplace Miscellaneous setting is not configure -----------------------------")
            trans_mp_config_setting_obj = False
        return {
            "term_and_condition" : trans_mp_config_setting_obj.term_and_condition if trans_mp_config_setting_obj else False,
            "message_to_publish" : trans_mp_config_setting_obj.message_to_publish if trans_mp_config_setting_obj else False,
            "sell_page_label" : trans_mp_config_setting_obj.sell_page_label if trans_mp_config_setting_obj else "Sell",
            "sellers_list_label" : trans_mp_config_setting_obj.sellers_list_label if trans_mp_config_setting_obj else "Seller List",
            "seller_shop_list_label" : trans_mp_config_setting_obj.seller_shop_list_label if trans_mp_config_setting_obj else "Seller Shop List",
            "seller_new_status_msg" : trans_mp_config_setting_obj.seller_new_status_msg if trans_mp_config_setting_obj else "Thank you for registering with us, to enjoy the benefits of our marketplace fill all your details and request for approval.",
            "seller_pending_status_msg" : trans_mp_config_setting_obj.seller_pending_status_msg if trans_mp_config_setting_obj else "Thank you for seller request, your request has been already sent for approval we'll process your request as soon as possible.",
        }

    @api.multi
    def execute(self):
        for rec in self:
            if rec.recently_product < 1 or rec.recently_product > 20:
                raise UserError(_("Recently Added Products count should be in range 1 to 20."))
            if rec.review_load_no < 1:
                raise UserError(_("Display Seller Reviews count should be more than 0."))
            if rec.global_commission < 0 or rec.global_commission >= 100:
                raise UserError(_("Global Commission should be greater than 0 and less than 100."))
            if rec.seller_payment_limit < 0 :
                raise UserError(_("Amount Limit can't be negative."))
            if rec.next_payment_requset < 0:
                raise UserError(_("Minimum Gap can't be negative."))
            # Update All Seller Setting
            all_seller_objs = rec.env["res.partner"].search(
                [("seller", "=", True), ("state", "=", "approved")])
            for seller_obj in all_seller_objs:
                if not seller_obj.set_seller_wise_settings:
                    vals = {
                        "commission": rec.global_commission,
                        "warehouse_id": rec.default_warehouse.id,
                        "location_id": rec.warehouse_location_id.id,
                        "auto_product_approve": rec.auto_product_approve,
                        "seller_payment_limit": rec.seller_payment_limit,
                        "next_payment_request": rec.next_payment_requset,
                        "auto_approve_qty": rec.auto_approve_qty,
                        "show_seller_since": rec.seller_since,
                        "show_seller_address": rec.shipping_address,
                        "show_product_count": rec.product_count,
                        "show_sale_count": rec.sale_count,
                        "show_return_policy": rec.return_policy,
                        "show_shipping_policy": rec.shipping_policy,
                        "show_seller_review": rec.seller_review,
                    }
                    seller_obj.write(vals)

            # Update All Seller Shop Setting
            all_seller_shop_objs = rec.env["seller.shop"].search(
                [("state", "=", "approved")])
            for seller_shop_obj in all_seller_shop_objs:
                if not seller_shop_obj.set_seller_wise_settings:
                    vals = {
                        "product_count": rec.product_count,
                        "sale_count": rec.sale_count,
                        "shipping_address": rec.shipping_address,
                        "seller_since": rec.seller_since,
                        "seller_t_c": rec.seller_t_c,
                        "seller_contact_btn": rec.seller_contact_btn,
                    }
                    seller_shop_obj.write(vals)
        return super(MarketplaceConfigSettings, self).execute()

    @api.model
    def _seller_warehouse(self):
        """ Set default warehouse"""
        user_obj = self.env.user
        if user_obj:
            company_id = user_obj.company_id.id
            warehouse_ids = self.env["stock.warehouse"].search(
                [("company_id", '=', company_id)])
            return warehouse_ids[0] if warehouse_ids else self.env["stock.warehouse"]
        return self.env["stock.warehouse"]

    @api.model
    def _default_location(self):
        """ Set default location """
        user_obj = self.env.user
        if user_obj:
            company_id = user_obj.company_id.id
            location_ids = self.env["stock.location"].sudo().search(
                [("company_id", '=', company_id), ("name", "=", "Stock"), ('usage', '=', 'internal')])
            return location_ids[0] if location_ids else self.env["stock.location"]
        return self.env["stock.location"].sudo().search([('usage', '=', 'internal')])[0]

    @api.multi
    def update_tanslate_field(self):
        self.ensure_one()
        view_id = self.env.ref(
            'odoo_marketplace.translate_marketplace_config_settings_form_view').id
        if self.env['ir.values'].get_default('marketplace.config.settings', 'trans_mp_config_setting_id'):
            try:
                res_id = int(self.env['ir.values'].get_default(
                    'marketplace.config.settings', 'trans_mp_config_setting_id'))
            except Exception, e:
                raise UserError(e)
        else:
            # For first time
            config_dict = self.mp_config_translatable()
            res_id = self.env["translate.marketplace.config.settings"].sudo().create({"term_and_condition": config_dict["term_and_condition"], "message_to_publish": config_dict[
                "message_to_publish"], "sell_page_label": config_dict["sell_page_label"], "sellers_list_label": config_dict["sellers_list_label"], "seller_shop_list_label": config_dict["seller_shop_list_label"], "seller_new_status_msg": config_dict["seller_new_status_msg"], "seller_pending_status_msg": config_dict["seller_pending_status_msg"]}).id
            self.env['ir.values'].sudo().set_default(
                'marketplace.config.settings', 'trans_mp_config_setting_id', res_id)
        return {
            'name': 'Marketplace Configuration Settings',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'translate.marketplace.config.settings',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': "inline",
            'res_id': res_id,
        }


class TranslateMarketplaceConfigSettings(models.Model):
    _name = 'translate.marketplace.config.settings'
    _description = "This model contains translatable fields of marketplace config settings."

    term_and_condition = fields.Html(string="Terms & Conditions", translate=True)
    message_to_publish = fields.Text(
        string="Review feedback message", help="Message to Customer on review publish.", translate=True)
    sell_page_label = fields.Char(
        string="Sell Link Label", default="Sell", translate=True)
    sellers_list_label = fields.Char(
        string="Seller List Link Label", default="Sellers List", translate=True)
    seller_shop_list_label = fields.Char(
        string="Seller Shop List Link Label", default="Seller Shop List", translate=True)
    seller_new_status_msg = fields.Text(
        string="For New Status", default="Thank you for registering with us, to enjoy the benefits of our marketplace fill all your details and request for approval.", translate=True)
    seller_pending_status_msg = fields.Text(
        string="For Pending Status", default="Thank you for seller request, your request has been already sent for approval we'll process your request as soon as possible.", translate=True)
    # seller_denied_status_msg = fields.Text(
    #     string="For Denied Status", default="Sorry To Say! Your seller account has been denied now.", translate=True)

    @api.multi
    def save(self):
        self.ensure_one()
        view_id = self.env.ref(
            'odoo_marketplace.marketplace_base_config_settings_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'marketplace.config.settings',
            'view_type': 'form',
            'view_id': view_id,
            'view_mode': 'form',
            'target': 'inline',
        }
