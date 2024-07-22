// Copyright (c) 2024, Sanskar Technolab and contributors
// For license information, please see license.txt

// frappe.ui.form.on("TradeIndia Enquiry", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("TradeIndia Enquiry", {
	refresh: function (frm) {
		if (frm.doc.status == "Approach") {
			frm.dashboard.add_comment(
				"Lead is " + frm.doc.lead_status + "  (" + frm.doc.lead + ")",
				"green"
			);
		}
		if (frm.doc.status == "Open" || frm.doc.status == "Not Connected") {
			frm.add_custom_button(__("Create Lead"), function () {
				frappe.confirm(
					"Are you sure want to create lead?",
					function () {
						var creation_date = frm.doc.creation;
						var user = frappe.session.user;
						var full_name = frm.doc.full_name;
						var mobile_no = frm.doc.mobile_no;

						var email_id = frm.doc.email_id;
						var phone_no = frm.doc.phone_no;

						var company = frm.doc.company;
						var product_name = frm.doc.product_name;
						var enquiry_type = frm.doc.enquiry_type;
						var city = frm.doc.city;
						var state = frm.doc.sender_state;
						var country = frm.doc.country;
						var remarks = frm.doc.remarks;
						var name = frm.doc.name;
						var enquiry_date = frm.doc.enquiry_date;
						var enquiry_id = frm.doc.name;

						if (email_id == null) {
							var email_id = "";
						} else {
							email_id = email_id;
						}
						if (phone_no == null) {
							var phone_no = "";
						} else {
							phone_no = phone_no;
						}

						if (product_name == null) {
							var product_name1 = "";
						} else {
							product_name1 = product_name;
						}

						if (enquiry_type == null) {
							var enquiry_type1 = "";
						} else {
							enquiry_type1 = enquiry_type;
						}

						if (enquiry_date == null) {
							var enquiry_Date = "";
						} else {
							enquiry_Date = enquiry_date;
						}

						if (enquiry_id == null) {
							var enquiry_id = "";
						} else {
							enquiry_id = enquiry_id;
						}

						if (city == null) {
							var city1 = "";
						} else {
							city1 = city;
						}
						if (state == null) {
							var state1 = "";
						} else {
							state1 = state;
						}
						if (country == null) {
							var country1 = "";
						} else {
							country1 = country;
						}
						if (remarks == null) {
							var remarks = "";
						} else {
							remarks = remarks;
						}
						if (company == null) {
							var company1 = "";
						} else {
							company1 = company;
						}
						frm.set_value("owner1", frappe.session.user);
						frappe
							.call({
								method:
									"tradeindia_integration.tradeindia_integration.doctype.tradeindia_enquiry.tradeindia_enquiry.tradeindia_to_lead",
								args: {
									name: name,
									full_name: full_name,
									mobile_no: mobile_no,
									email_id: email_id,
									phone_no: phone_no,
									user: user,
									product_name: product_name1,
									city: city1,
									state: state1,
									country: country1,
									remarks: remarks,
									company: company1,
									enquiry_type: enquiry_type1,
									enquiry_date: enquiry_Date,
									enquiry_id: enquiry_id,
									creation: creation_date,
								},
							})
							.then((records) => {
								frm.reload_doc();
							});
					},
				);
			});
			frm.add_custom_button(__("Set as Lost"), function () {
				frappe.confirm(
					"Are you sure want to set as Lost this Enquiry",
					function () {
						frm.set_value("status", "Lost");
						frm.set_value("owner1", frappe.session.user);
						frm.set_value("lost_verification", "Not Approved");
						frm.set_df_property('remarks', 'reqd', 1)
						frm.save();
					}
				);
			});
		}
		if (frm.doc.status == "Open") {
			frm.add_custom_button(__("Set as Not Connected"), function () {
				frappe.confirm(
					"Are you sure want to set as Not Connected",
					function () {
						frm.set_value("status", "Not Connected");
						frm.set_value("owner1", frappe.session.user);
						frm.save();
					}
				);
			});
		}

		if (frappe.user.has_role("System Manager") && frm.doc.status === "Lost") {
			frm.add_custom_button(__("Reopen"), function () {
				frappe.confirm("Are you sure want to set as reopen", function () {
					frm.set_value("status", "Open");
					frm.set_value("owner1", frappe.session.user);
				});
			});
		}
	},

	onload: function (frm) {
		// Check if any lost enquiries with same mobile number
		const Lost_enquiry = (frm, callback) => {
			if (frm.doc.status == "Repeat Customer") {
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "TradeIndia Enquiry",
						filters: {
							mobile_no: frm.doc.mobile_no,
							status: "Lost",
							name: ["!=", frm.doc.name]
						},
						fields: ["name"]
					},
					callback: function (r) {
						if (r.message && r.message.length > 0) {
							callback(true);
						} else {
							callback(false);
						}
					}
				});

			}
			else {
				callback(false);
				return;
			}
		};
		Lost_enquiry(frm, function (has_lost_enquiry) {
			if (frm.doc.status == "Open" || frm.doc.status == "Not Connected" || has_lost_enquiry == true) {
				frm.add_custom_button(__("Create Lead"), function () {
					frappe.confirm(
						"Are you sure want to create lead?",
						function () {
							var creation_date = frm.doc.creation;
							var user = frappe.session.user;
							var full_name = frm.doc.full_name;
							var mobile_no = frm.doc.mobile_no;

							var email_id = frm.doc.email_id;
							var phone_no = frm.doc.phone_no;

							var company = frm.doc.company;
							var product_name = frm.doc.product_name;
							var enquiry_type = frm.doc.enquiry_type;
							var city = frm.doc.city;
							var state = frm.doc.sender_state;
							var country = frm.doc.country;
							var remarks = frm.doc.remarks;
							var name = frm.doc.name;
							var enquiry_date = frm.doc.enquiry_date;
							var enquiry_id = frm.doc.name;

							if (email_id == null) {
								var email_id = "";
							} else {
								email_id = email_id;
							}
							if (phone_no == null) {
								var phone_no = "";
							} else {
								phone_no = phone_no;
							}

							if (product_name == null) {
								var product_name1 = "";
							} else {
								product_name1 = product_name;
							}

							if (enquiry_type == null) {
								var enquiry_type1 = "";
							} else {
								enquiry_type1 = enquiry_type;
							}

							if (enquiry_date == null) {
								var enquiry_Date = "";
							} else {
								enquiry_Date = enquiry_date;
							}

							if (enquiry_id == null) {
								var enquiry_id = "";
							} else {
								enquiry_id = enquiry_id;
							}

							if (city == null) {
								var city1 = "";
							} else {
								city1 = city;
							}
							if (state == null) {
								var state1 = "";
							} else {
								state1 = state;
							}
							if (country == null) {
								var country1 = "";
							} else {
								country1 = country;
							}
							if (remarks == null) {
								var remarks = "";
							} else {
								remarks = remarks;
							}
							if (company == null) {
								var company1 = "";
							} else {
								company1 = company;
							}
							frm.set_value("owner1", frappe.session.user);
							frappe
								.call({
									method:
										"tradeindia_integration.tradeindia_integration.doctype.tradeindia_enquiry.tradeindia_enquiry.tradeindia_to_lead",
									args: {
										name: name,
										full_name: full_name,
										mobile_no: mobile_no,
										email_id: email_id,
										phone_no: phone_no,
										user: user,
										product_name: product_name1,
										city: city1,
										state: state1,
										country: country1,
										remarks: remarks,
										company: company1,
										enquiry_type: enquiry_type1,
										enquiry_date: enquiry_Date,
										enquiry_id: enquiry_id,
										creation: creation_date,
									},
								})
								.then((records) => {
									frm.reload_doc();
								});
						},
					);
				});
				frm.add_custom_button(__("Set as Lost"), function () {
					frappe.confirm(
						"Are you sure want to set as Lost this Enquiry",
						function () {
							frm.set_value("status", "Lost");
							frm.set_value("owner1", frappe.session.user);
							frm.set_value("lost_verification", "Not Approved");
							frm.set_df_property('remarks', 'reqd', 1)
							frm.save();
						}
					);
				});
			}
		})
		Lost_enquiry(frm, function (has_lost_enquiry) {
			if (frm.doc.status == "Open" || has_lost_enquiry) {
				frm.add_custom_button(__("Set as Not Connected"), function () {
					frappe.confirm(
						"Are you sure want to set as Not Connected",
						function () {
							frm.set_value("status", "Not Connected");
							frm.set_value("owner1", frappe.session.user);
							frm.save();
						}
					);
				});

			}
		})
	},

	status: function (frm) {
		if (frappe.user.has_role("System Manager") === true) {
			if (frm.doc.status == "Lost") {
				frm.set_value("lost_verification", "Approved");
				frm.set_value("user", frappe.session.user);
				frm.set_value("owner1", frappe.session.user);
			}
			if (frm.doc.status == "Approach") {
				frm.set_value("owner1", frappe.session.user);
			}
		}
	},
});