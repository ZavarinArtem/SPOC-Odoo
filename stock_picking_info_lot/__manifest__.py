# -*- coding: utf-8 -*-
{
    'name': "Stock Transfers Lot Info",
    'summary': "Add lot information on Stock Transfer lines",
    'description': """
        This feature allows for inventory operations to have additional information about the lot numbers being moved.
        This can be relevant, for example, when the warehouse management is outsourced to a third party provider, that is in charge of managing the actual lot tracking.
        It allows for Odoo store the lot information relayed by the 3PL, for information or reporting purposes. 
        Note that this is different from the case where Odoo is doing the actual lot/serial number tracking, and this feature is expected to be used with Odoo lot tracking disabled.
    """,
    'website': "https://github.com/OCA/stock-logistics-workflow",
    "license": "AGPL-3",
    'category': 'Warehouse',
    'version': '15.0.1.0.0',
    "application": False,
    "installable": True,
    "depends": ["stock"],
    "data": ['views/product_template.xml'],
}
