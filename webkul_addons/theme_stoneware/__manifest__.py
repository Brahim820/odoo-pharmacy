{
    'name': 'Theme Stoneware',
    'category': 'Theme/Ecommerce',
    'summary': "Theme Stoneware is a Odoo theme with advanced ecommerce feature, extremely customizable and fully responsive. It's suitable for any e-commerce sites. Start your Odoo store right away with The Stoneware theme",
    'version': '10.2.1.0',
    'author': 'Atharva System',
	'website': 'https://www.atharvasystem.com',
	'support': 'support@atharvasystem.com',
    'description': """
Theme Stoneware
===================
Theme Stoneware is  is a Odoo theme with advanced ecommerce feature, extremely customizable and fully responsive. It's suitable for any e-commerce sites. Start your Odoo store right away with The Stoneware theme.
        """,
    'depends': ['website_sale','website_mass_mailing','website_crm','website_blog','website_event'],
    'data': [  
        'views/website_setting.xml',
		'views/product_brand_view.xml',                                                         
        'views/product_category_view.xml',
        'views/templates.xml',
        'views/assets.xml',
        'views/snippets.xml',  
        'views/customize_template.xml',  
		'views/website_menu_view.xml',
		'views/mega_menu_template.xml', 
		'views/product_slider_templates.xml',
		'security/ir.model.access.csv',
        'views/product_brand_template.xml',
        'views/breadcum_template.xml',
        'views/multi_tab_configure_view.xml',
        'views/snippet_multitab_slider.xml',
		'views/website_blog_config.xml',
		'views/snippet_blog_template.xml',
        'views/wishlist_view.xml',
		'views/product_brand_page.xml',
    ],
    'live_test_url': 'http://theme-stoneware.atharvasystem.com',    
    'images': [
		'static/description/stoneware_desc.png',
		'static/description/stoneware_screenshot.png'
	],
    'price': 175.00,
    'currency': 'EUR',
    'installable': True,
}
