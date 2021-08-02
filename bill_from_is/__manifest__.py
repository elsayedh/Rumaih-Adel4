# -*- coding: utf-8 -*-

{
    # App information
   
    'name': 'Create Vendor Bill From Incoming Shipment',
    'version': '1.0',
    'category': 'website',
    'license': 'OPL-1',
    'summary': """Create Vendor Bill From Picking""",
    
    # Dependencies
   
    'depends': ['purchase_stock'],
   
    # Views
   
    'data' : [
        'view/res_config_setting.xml',
        'view/views.xml',
        'view/account_payment_po.xml',
        # 'data/uom_data.xml',
    ],
    
    # Odoo Store Specific
    
    'images': ['static/description/bill_from_in_ship.png'],      
    
    # Author

    'author': 'Craftsync Technologies',
    'website': 'https://www.craftsync.com',
    'maintainer': 'Craftsync Technologies',
       
       
    # Technical 
    
    'installable': True,
    'currency': 'USD',
    'price': 14.99,
    'auto_install': False,
    'application': True,
          
}
