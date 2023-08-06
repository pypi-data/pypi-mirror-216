# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author:Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#    Modify by Team Devcontrol
#
#############################################################################
from datetime import datetime
import pytz
import json
import datetime
import io
from odoo import fields, models, _
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class StockReport(models.TransientModel):
    _name = "wizard.deposito.history"
    _description = "Desposito actual"

    warehouse = fields.Many2many('stock.warehouse', 'war_wiz_rel', 'wardep', 'wiz', string='Warehouse', required=True)
    owner = fields.Many2many('res.partner', 'own_wiz_rel', 'owndep', 'wiz', string='Owner', domain="[('is_author','=',False)]")

    def export_resumen_xls(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'warehouse': self.warehouse.ids,
        }

        return {
            'type': 'ir_actions_xlsx_download_deposito',
            'data': {'model': 'wizard.deposito.history',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Deposito_general',
                     'resumen': True,
                     }
        }

    def export_xls(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'warehouse': self.warehouse.ids,
            'owner': self.owner.ids,
        }
        obj = self.env['res.partner'].browse(self.owner.ids[0])
        return {
            'type': 'ir_actions_xlsx_download_deposito',
            'data': {'model': 'wizard.deposito.history',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': f'Deposito_de_{obj.name}',
                     'resumen': False,
                     }
        }

    def get_warehouse(self, data):
        wh = data.warehouse.mapped('id')
        obj = self.env['stock.warehouse'].search([('id', 'in', wh)])
        l1 = []
        l2 = []
        for j in obj:
            l1.append(j.name)
            l2.append(j.id)
        return l1, l2
    
    def get_owner(self, data):
        ow = data.owner.mapped('id')
        obj = self.env['res.partner'].search([('id', 'in', ow)])
        l1 = []
        l2 = []
        for j in obj:
            l1.append(j.name)
            l2.append(j.id)
        return l1, l2

    def get_lines(self, partner_id):

        domain = [
            ('owner_id', '=', partner_id),
            ('location_id', '=' , 17), # This is the id of the Location DS/Depósitos (the source of the move)
            ('location_dest_id', '=' , 5), # This is the id of the Location Partner Locations/Customers (the destination of the move)
            ('state', 'in', ('assigned', 'partially_available')),
        ]
        pendientes_liquidar_line_ids = self.env['stock.move.line'].search(domain)
        deposito_lines = {}
        for move_line in pendientes_liquidar_line_ids:
            key = move_line.product_id.id
            if key not in deposito_lines:
                deposito_lines[key] = {
                    'deposito': move_line.product_uom_qty - move_line.qty_done,
                }
            else:
                deposito_lines[key].update({
                    'deposito': deposito_lines[key].get('deposito') + move_line.product_uom_qty - move_line.qty_done,
                })

        lines = []
        # falataria filtrar las línas por la categoría (en caso de que nos interese)
        # añadir aquí los campos isbn, name, category, deposito

        for key_prod_id, value_deposito in deposito_lines.items():
            product = self.env['product.product'].browse(key_prod_id)
            vals = {
                'isbn': product.isbn_number,
                'name': product.name,
                'category': product.categ_id.name,
                'cost_price': product.list_price,
                'deposito': value_deposito.get('deposito'),
            }
            lines.append(vals)
        return lines

    def get_fecha_ultima_liq(self, partner_id):
        domain = [
            ('partner_id', '=', partner_id),
            ('is_liquidacion', '=' , True),
            ('state', '=', 'posted'),
        ]
        ultima_liq = self.env['account.move'].search(domain, order='invoice_date desc', limit=1)
        return ultima_liq.invoice_date if ultima_liq.invoice_date else 'Sin fecha conocida'

    def get_xlsx_resumen_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        lines = self.browse(data['ids'])
        get_warehouse = self.get_warehouse(lines)
        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet(f'Resumen depósitos')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        sheet.merge_range('A1:G2', 'Informe resumen de depósitos', format0)
        sheet.merge_range('A3:G3', comp, format11)
        w_house = ', '
        sheet.write(4, 0, 'Warehouses : ', format4)
        w_house = w_house.join(get_warehouse[0])
        sheet.write('B5', w_house, format4)
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz if user.tz else 'UTC')
        times = pytz.utc.localize(datetime.datetime.now()).astimezone(tz)
        sheet.merge_range('A7:D7', 'Fecha de informe: ' + str(times.strftime("%Y-%m-%d %H:%M %p")), format1)
        sheet.merge_range('A9:G9', 'Información de clientes', format11)
        sheet.write(9, 0, 'Nombre', format21)
        sheet.write(9, 1, 'Valor en depósito (€)', format21)
        sheet.write(9, 2, 'Fecha uĺtima liquidación de depósito', format21)

        prod_row = 10
        prod_col = 0
        sheet.set_column('A:A', 60)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 30)

        clientes = self.env['res.partner'].search([])
        for cliente in clientes:
            fecha_liq = self.get_fecha_ultima_liq(cliente.id)
            get_line = self.get_lines(cliente.id)
            valor_deposito = sum(x['deposito'] * x['cost_price'] for x in get_line)
            client_full_name = (f"({cliente.comercial}) " if cliente.comercial else '') + f"{cliente.name}"
            sheet.write(prod_row, prod_col, client_full_name, font_size_8)
            sheet.write(prod_row, prod_col + 1, valor_deposito, font_size_8_l)
            sheet.write(prod_row, prod_col + 2, str(fecha_liq), font_size_8)
            prod_row = prod_row + 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        lines = self.browse(data['ids'])
        # get_warehouse = self.get_warehouse(lines)
        get_owner = self.get_owner(lines)
        comp = self.env.user.company_id.name
        fecha_liq = self.get_fecha_ultima_liq(get_owner[1][0])
        sheet = workbook.add_worksheet(f'{get_owner[0][0][:31]}')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        sheet.merge_range('A1:G2', 'Informe de stock', format0)
        sheet.merge_range('A3:G3', comp, format11)
        w_house = ', '
        sheet.write(4, 0, 'Depósito : ', format4)
        w_house = w_house.join(get_owner[0])
        sheet.write('B5', w_house, format4)
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz if user.tz else 'UTC')
        times = pytz.utc.localize(datetime.datetime.now()).astimezone(tz)
        sheet.merge_range('A7:D7', 'Fecha de informe: ' + str(times.strftime("%Y-%m-%d %H:%M %p")), format1)
        sheet.merge_range('F7:K7', f'Fecha última liq.: {fecha_liq}', format1)
        sheet.merge_range('A9:G9', 'Información de producto', format11)   
        sheet.write(9, 0, 'ISBN', format21)
        sheet.write(9, 1, 'Nombre', format21)
        sheet.write(9, 2, 'Categoria', format21)
        sheet.write(9, 3, 'Precio PVP', format21)
        p_col_no1 = 4
        for i in get_owner[0]:
            sheet.write(9, p_col_no1, 'Deposito', format21)

        prod_row = 10
        prod_col = 0
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 50)
        sheet.set_column('D:D', 10)
        for i in get_owner[1]:
            get_line = self.get_lines(i)
            for each in get_line:
                sheet.write(prod_row, prod_col, each['isbn'], font_size_8)
                sheet.write(prod_row, prod_col + 1, each['name'], font_size_8_l)
                sheet.write(prod_row, prod_col + 2, each['category'], font_size_8)
                sheet.write(prod_row, prod_col + 3, each['cost_price'], font_size_8_r)
                prod_row = prod_row + 1
            break
        prod_row = 10
        prod_col = 4
        for i in get_owner[1]:
            get_line = self.get_lines(i)
            for each in get_line:
                if each['deposito'] < 0:
                    sheet.write(prod_row, prod_col, each['deposito'], red_mark)
                else:
                    sheet.write(prod_row, prod_col, each['deposito'], font_size_8)
                prod_row = prod_row + 1
            prod_row = 10
            prod_col = prod_col + 4
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
