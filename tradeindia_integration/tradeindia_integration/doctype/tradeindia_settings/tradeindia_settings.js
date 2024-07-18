// Copyright (c) 2024, Sanskar Technolab and contributors
// For license information, please see license.txt

// frappe.ui.form.on("TradeIndia Settings", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('TradeIndia Settings', {
	sync_enquiries: function (frm) {

		if (!frm.doc.from_date || !frm.doc.to_date) {
			frappe.throw(__("From And To Date Mandatory"))
		}
		if (frm.doc.from_date && frm.doc.to_date) {
			frappe.call({
				method: "tradeindia_integration.tradeindia_integration.doctype.tradeindia_enquiry.tradeindia_enquiry.tradeindia_api",
				args: { "from_date": frm.doc.from_date, "to_date": frm.doc.to_date },
				freeze:true,
				freeze_message:"Syncing Enquiries . . .",
				callback: function (r) {
					if (r) {
						frappe.show_alert({
							message: __("Enquiries synced successfully"),
							indicator: "green",
						});
					}
				}
			})
		}
	},
});