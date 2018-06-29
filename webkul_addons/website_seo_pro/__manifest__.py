# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Website Sitemap",
  "summary"              :  "Website Sitemap Page of  your Odoo eCommerce !!!",
  "category"             :  "Website",
  "version"              :  "1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-SEO-Suite.html",
  "description"          :  """http://webkul.com/blog/odoo-website-seo-pro/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_seo_pro&version=10.0",
  "depends"              :  ['website'],
  "data"                 :  ['views/template.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  30,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}