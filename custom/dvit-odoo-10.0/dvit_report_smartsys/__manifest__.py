{
    'name': 'DVIT SMARTSYS Report ',
    'summary': 'SMARTSYS Report',
    'version': '10.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': "DVIT.ME",
    'website': 'http://dvit.me/',
    'depends': [
        'product_pack',
        'partner_contact_department',
        'dvit_sale_discount',
        'sales_report_product_image',
        'dvit_sale_hide_price',
        'dvit_sale_duplicate_lines',
       'dvit_sale_line_no',
       'sale_comment_template',
        ],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
