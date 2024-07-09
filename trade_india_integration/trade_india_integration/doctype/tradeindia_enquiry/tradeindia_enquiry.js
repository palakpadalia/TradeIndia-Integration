// Copyright (c) 2024, Sanskar Technolab and contributors
// For license information, please see license.txt

frappe.ui.form.on("TradeIndia Enquiry", {
	refresh: function (frm) {
		if (frm.doc.status == "Approach") {

			frm.dashboard.add_comment("Lead is " + frm.doc.lead_status + "  (" + frm.doc.lead + ")", "green");
		}
		if (frm.doc.status == "Open" || frm.doc.status == "Not Connected") {
			frm.add_custom_button(__('Create Lead'), function () {
				frappe.confirm(
					'Are you sure want to create lead?',
					function () {
						var user = frappe.session.user;
						var full_name = frm.doc.full_name;
						var mobile = frm.doc.mobile;
						// var phone = frm.doc.phone;
						// var email = frm.doc.email;
						var mobile_2 = frm.doc.mobile_2;
						// var phone_2 = frm.doc.phone_2;
						// var product_category = frm.doc.product_category;
						var company = frm.doc.company;
						var product_name = frm.doc.product_name
						var city = frm.doc.city;
						var state = frm.doc.state;
						var country = frm.doc.country;
						var message = frm.doc.message;
						var name = frm.doc.name;
						// alert(name)
						// if (phone == null) { var phone1 = "" } else { phone1 = phone }
						// if (email == null) { var email1 = "" } else { email1 = email }
						if (mobile_2 == null) { var mobile2 = "" } else { mobile2 = mobile_2 }
						// if (email_2==null){ email2="" } else{email2=email_2}
						// if (phone_2 == null) { var phone2 = "" } else { phone2 = phone_2 }
						if (product_name == null) { var product_name1 = "" } else { product_name1 = product_name }
						// if (product_category == null) { var product_category1 = "" } else { var product_category1 = product_category }
						if (city == null) { var city1 = "" } else { city1 = city }
						if (state == null) { var state1 = "" } else { state1 = state }
						if (country == null) { var country1 = "" } else { country1 = country }
						if (message == null) { var message1 = "" } else { message1 = message }
						if (company == null) { var company1 = "" } else { company1 = company }
						frm.set_value("owner1", frappe.session.user)
						frappe.call({
							method: "trade_india_integration.trade_india_integration.doctype.tradeindia_enquiry.tradeindia_enquiry.trade_india_to_lead",
							args: {
								"name": name,
								"full_name": full_name,
								"mobile": mobile,
								// "email": email1,
								// "phone": phone1,
								"mobile_2": mobile2,
								"user": user,
								// "phone_2": phone2,
								"product_name": product_name1,
								"city": city1,
								"state": state1,
								"country": country1,
								"message": message1,
								"company": company1,
								// "product_category": product_category1
							}
						}).then(records => {

							frm.reload_doc()

						})
					},
					function () {

					}
				)
			})
			frm.add_custom_button(__('Set as Lost'), function () {
				frappe.confirm(
					'Are you sure want to set as Lost this Enquiry',
					function () {
						frm.set_value("status", "Lost")
						frm.set_value("owner1", frappe.session.user)
						frm.set_value("lost_verification", "Not Approved")
						// frm.set_value("user","")
					})
			})
		}
		if (frm.doc.status == "Open") {
			frm.add_custom_button(__('Set as Not Connected'), function () {
				frappe.confirm(
					'Are you sure want to set as Not Connected',
					function () {
						frm.set_value("status", "Not Connected")
						frm.set_value("owner1", frappe.session.user)
						// frm.set_value("lost_verification","Not Approved")
						// frm.set_value("user","")
					})
			})

		}

		if (frappe.user.has_role("System Manager") && frm.doc.status === "Lost") {
			frm.add_custom_button(__('Reopen'), function () {
				frappe.confirm(
					'Are you sure want to set as reopen',
					function () {
						frm.set_value("status", "Open");
						frm.set_value("owner1", frappe.session.user);
					});
			});
		}

	},
	



	status: function (frm) {
		
		if (frappe.user.has_role("System Manager") === true) {
			if (frm.doc.status == "Lost") {
				frm.set_value("lost_verification", "Approved")
				frm.set_value("user", frappe.session.user)
				frm.set_value("owner1", frappe.session.user)
			}
			if (frm.doc.status == "Approach") {
				frm.set_value("owner1", frappe.session.user)
			}
		}
	}
});
