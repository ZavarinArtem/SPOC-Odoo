{
    'name': "Invoice Report for Account Move",
    'summary': """Some fancy invoice form""",
    'version': "15.0.1.0.1",
    'category': 'Accounting/Accounting',
    'website': "https://spoc.com.ua",
    'author': "Spoc, Artem Zavarin",
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'depends': [
        'account',
    ],
    'data': [
        'views/account_report.xml',
    ],
}
