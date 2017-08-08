// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.ui.form.on('Withholding', {
	refresh: function(frm) {
		if (frm.doc.status == 'Draft') {
			frm.add_custom_button(__("Confirm"), function() {
				frm.events.update_to_confirm_withholding(frm);
			}).addClass("btn-primary");
		}
	},

	update_to_confirm_withholding: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_to_confirm_withholding",
			freeze: true,
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		})
	}
});

frappe.ui.form.on('Withholding Tax', {
	base: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.base) {
			args = {
				'base'			: d.base,
				'tax'			: d.tax
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "get_values",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("taxes");
						cur_frm.refresh_fields();
						calculate_retencion(frm);
					}
				}
			});
		}
		cur_frm.refresh_fields();
	},

	tax: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.tax) {
			args = {
				'base'			: d.base,
				'tax'			: d.tax
			};
			return frappe.call({
				doc: cur_frm.doc,
				method: "get_values",
				args: args,
				callback: function(r) {
					if(r.message) {
						var d = locals[cdt][cdn];
						$.each(r.message, function(k, v) {
							d[k] = v;
						});
						refresh_field("taxes");
						cur_frm.refresh_fields();
						calculate_retencion(frm);
					}
				}
			});
		}
		cur_frm.refresh_fields();
	}
})

var calculate_retencion = function(frm) {
	var doc = frm.doc;
	doc.retencion = 0;

	if(doc.taxes) {
		$.each(doc.taxes, function(index, data){
			doc.retencion += (data.valor);
		})
	}
	refresh_field('retencion')
}
