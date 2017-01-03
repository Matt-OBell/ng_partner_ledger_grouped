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

from osv import osv, fields
from tools.translate import _

class account_partner_ledger_report(osv.osv_memory):#probuse
    _inherit = 'account.partner.ledger.report'#probuse inherited from ng_partner_report
    
    _columns = {
        'is_grouped' : fields.boolean('Is Grouped?')#probuse
    }
    
    _defaults = {
        'is_grouped': True#probuse
    }
    #inherited from ng_partner_report
    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        #probuse added 'is_grouped' field in data
        data['form'].update(self.read(cr, uid, ids, ['is_grouped','initial_balance', 'filter', 'page_split', 'amount_currency', 'journal_ids','partner_ids','for_all','account_ids','for_all_acc'])[0])
        if data['form']['page_split']:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.third_party_ledger_grouped',#probuse changed the report name
                'datas': data,
        }
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.third_party_ledger_other_grouped',#probuse changed the report name
                'datas': data,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
