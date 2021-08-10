# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################

{
    "name": "POS Receipt Barcode Print",
    "version": "1.0",
    "summary": """
        Prints product barcode on POS receipt.
    """,
    'description': """
    POS Customer Details
    =============================

    Prints the EAN barcode to the product as a sequence of numbers on POS receipt.

    """,
    "category": "Point Of Sale",
    'license': 'OPL-1',
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "depends": ['point_of_sale'],
    'images': ['static/description/banner.jpg'],
    "data": [
        'views/templates.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/print_ean.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 15,
    'currency': 'EUR'
}
