# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Binotel Module",
    "summary": "Binotel Integration",
    "description": """
        Integration with Binotel IP-Tel. Loads calls and tech info. Creates Helpdesk Tickets.  
    """,
    "version": "15.0.1.0.0",
    "development_status": "Alpha",
    "category": "IP Telephony",
    "author": "SPOC",
    "website": "https://spoc-odoo.com.ua/",
    "company": "SPOC corp",
    "maintainer": "SPOC corp",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "helpdesk_mgmt",
        "spoc_hd_addons",
        "phone_validation",
    ],
    "data": [
        "data/binotel_calls.xml",
        "security/binotel_calls.xml",
        "security/ir.model.access.csv",
        "views/binotel_calls_menu.xml",
        "views/binotel_calls_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/binotel_calls_manual_load_wizard_views.xml",
    ],
}
