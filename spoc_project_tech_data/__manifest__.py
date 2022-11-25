{
    "name": "Technical data for project tasks",
    "summary": "Adds technical data to project task and stage views",
    "description": """
        Adds technical data (date of creation and uid) to Task views.
        Adds project list in project Stage form view. 
    """,
    "author": "SPOC",
    "website": "https://spoc-odoo.com.ua/",
    "company": "SPOC corp",
    "maintainer": "SPOC corp",
    "license": "LGPL-3",
    "version": "15.0.1.0.1",
    "category": "Hidden",
    "application": False,
    "installable": True,
    "depends": [
        "project",
    ],
    "data": [
        "views/project_views.xml",
    ],
}
