# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Mattobell (<http://www.mattobell.com>)
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#

{
    'name' : 'Grouped Partner Ledger Report ',
    'version': '1.0',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'description':'''These module adds the Is Grouped Check box in partner ledger report.
                    if Check box is true it merge the same ref number records in single line in
                    partner ledger report''',
    'data':[
            'wizard/ng_partner_ledger_view.xml'
            ],
    'depends':[
               'account',
               'ng_partner_reports'
            ],
    'installable':True,
    'auto_install':False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
