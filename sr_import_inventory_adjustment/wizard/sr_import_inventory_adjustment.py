# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import tempfile
import binascii
import xlrd
import base64
import io
import csv


class ImportInventoryAdjustment(models.TransientModel):
    _name = 'import.inventory.adjustment'
    _description = 'Import Inventory Adjustment'

    import_file = fields.Binary('File')
    import_file_by = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select File', default='csv')
    import_product_option = fields.Selection([('name', 'Name'), ('code', 'Code'), ('barcode', 'Barcode')], string='Import Product By', default='name')
    location_id = fields.Many2one('stock.location', string='Select Inventory Location', required=True, domain="[('usage', 'in', ['internal', 'transit'])]")
    inventory_name = fields.Char(string='Inventory Adjustment Name', required=True)
    
    def import_inventory_adjustment(self):
        inventory_val = []
        try:
            if self.import_file_by == 'xls':
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.import_file))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
                for row_no in range(sheet.nrows):
                    val = {}
                    if row_no <= 0:
                        fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
                    else:
                        line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                        values.update({
                                        'product_name':line[0],
                                        'qty': line[1],
                                        })
                        inventory_val.append(values)
            else:
                keys = ['product_name', 'qty']
                try:
                    csv_data = base64.b64decode(self.import_file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    data_file.seek(0)
                    file_reader = []
                    values = {}
                    csv_reader = csv.reader(data_file, delimiter=',')
                    file_reader.extend(csv_reader)
                except:
                    raise UserError(_("Invalid file!"))
                for i in range(len(file_reader)):
                    field = list(map(str, file_reader[i]))
                    values = dict(zip(keys, field))
                    if values:
                        if i == 0:
                            continue
                        else:
                            inventory_val.append(values)
            product_ids = []
            for record in inventory_val:
                p_id = self._find_product(record.get('product_name'))
                product_ids.append(p_id.id)
            inventory = self.env['stock.inventory'].create({
            'name':self.inventory_name,
            'location_ids':[(6,0,[self.location_id.id])],
            'product_ids':[(6,0,product_ids)]
            })
            inventory.action_start()
            for record in inventory_val:
                self.create_inventory_adjustment(record, inventory)
            inventory.action_validate()
        except Exception as e:
            raise UserError(_(e))


    def _find_product(self,product):
        if self.import_product_option == 'name':
            product_id = self.env['product.product'].search([('name','=',product)])
            if not product_id:
                raise UserError(_('Product name "%s" is not available in system' %product))
            return product_id
        elif self.import_product_option == 'code':
            product_id = self.env['product.product'].search([('default_code','=',product)])
            if not product_id:
                raise UserError(_('Product code "%s" is not available in system' %product))
            return product_id
        else:
            product_id = self.env['product.product'].search([('barcode','=',product)])
            if not product_id:
                raise UserError(_('Product barcode "%s" is not available in system' %product))
            return product_id
        


    def create_inventory_adjustment(self, value, inventory):
        product_id = self._find_product(value.get('product_name'))
        inventory_lines = self.env['stock.inventory.line']
        test = inventory_lines.create({
            'product_id':product_id.id , 
            'location_id' : self.location_id.id,
            'product_uom_id' : product_id.uom_id.id  ,
            'product_qty': value.get('qty'),
            'inventory_id':inventory.id
            })
    
