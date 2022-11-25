{
    "name": "Account Invoice Report",
    "summary": """
        Multilanguage Invoice Report for Account Move""",
    "description": """
        Adds two-language (eng & ukr) Invoice report for account Move document.
        Also adds required for printing fields in Partners and Banks  
    """,
    "author": "SPOC",
    "website": "https://spoc-odoo.com.ua/",
    "company": "SPOC corp",
    "maintainer": "SPOC corp",
    "license": "LGPL-3",
    "category": "Uncategorized",
    "version": "15.0.1.0.1",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "product",
        "account",
    ],
    # always loaded
    "data": ["views/views.xml", "reports/account_report.xml"],
}
