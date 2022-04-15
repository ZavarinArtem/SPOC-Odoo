# -*- coding: utf-8 -*-
{
    'name': "Stock Transfers Lot Info",

    'summary': """
        Add lot information on Stock Transfer lines""",

    'description': """
        This feature allows for inventory operations to have additional information about the lot numbers being moved.
        This can be relevant, for example, when the warehouse management is outsourced to a third party provider, that is in charge of managing the actual lot tracking.
        It allows for Odoo store the lot information relayed by the 3PL, for information or reporting purposes. 
        Note that this is different from the case where Odoo is doing the actual lot/serial number tracking, and this feature is expected to be used with Odoo lot tracking disabled.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
