# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Binotel Module",
    "summary": "Binotel Integration",
    "version": "15.0.1.0.0",
    "development_status": "Alpha",
    "category": "IP Telephony",
    "website": "https://spoc-odoo.com.ua/",
    "author": "SPOC",
    "maintainers": ["SPOC corp"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "helpdesk_mgmt",
        "spoc_hd_addons",
    ],
    "data": [
        'data/binotel_calls.xml',
        'security/binotel_calls.xml',
        'security/ir.model.access.csv',
        'views/binotel_calls_menu.xml',
        'views/binotel_calls_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "demo": [
    ],
}
