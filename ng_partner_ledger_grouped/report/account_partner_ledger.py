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
from report import report_sxw
from account.report import account_partner_ledger
from ng_partner_reports.report import partner_ledger_report

from tools.translate import _
#probuse inherited from partner_ledger_report
class ng_party_ledger(partner_ledger_report.ng_party_ledger):
    def __init__(self, cr, uid, name, context=None):
        super(ng_party_ledger, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'lines': self.lines,
        })

    def set_context(self, objects, data, ids, report_type=None):
        res =  super(ng_party_ledger, self).set_context(objects, data, ids, report_type)
        self.is_group = data['form'].get('is_grouped', False)
        return res

    def lines(self, partner):
        #if self.is_group is false then super call
        if not self.is_group:
            return super(ng_party_ledger, self).lines(partner)
        #if self.is_group is true then execute below
        move_state = ['draft','posted']
        if self.target_move == 'posted':
            move_state = ['posted']

        full_account = []
        if self.reconcil:
            RECONCILE_TAG = " "
        else:
            RECONCILE_TAG = "AND l.reconcile_id IS NULL"
        self.cr.execute(
            "SELECT l.id, l.date, j.code, acc.code as a_code, acc.name as a_name, l.ref, m.name as move_name, l.name, l.debit, l.credit, l.amount_currency,l.currency_id, c.symbol AS currency_code " \
            "FROM account_move_line l " \
            "LEFT JOIN account_journal j " \
                "ON (l.journal_id = j.id) " \
            "LEFT JOIN account_account acc " \
                "ON (l.account_id = acc.id) " \
            "LEFT JOIN res_currency c ON (l.currency_id=c.id)" \
            "LEFT JOIN account_move m ON (m.id=l.move_id)" \
            "WHERE l.partner_id = %s " \
                "AND l.account_id IN %s AND " + self.query +" " \
                "AND m.state IN %s " \
                " " + RECONCILE_TAG + " "\
                "ORDER BY l.date",
                (partner.id, tuple(self.account_ids), tuple(move_state)))
        res = self.cr.dictfetchall()
        #if is_grouped is true the same reference number record is merged in single ledger line in report
        res_ref= []#probuse
        res_ref_dict = {}#probuse
        res_final = []#probuse
        for l in res:#probuse
            if l['move_name'] not in res_ref_dict:#probuse
                res_ref_dict[l['move_name']] = l#probuse
            else:#probuse
                #if found the duplicate ref number record it merge the creadit, debit, ref 
                credit = l['credit'] + res_ref_dict[l['move_name']]['credit']#probuse
                debit = l['debit'] + res_ref_dict[l['move_name']]['debit']#probuse
                amount_currency = l['amount_currency'] + res_ref_dict[l['move_name']]['amount_currency']#probuse
                ref = l['name'] + res_ref_dict[l['move_name']]['name']#probuse
                res_ref_dict[l['move_name']].update({'name':ref, 'debit': debit, 'credit':credit, 'amount_currency':amount_currency})#probuse
        #create then final dictionary with replace of duplicate records with merged record
        for r in res_ref_dict:#probuse
            res_final.append(res_ref_dict[r])#probuse
        res = res_final#probuse
        
        sum = 0.0
        if self.initial_balance:
            sum = self.init_bal_sum
        for r in res:
            sum += r['debit'] - r['credit']
            r['progress'] = sum
            full_account.append(r)
        return full_account
    
report_sxw.report_sxw('report.account.third_party_ledger_grouped', 'res.partner',
        'addons/ng_partner_reports/report/account_partner_ledger.rml',parser=ng_party_ledger,
        header='internal')#probuse

report_sxw.report_sxw('report.account.third_party_ledger_other_grouped', 'res.partner',
        'addons/ng_partner_reports/report/account_partner_ledger_other.rml',parser=ng_party_ledger,
        header='internal')#probuse

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
