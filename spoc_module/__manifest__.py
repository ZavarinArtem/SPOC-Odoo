{
    "name": "S.P.O.C. module",
    "summary": """
        Some utility features""",
    "description": """
        Add-ons for better compatibility with 1C
    """,
    "author": "S.P.O.C.",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "14.0.1.0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "product",
        "account",
    ],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/account_report.xml"
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
