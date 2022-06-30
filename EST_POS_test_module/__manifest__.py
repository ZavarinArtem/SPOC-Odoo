# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "EST-POS test module",
    "summary": "Test CRM-based module",
    "version": "14.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://spoc.com.ua/",
    "author": "Zavarin Artem, S.P.O.C.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_lead_views.xml",
    ],
}
