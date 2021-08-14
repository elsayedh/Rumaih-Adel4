# -*- coding: utf-8 -*-
{
    'name': 'Account Statement Report',
    'version': '13.0',
    'category': 'Accounting',
    'description': """
This module contain Account Statement Report in pdf and xls format.
====================================================================================
    """,
    'author': 'Kanak Infosystems LLP.',
    'website': 'http://www.kanakinfosystems.com',
    'depends': ['account'],
    'data': [
        'report/report_qweb.xml',
        'report/report_view.xml',
        'wizard/account_statement_wizard.xml',
    ],
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'application': False,
    'price': 30,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': 'https://youtu.be/xgnuTSCuj4c',
}
