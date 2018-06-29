#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import base64
import io
from odoo import _, api, fields, models, tools, SUPERUSER_ID
from wand.image import Image as wImage
from wand.drawing import Drawing
from wand.color import Color
from .arabic_reshaper import reshape
from .bidi.algorithm import get_display
from escpos.printer import *
from odoo.exceptions import UserError, ValidationError
import math


class PosOrder(models.Model):
    _inherit = "pos.order"
    #FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    @api.model
    def pos_malik(self, data):
        try:
            y = 0
            for aa in data['receipt']['orderlines']:
                y = y + 1
            fonts = [os.path.dirname(__file__) + '/img/KacstOffice.ttf', os.path.dirname(__file__) + '/img/amiri-regular.ttf']
            draw = Drawing()
            img = wImage(width=500, height=260 + y * 75 + 300, background=Color('#ffffff'))
            draw.text_alignment = 'center';
            draw.text_antialias = True
            draw.text_encoding = 'utf-8'
            draw.text_kerning = 0.0
            draw.font = fonts[0]
            draw.font = fonts[1]
            draw.font_size = 28
            x = 260
            if data['receipt']['company']['name']:
                draw.text(495 / 2, 20, get_display(reshape(u''.join(data['receipt']['company']['name']))));
            if data['receipt']['company']['email']:
                draw.text(495 / 2, 50, get_display(reshape(u''.join(data['receipt']['company']['email']))));
            if data['receipt']['company']['website']:
                draw.text(495 / 2, 80, get_display(reshape(u''.join(data['receipt']['company']['website']))));
            if data['receipt']['company']['phone']:
                draw.text(495 / 2, 110, get_display(reshape(u''.join(data['receipt']['company']['phone']))));
            if data['receipt']['company']['vat']:
                draw.text(495 / 2, 140, get_display(reshape(u''.join(data['receipt']['company']['vat']))) + " : " + get_display(
                    reshape(u''.join(u"الرقم الضريبي"))));

            draw.text_alignment = 'right';
            draw.text(500, 170,
                      "...........................................................................................................")
            draw.text(500, 175,
                      "...........................................................................................................")

            draw.text(495, 200, get_display(reshape(u'الصنـــف')));
            draw.text(160, 200, get_display(reshape(u'الكميـــة')));
            draw.text(60, 200, get_display(reshape(u'السعـــر\n')))
            draw.text(500, 225,
                      "...........................................................................................................")
            draw.text(500, 230,
                      "...........................................................................................................")

            t = 0
            for malik in data['receipt']['orderlines']:
                draw.text(495, x, get_display(reshape(
                    u''.join(malik['product_name']))));
                draw.text(160, x + 30, str(malik['quantity']));
                draw.text(90, x + 30, str(float(malik['price_with_tax'])))
                if malik['discount'] > 0:
                    draw.text(410, x + 30, get_display(reshape(u'خصـم')));
                    draw.text(475, x + 30, str(malik['discount']));
                    draw.text(495, x + 30, '%');
                if malik['tax'] > 0:
                    draw.text(290, x + 30, get_display(reshape(u'ضريبة')));
                    draw.text(370, x + 30, str(malik['tax']));
                t += 1
                if t == y:
                    draw.text(500, x + 50, ".........................................................................................................................")
                    draw.text(500, x + 55, ".........................................................................................................................")
                else:
                    draw.text(500, x + 50, "------------------------------------------------------------------------------------------------------")
                x = x + 75
            draw.text(495, x, get_display(reshape(u' ضرائب:')));
            draw.text(75, x, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(410, x, str(float(data['receipt']['total_tax'])));

            draw.text(247, x, get_display(reshape(u' خصم:')));
            #draw.text(80, x + 40, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(170, x, str(float(data['receipt']['total_discount'])));

            draw.text(495, x + 40, get_display(reshape(u' اجمالي:')));
            draw.text(75, x + 40, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(410, x + 40, str(float(data['receipt']['total_with_tax'])));

            draw.text(247, x + 40, get_display(reshape(u'متبقي:')));
            #draw.text(80, x + 120, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(170, x + 40, str(float(data['receipt']['change'])));

            draw.text(500, x + 60, "...........................................................................................................")
            draw.text(500, x + 65, "...........................................................................................................")

            draw.text(495, x + 90, get_display(reshape(u'مقــــدم الخدمــــة :')));
            draw.text(300, x + 90, get_display(
                reshape(u''.join(data['receipt']['cashier']))));

            if data['receipt']['table']:
                draw.text(495, x + 130, get_display(reshape(u'الطاولة :')));
                draw.text(300, x + 130, get_display(reshape(u''.join(data['receipt']['table']))));
            if data['receipt']['customer_count']:
                draw.text(495, x + 170, get_display(reshape(u'الضيوف :')));
                draw.text(400, x + 170, str(data['receipt']['customer_count']));
            if data['receipt']['client']:
                draw.text(300, x + 170, get_display(reshape(u'الزبون :')));
                draw.text(225, x + 170, get_display(reshape(u''.join(data['receipt']['client']))));

            draw.text(500, x + 195, "...........................................................................................................")
            draw.text(500, x + 200, "...........................................................................................................")
            draw.text_alignment = 'center';
            draw.text(495 / 2, x + 225, get_display(reshape(u''.join(data['receipt']['name']))));
            draw.text(495 / 2, x + 265, get_display(reshape(u''.join(data['receipt']['date']['localestring']))));
            draw(img)
            if data['ar_al']:
                if data['pr_ip']:
                    try:
                        p = Network(data['pr_ip'])
                        f1 = io.BytesIO('img')
                        f = io.BytesIO('img')
                        f1.write(
                            base64.decodestring(tools.image_resize_image(self.env.user.company_id.logo, (300, 255))))
                        f.write(base64.decodestring(img.make_blob('png').encode('base64')))
                        p.set("CENTER", "B", "normal", 1, 1, False, False, False)
                        p.image(f1)
                        p.image(f)
                        if data['sh_dr']:
                            p.cashdraw(2)
                            p.cashdraw(5)
                        p.cut()
                    except:
                        pass
            return img.make_blob('png').encode('base64')
        except:
            pass
    #FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    @api.model
    def print_kitchen_malik_1(self, data):
        try:
            y = 0
            for aa in data['changes']['new']:
                y = y + 1
            y2 = 0
            for aaa in data['changes']['cancelled']:
                y2 = y2 + 1
            fonts = [os.path.dirname(__file__) + '/img/KacstOffice.ttf', os.path.dirname(__file__) + '/img/amiri-regular.ttf']
            draw = Drawing()
            img = wImage(width=500, height=260 + y * 70 + 100, background=Color('#ffffff'))
            draw.text_alignment = 'center';
            draw.text_antialias = True
            draw.text_encoding = 'utf-8'
            draw.text_kerning = 0.0
            draw.font = fonts[0]
            draw.font = fonts[1]
            draw.font_size = 25
            x = 310
            if data['changes']['name']:
                draw.text(495 / 2, 20, get_display(reshape(u''.join(data['changes']['name']))));
            if data['cl'] != "no":
                draw.text(495 / 2, 60, get_display(reshape(u''.join(data['cl']['name']))) + ": " + get_display(reshape(u''.join(u"اسم الزبون"))));
            draw.font_size = 40
            if data['changes']['floor']:
                draw.text(495 / 2, 120, get_display(reshape(u''.join(data['changes']['table']))) + "/" + get_display(reshape(u''.join(data['changes']['floor']))));
            if len(data['changes']['new']) > 0:
                draw.text(495 / 2, 180, get_display(reshape(
                    u''.join(u"جديد" + "/" + str(data['changes']['time']['hours']) + ":" + str(
                        data['changes']['time']['minutes'])))));
            if len(data['changes']['cancelled']) > 0:
                draw.text(495 / 2, 180, get_display(reshape(
                    u''.join(u"ملغي" + "/" + str(data['changes']['time']['hours']) + ":" + str(
                        data['changes']['time']['minutes'])))));
            draw.font_size = 28
            draw.text_alignment = 'right';
            draw.text(500, 205, "........................................................................................................")
            draw.text(500, 210, "..........................................................................................................")
            draw.text(495, 243, get_display(reshape(u'الصنـــف')));
            draw.text(85, 240, get_display(reshape(u'الكميـــة')));
            #draw.text(50, 240, get_display(reshape(u'النوع')));

            draw.text(500, 265, "................................................................................................................")
            draw.text(500, 270, "...........................................................................................................")
            ex = 0
            if len(data['changes']['new']) > 0:
                t = 0
                for malik in data['changes']['new']:
                    draw.text(495, x, get_display(reshape(u''.join(malik['name']))));
                    draw.text(50, x, str(malik['qty']));
                    #draw.text(85, x, get_display(reshape(u''.join("aaaaa"))));
                    if malik['note']:
                        draw.font_size = 22
                        draw.text(495, x + 30, get_display(reshape(u''.join(malik['note']).replace("\n", "-"))) + " : " + get_display(reshape(u''.join(u"ملاحظة"))));
                        draw.font_size = 28
                        draw.text(500, x + 53, "---------------------------------------------------------------------")
                        x = x + 70
                    else:
                        draw.text(500, x + 20, "---------------------------------------------------------------------")
                        x = x + 45
                ex = 1

            if len(data['changes']['cancelled']) > 0 and ex == 0:
                t2 = 0
                for malik in data['changes']['cancelled']:
                    draw.text(495, x, get_display(reshape(u''.join(malik['name']))));
                    draw.text(50, x, str(malik['qty']));
                    x = x + 30

            draw(img)
            if data['ar_al']:
                if data['pr_ip']:
                    try:
                        p = Network(data['pr_ip'])
                        f = io.BytesIO('img')
                        f.write(base64.decodestring(img.make_blob('png').encode('base64')))
                        p.set("CENTER", "B", "normal", 1, 1, False, False, False)
                        p.image(f)
                        p.cut()
                    except:
                        pass
            return img.make_blob('png').encode('base64')
        except:
            pass
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
class PosConfig(models.Model):
    _inherit = 'pos.config'

    arabic_allow = fields.Boolean("Print Arabic via Network Printer?", default=False)
