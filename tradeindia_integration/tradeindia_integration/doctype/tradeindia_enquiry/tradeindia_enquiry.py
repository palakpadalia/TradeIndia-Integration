# Copyright (c) 2024, Sanskar Technolab and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.utils.data import now_datetime
import requests
from datetime import datetime, timedelta
from frappe.utils import now
from frappe.model.document import Document


class TradeIndiaEnquiry(Document):
    def validate(self):
        self.repeat_enquiry()

    def repeat_enquiry(self):
        if self.is_new():
            # Check if the Sender`s` mobile number or Email - ID already exists in the Enquiry doctype
            Existing_Enquiries = frappe.get_all(
                "TradeIndia Enquiry",
                or_filters=[{"mobile_no": self.mobile_no}],
            )
            if Existing_Enquiries:
                self.status = "Repeat Customer"
            else:
                self.status = "Open"

        


# Returns From and To Date in YYYY-MM-DD format
@frappe.whitelist()
def start_and_end():
    to_date = datetime.now()

    # Remove time part by formatting
    from_date = to_date.strftime("%Y-%m-%d")
    to_date = to_date.strftime("%Y-%m-%d")

    return from_date, to_date


# Convert date and time as per my format
def convert_datetime(date_str, time_str):

    generated_date = datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
    generated_time = datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M:%S")

    return generated_date, generated_time


# Extracting Interest Message
def extract_interest_message(message):
    try:
        # Lowercase the message to make it case-insensitive
        lower_message = message.lower()
        # Find the start of the "sender details" section
        start_index = lower_message.find("sender details")
        if start_index == -1:
            # Find the start of the "details of the sender" section
            start_index = lower_message.find("details of the sender")

        if start_index != -1:
            # Remove everything from the start of the sender details section to the end of the message
            message = message[:start_index].strip()
            # print("message--",message)
            message

        return message
    except Exception as e:
        print(f"Error removing sender details: {e}")
        return message


