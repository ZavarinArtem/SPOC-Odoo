# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product: name wider in the tree view",
    "summary": "Makes products' name field wider",
    "version": "14.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "category": "Uncategorized",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "views/product.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_name_wider_in_tree_view/static/src/css/product_name_wider_class.css",
        ],
    },
}
