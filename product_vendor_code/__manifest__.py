{
    "name": "Vendor code",
    "summary": """
        Vendor's code for product template""",
    "description": """
        Vendor's code for product template
    """,
    "author": "S.P.O.C.",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "14.0.1.0.1",
    # any module necessary for this one to work correctly
    "depends": ["product"],
    # always loaded
    "data": [
        "views/views.xml",
    ],
}