@frappe.whitelist()
def tradeindia_code():
    enabled = frappe.db.get_single_value("TradeIndia Settings", "enabled")
    if enabled == 0:
        # Retrieve TradeIndia Settings
        website_url = frappe.db.get_single_value(
            "TradeIndia Settings", "tradeindia_url"
        )
        tradeindia_key = frappe.db.get_single_value(
            "TradeIndia Settings", "tradeindia_key"
        )
        user_id = frappe.db.get_single_value("TradeIndia Settings", "user_id")
        profile_id = frappe.db.get_single_value("TradeIndia Settings", "profile_id")

        # Define the date range
        from_date, to_date = start_and_end()

        # Construct the API URL
        creating_url = (
            f"{website_url}?userid={user_id}&profile_id={profile_id}&key={tradeindia_key}"
            f"&from_date={from_date}&to_date={to_date}"
        )
        headers = {"accept": "application/json"}
        try:
            response = requests.get(creating_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # Filter out already existing sender_ids
                Existing_Enquiry_Entries = frappe.get_list(
                    "TradeIndia Enquiry", fields=["name", "rfi_id"]
                )
                Existing_RFI_Ids = [
                    entry["rfi_id"] for entry in Existing_Enquiry_Entries
                ]
                RFI_Ids = [id_str for id_str in Existing_RFI_Ids]
                New_Entries = [
                    entry for entry in data if entry.get("rfi_id") not in RFI_Ids
                ]
                if New_Entries:
                    for new_entry in New_Entries:
                        try:
                            generated_date, generated_time = convert_datetime(
                                new_entry.get("generated_date"),
                                new_entry.get("generated_time"),
                            )
                            clean_message = extract_interest_message(
                                new_entry.get("message")
                            )
                            # Check if the sender's mobile number already exists in the Enquiry doctype
                            Existing_Enquiries = frappe.get_all(
                                "TradeIndia Enquiry",
                                filters={"mobile_no": new_entry.get("sender_mobile")},
                            )
                            if Existing_Enquiries:
                                # If the sender is a repeat customer, set the status to 'Repeat Customer'
                                status = "Repeat Customer"
                            else:
                                # If the sender is a new customer, set the status to 'Open'
                                status = "Open"
                            Enquiry = frappe.get_doc(
                                {
                                    "doctype": "TradeIndia Enquiry",
                                    "sender_id": new_entry.get("sender_uid"),
                                    "full_name": new_entry.get("sender_name"),
                                    "email_id": new_entry.get("sender_email"),
                                    "rfi_id": new_entry.get("rfi_id"),
                                    "enquiry_type": new_entry.get("inquiry_type"),
                                    "mobile_no": new_entry.get("sender_mobile"),
                                    "phone_no": new_entry.get("sender_other_mobiles"),
                                    "product_id": new_entry.get("product_id"),
                                    "product_name": new_entry.get("product_name"),
                                    "product_source": new_entry.get("product_source"),
                                    "company": new_entry.get("sender_co"),
                                    "enquiry_time": generated_time,
                                    "enquiry_date": generated_date,
                                    "city": new_entry.get("sender_city"),
                                    "sender_state": new_entry.get("sender_state"),
                                    "country": new_entry.get("sender_country"),
                                    "message": clean_message,
                                    "status": status,
                                }
                            )
                            Enquiry.insert(ignore_permissions=True)
                            frappe.db.commit()
                        except Exception as e:
                            print(f"An error occurred while creating an Enquiry: {e}")
                else:
                    pass
            else:
                print(f"Failed to fetch data. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


@frappe.whitelist()
def tradeindia_api(from_date, to_date):
    
    # Fetch existing entries to avoid duplicate creation
    Existing_Enquiry_Entries = frappe.get_list("TradeIndia Enquiry", fields=["rfi_id"])
    Existing_RFI_Ids = [entry["rfi_id"] for entry in Existing_Enquiry_Entries]

    enabled = frappe.db.get_single_value("TradeIndia Settings", "enabled")

    if enabled == 1:
        website_url = frappe.db.get_single_value(
            "TradeIndia Settings", "tradeindia_url"
        )
        tradeindia_key = frappe.db.get_single_value(
            "TradeIndia Settings", "tradeindia_key"
        )
        user_id = frappe.db.get_single_value("TradeIndia Settings", "user_id")
        profile_id = frappe.db.get_single_value("TradeIndia Settings", "profile_id")

        # Convert from_date and to_date to datetime objects
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")

        # Initialize a list to store response texts from each API call
        response_texts = []

        # Loop through 24-hour periods until the end date is reached
        while from_datetime <= to_datetime:
            # Adjust the to_datetime to be within 24 hours of from_datetime
            next_day_datetime = from_datetime + timedelta(days=1)

            # Format dates as required for the API call
            from_date_str = from_datetime.strftime("%Y-%m-%d")
            to_date_str = next_day_datetime.strftime("%Y-%m-%d")
            creating_url = f"{website_url}?userid={user_id}&profile_id={profile_id}&key={tradeindia_key}&from_date={from_date_str}&to_date={to_date_str}"

            headers = {
                "accept": "application/json",
            }

            try:
                response = requests.get(creating_url, headers=headers)

                # Optionally handle the response data if needed
                if response.status_code == 200:
                    data = response.json()

                    # Convert each string to an integer
                    rfi_ids = [id_str for id_str in Existing_RFI_Ids]
                    new_entries = [
                        entry for entry in data if entry.get("rfi_id") not in rfi_ids
                    ]

                    if new_entries:
                        for entry in new_entries:
                            try:
                                generated_date, generated_time = convert_datetime(
                                    entry.get("generated_date"),
                                    entry.get("generated_time"),
                                )

                                clean_message = extract_interest_message(
                                    entry.get("message")
                                )

                                # Check if the sender's mobile number already exists in the Enquiry doctype
                                existing_enquiry = frappe.get_all(
                                    "TradeIndia Enquiry",
                                    filters={"mobile_no": entry.get("sender_mobile")},
                                )
                                if existing_enquiry:
                                    status = "Repeat Customer"
                                else:
                                    status = "Open"

                                Enquiry = frappe.get_doc(
                                    {
                                        "doctype": "TradeIndia Enquiry",
                                        "sender_id": entry.get("sender_uid"),
                                        "full_name": entry.get("sender_name"),
                                        "rfi_id": entry.get("rfi_id"),
                                        "email_id": entry.get("sender_email"),
                                        "enquiry_type": entry.get("inquiry_type"),
                                        "mobile_no": entry.get("sender_mobile"),
                                        "phone_no": entry.get("sender_other_mobiles"),
                                        "product_id": entry.get("product_id"),
                                        "product_name": entry.get("product_name"),
                                        "product_source": entry.get("product_source"),
                                        "company": entry.get("sender_co"),
                                        "enquiry_time": generated_time,
                                        "enquiry_date": generated_date,
                                        "city": entry.get("sender_city"),
                                        "state": entry.get("sender_state"),
                                        "country": entry.get("sender_country"),
                                        "message": clean_message,
                                        "status": status,
                                    }
                                )

                                Enquiry.insert(ignore_permissions=True)
                                frappe.db.commit()

                            except Exception as e:
                                print(
                                    f"An error occurred while creating an Enquiry: {e}"
                                )

                    else:
                        pass

                else:
                    print(f"Failed to fetch data. Status Code: {response.status_code}")

                # Append response text to the list
                response_texts.append(response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            from_datetime = next_day_datetime

        return response_texts

    else:
        return "Trade India integration is not enabled."


# Indiamart Enquiries to Lead Creation
@frappe.whitelist()
def tradeindia_to_lead(
    creation,
    user,
    name,
    mobile_no,
    email_id,
    phone_no,
    product_name,
    city,
    state,
    remarks,
    enquiry_type,
    enquiry_date,
    enquiry_id,
    company="",
    full_name="",
):
    lead_data = frappe.db.sql(
        "SELECT name, status FROM `tabLead` WHERE mobile_no = %s OR email_id = %s",
        (mobile_no, email_id),
        as_dict=True
    )

    if len(lead_data) == 0:
        data = frappe.new_doc("Lead")
        data.first_name = full_name
        data.mobile_no = mobile_no
        data.email_id = email_id
        data.company_name = company
        data.phone = phone_no
        data.state = state
        data.city = city
        data.lead_owner = user
        data.source = "TradeIndia"
        data.save()
        frappe.db.commit()

        lead_record = frappe.get_doc("Lead", data.name)
        lead_record.append(
            "follow_up",
            {
                "date": datetime.today(),
                "remark": remarks,
                "follow_up_date": enquiry_date,
                "user": user,
                "follow_up_status": "Direct",
                "query_type": enquiry_type,
            },
        )
        lead_record.save()
        frappe.db.commit()

        frappe.db.set_value(
            "TradeIndia Enquiry",
            name,
            {
                "lead": data.name,
                "status": "Approach",
                "lead_status": "Created",
                "owner1": user,
            },
        )
        frappe.db.commit()
        other_enquiries = frappe.get_list(
                "TradeIndia Enquiry",
                filters={"mobile_no": mobile_no, "name": ("!=", name)},
                fields=["*"],
            )
        for enquiry in other_enquiries:
                frappe.db.set_value(
                    "TradeIndia Enquiry",
                    enquiry.name,
                    "lead",
                    data.name,
            )
        frappe.db.set_value("TradeIndia Enquiry", enquiry.name, "lead", data.name)

        associated_lead = frappe.get_doc("Lead", data.name)

        associated_lead.append(
                "follow_up",
                {
                    # "product_name": enquiry.product_name,
                    # "product_category": enquiry.product_category,
                    "remark": enquiry.remarks,
                    "date": datetime.today(),
                    "user": frappe.session.user,
                },
            )

        associated_lead.save()
    

    else:
        if lead_data[0]["status"] != "Do Not Contact":
            doc = frappe.get_doc("Lead", lead_data[0]["name"])
            TradeIndia_Product_Record = frappe.db.sql(
                "select idx from `tabFollow Up Details` where parent=%s",
                lead_data[0]["name"],
            )
            TradeIndia_Product_Records = []
            for i in TradeIndia_Product_Record:
                for j in i:
                    TradeIndia_Product_Records.append(j)

            add_row = doc.append("follow_up", {})
            add_row.update(
                {
                    "date": datetime.today(),
                    "remark": remarks,
                    "user": user,
                    "idx": 0,
                    "follow_up_status": "Direct",
                    "query_type": enquiry_type,
                    "follow_up_date": enquiry_date,
                }
            )


            doc.save()

            frappe.db.commit()
            frappe.db.set_value(
                "TradeIndia Enquiry",
                name,
                {
                    "lead": lead_data[0]["name"],
                    "status": "Approach",
                    "lead_status": "Updated",
                    "owner1": user,
                },
            )


@frappe.whitelist()
def scheduled_tradeindia_api():
    from_date = datetime.today().strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    tradeindia_api(from_date, to_date)