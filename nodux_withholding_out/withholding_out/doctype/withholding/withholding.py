# -*- coding: utf-8 -*-
# Copyright (c) 2015, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate

class Withholding(Document):
	def before_save(self):
		self.docstatus = 1

	def update_to_confirm_withholding(self):
		if self.efectivo == 1:
			default_account = frappe.db.get_value("Company", {"company_name": self.company}, "default_cash_account")
			lined = frappe.get_doc({
				"doctype": "Journal Entry Account",
				"account": default_account,
				"debit_in_account_currency":0,
				"credit_in_account_currency":self.retencion,
			})
		else:
			default_account = frappe.db.get_value("Company", {"company_name": self.company}, "default_receivable_account")
			lined = frappe.get_doc({
				"doctype": "Journal Entry Account",
				"account": default_account,
				"debit_in_account_currency":0,
				"credit_in_account_currency":self.retencion,
				"party_type": "Customer",
				"party": self.customer,
			})

		journal = frappe.get_doc({
			"doctype":"Journal Entry",
			"voucher_type": "Journal Entry",
			"posting_date": nowdate(),
		})

		lined = frappe.get_doc({
			"doctype": "Journal Entry Account",
			"account": default_account,
			"debit_in_account_currency":0,
			"credit_in_account_currency":self.retencion,
			"party_type": "Customer",
			"party": self.customer,
		})
		for tax in self.taxes:
			linec = frappe.get_doc({
				"doctype": "Journal Entry Account",
				"account": tax.account,
				"debit_in_account_currency":tax.value,
				"credit_in_account_currency":0,
			})
			journal.append('accounts', linec)

		journal.append('accounts', lined)

		journal.save()
		journal.docstatus = 1
		journal.save()
		self.status = "Confirmed"
		self.save()

	def get_values(self, args=None, serial_no=None):
		tax_name = args.get('tax').split('-')
		tax_name = tax_name[0]
		tax_name = tax_name.strip()
		tax = frappe.db.sql("""select tax_rate from `tabAccount`
			where account_name = %s""",
			(tax_name), as_dict = 1)

		if not tax:
			frappe.throw(_("No existe impuesto {0}").format(args.get("tax")))

		tax = tax[0]
		if args.get('base'):
			ret = {
				'valor'	: args.get('base') * ((tax.tax_rate)/100)
			}
		else:
			ret = {
				'valor'	: 0
			}
		return ret
