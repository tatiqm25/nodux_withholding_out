# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cint, flt
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.controllers.stock_controller import update_gl_entries_after
from frappe.model.mapper import get_mapped_doc
from erpnext.accounts.doctype.sales_invoice.pos import update_multi_mode_option

from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.utils import get_account_currency
from erpnext.stock.doctype.delivery_note.delivery_note import update_billed_amount_based_on_so
from erpnext.projects.doctype.timesheet.timesheet import get_projectwise_timesheet_data
from erpnext.accounts.doctype.asset.depreciation \
	import get_disposal_account_and_cost_center, get_gl_entries_on_asset_disposal

@frappe.whitelist()
def make_withholding_out(source_name, target_doc=None):
	def postprocess(source, target):
		set_missing_values(source, target)

	def update_item(obj, target, source_parent):
		target.customer = obj.customer
		target.customer_name = obj.customer
		target.base_imponible = obj.net_total
		target.total_taxes = obj.base_total_taxes_and_charges
		target.nro_invoice = obj.naming_series
		target.retencion = 0

	doc = get_mapped_doc("Sales Invoice", source_name,	{
		"Sales Invoice": {
			"doctype": "Withholding",
			"validation": {
				"docstatus": ["=", 1],
			},
			"postprocess": update_item
		}
	}, target_doc, postprocess)

	return doc

def set_missing_values(source, target):
	target.efectivo = 1
