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
	pass



@frappe.whitelist()
def start_and_end():
    to_date = datetime.now()

    # Remove time part by formatting
    from_date = to_date.strftime("%Y-%m-%d")
    to_date = to_date.strftime("%Y-%m-%d")

    return from_date, to_date



def Convert(result):
    res_dct = {result[i]: result[i + 1] for i in range(0, len(result), 2)}
    return res_dct

@frappe.whitelist()
def trade_india_code():
    print("Call.........Call..........Call..........Call..........Call.......")

    # Check if Trade India integration is enabled
    enabled = frappe.db.get_single_value("TradeIndia Settings", "enabled")
    if enabled == 1:
        # Retrieve TradeIndia Settingss
        website_url = frappe.db.get_single_value("TradeIndia Settings", "tradeindia_url")
        tradeindia_key = frappe.db.get_single_value("TradeIndia Settings", "tradeindia_key")
        user_id = frappe.db.get_single_value("TradeIndia Settings", "user_id")
        profile_id = frappe.db.get_single_value("TradeIndia Settings", "profile_id")

        # Define the date range
        # from_date, to_date = start_and_end()
        from_date = "2024-06-05"
        to_date = "2024-06-05"
        # print(from_date, to_date)

        # Construct the API URL
        creating_url = f"{website_url}?userid={user_id}&profile_id={profile_id}&key={tradeindia_key}&from_date={from_date}&to_date={to_date}"
        print("creating_url \n\n\n\n\n",creating_url)

        headers = {"accept": "application/json"}

        try:
            # Make the API call
            response = requests.get(creating_url, headers=headers)
            # Print status code and response content for debugging
            print(f"Status Code: {response.status_code}")
            print(f"Response Content: {response}")

            # Optionally handle the response data if needed
            if response.status_code == 200:
                data = response.json()
                # Process the data as needed
                print(f"Response JSON: {data}")

                # Filter out already existing sender_ids
                existing_enquiry_entries = frappe.get_list("TradeIndia Enquiry", fields=['name', 'rfi_id'])
                existing_rfi_ids = [entry['rfi_id'] for entry in existing_enquiry_entries]
                rfi_ids = [id_str for id_str in existing_rfi_ids]

                    # Print the result to verify
                print("Ids : \n\n\n\n",rfi_ids)
                new_entries = [entry for entry in data if entry.get("rfi_id") not in rfi_ids]
                if new_entries:
                    print("New enquiry : \n\n\n\n",new_entries)

                    for new_entry in new_entries:
                        try:
                            # print("Try run : \n\n\n\n")

                            # Log the entry being processed
                            generated_date, generated_time = convert_datetime(new_entry.get("generated_date"), new_entry.get("generated_time"))
                            print("generated_date \n\n\n\n\n\n", generated_time,generated_date)

                            clean_message = extract_interest_message(new_entry.get("message"))

                            # Check if the sender's mobile number already exists in the Enquiry doctype
                            existing_enquiry = frappe.get_all("TradeIndia Enquiry", filters={"mobile": new_entry.get("sender_mobile")})
                            if existing_enquiry:
                                # If the sender is a repeat customer, set the status to 'Repeat Customer'
                                status = "Repeat Customer"
                            else:
                                # If the sender is a new customer, set the status to 'Open'
                                status = "Open"

                            inquiry = frappe.get_doc({
                                "doctype": "TradeIndia Enquiry",
                                "sender_id": new_entry.get("sender_uid"),
                                "full_name": new_entry.get("sender_name"),
                                "rfi_id": new_entry.get("rfi_id"),
                                "inquiry_type": new_entry.get("inquiry_type"),
                                "mobile": new_entry.get("sender_mobile"),
                                "mobile_2": new_entry.get("sender_other_mobiles"),
                                "product_id": new_entry.get("product_id"),
                                "product_name": new_entry.get("product_name"),
                                "product_source": new_entry.get("product_source"),
                                "company": new_entry.get("sender_co"),
                                "time": generated_time,
                                "date": generated_date,
                                "city": new_entry.get("sender_city"),
                                "state": new_entry.get("sender_state"),
                                "country": new_entry.get("sender_country"),
                                "message": clean_message,
                                "status": status
                            })

                            inquiry.insert(ignore_permissions=True)
                            frappe.db.commit()
                            print(f"Inquiry {inquiry.name} created successfully.")

                        except Exception as e:
                            print(f"An error occurred while creating an inquiry: {e}")

                else:
                    print("No new entries to add.")

            else:
                print(f"Failed to fetch data. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")    


def convert_datetime(date_str, time_str):
    # Convert date and time to the required format

    generated_date = datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
    generated_time = datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M:%S")


    # generated_date = datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    # generated_time = datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M:%S")
    return generated_date, generated_time


# def extract_interest_message(message):
#     try:
#         # Split the message by newline character
#         lines = message.split("\n")
#         # Look for the line containing the interested message
#         for line in lines:
#             if "interested in" in line:
#                 return line.strip()
#         # Return None if the message is not found
#         return None
#     except Exception as e:
#         print(f"Error extracting interest message: {e}")
#         return None


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

# def create_inquiry_entries(data):
#     for entry in data:
#         try:
#             # Log the entry being processed
#             generated_date, generated_time = convert_datetime(entry.get("generated_date"), entry.get("generated_time"))
#             print(generated_date, generated_time)

#             clean_message = extract_interest_message(entry.get("message"))
            

#              # Check if the sender's mobile number already exists in the Enquiry doctype
#             existing_enquiry = frappe.get_all("TradeIndia Enquiry", filters={"mobile": entry.get("sender_mobile")})
#             if existing_enquiry:
#                 # If the sender is a repeat customer, set the status to 'Repeat Customer'
#                 status = "Repeat Customer"
#             else:
#                 # If the sender is a new customer, set the status to 'New'
#                 status = "Open"          

#             inquiry = frappe.get_doc({
#                 "doctype": "TradeIndia Enquiry",
#                 "sender_id": entry.get("sender_uid"),
#                 "full_name": entry.get("sender_name"),
#                 "rfi_id": entry.get("rfi_id"),
#                 "inquiry_type": entry.get("inquiry_type"),
#                 "mobile": entry.get("sender_mobile"),
#                 "mobile_2": entry.get("sender_other_mobiles"),
#                 "product_id": entry.get("product_id"),
#                 "product_name": entry.get("product_name"),
#                 "product_source": entry.get("product_source"),
#                 "company": entry.get("sender_co"),
#                 "time": generated_time,
#                 "date": generated_date,
#                 "city": entry.get("sender_city"),
#                 "state": entry.get("sender_state"),
#                 "country": entry.get("sender_country"),
#                 "message":entry.get("message"),
#                 "status": status  # Add the status field
#             })

#             inquiry.insert(ignore_permissions=True)
#             frappe.db.commit()
#             print(f"Inquiry {inquiry.name} created successfully.")
        
#         except Exception as e:
#             print(f"An error occurred while creating an inquiry: {e}")



@frappe.whitelist()
def trade_india_api(from_date, to_date):
    print(from_date, to_date)

    # Fetch existing entries to avoid duplicate creation
    existing_enquiry_entries = frappe.get_list("TradeIndia Enquiry", fields=['rfi_id'])
    existing_rfi_ids = [entry['rfi_id'] for entry in existing_enquiry_entries]
    print("Existing Sender IDs: ", existing_rfi_ids)

    enabled = frappe.db.get_single_value("TradeIndia Settings", "enabled")

    # if existing_enquiry_entries:
    #     return "No new API calls made. Existing entries found."
        
    if enabled == 1:
        website_url = frappe.db.get_single_value("TradeIndia Settings", "tradeindia_url")
        tradeindia_key = frappe.db.get_single_value("TradeIndia Settings", "tradeindia_key")
        user_id = frappe.db.get_single_value("TradeIndia Settings", "user_id")
        profile_id = frappe.db.get_single_value("TradeIndia Settings", "profile_id")

        # Convert from_date and to_date to datetime objects
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        # print(from_datetime, to_datetime)

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
                # Print status code and response content for debugging
                # print(f"Status Code: {response.status_code}")
                # print(f"Response Content: {response}")

                # Optionally handle the response data if needed
                if response.status_code == 200:
                    data = response.json()
                    # Process the data as needed
                    # print(f"Response JSON: {data}")

                    # Filter out already existing sender_ids
                    print("existing_rfi_ids----------------> ",existing_rfi_ids)
                    # Convert each string to an integer
                    rfi_ids = [id_str for id_str in existing_rfi_ids]

                    # Print the result to verify
                    print(rfi_ids)
                    new_entries = [entry for entry in data if entry.get("rfi_id") not in rfi_ids]
                    print("New Entries After Filtering:", new_entries)
                    if new_entries:
                        for entry in new_entries:
                            # rfi_id = entry.get("rfi_id")
                            try:
                                generated_date, generated_time = convert_datetime(entry.get("generated_date"), entry.get("generated_time"))
                                print(generated_date, generated_time)

                                clean_message = extract_interest_message(entry.get("message"))

                                # Check if the sender's mobile number already exists in the Enquiry doctype
                                existing_enquiry = frappe.get_all("TradeIndia Enquiry", filters={"mobile": entry.get("sender_mobile")})
                                if existing_enquiry:
                                    status = "Repeat Customer"
                                else:
                                    status = "Open"

                                inquiry = frappe.get_doc({
                                    "doctype": "TradeIndia Enquiry",
                                    "sender_id": entry.get("sender_uid"),
                                    "full_name": entry.get("sender_name"),
                                    "rfi_id": entry.get("rfi_id"),
                                    "inquiry_type": entry.get("inquiry_type"),
                                    "mobile": entry.get("sender_mobile"),
                                    "mobile_2": entry.get("sender_other_mobiles"),
                                    "product_id": entry.get("product_id"),
                                    "product_name": entry.get("product_name"),
                                    "product_source": entry.get("product_source"),
                                    "company": entry.get("sender_co"),
                                    "time": generated_time,
                                    "date": generated_date,
                                    "city": entry.get("sender_city"),
                                    "state": entry.get("sender_state"),
                                    "country": entry.get("sender_country"),
                                    "message": clean_message,
                                    "status": status
                                })

                                inquiry.insert(ignore_permissions=True)
                                frappe.db.commit()
                                print(f"Inquiry {inquiry.name} created successfully.")
                            
                            except Exception as e:
                                print(f"An error occurred while creating an inquiry: {e}")

                    else:
                        print("No new entries to add.")

                else:
                    print(f"Failed to fetch data. Status Code: {response.status_code}")

                # Append response text to the list
                response_texts.append(response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

            # Move to the next 24-hour period
            from_datetime = next_day_datetime

        return response_texts
    
    else: 
        return "Trade India integration is not enabled."




# inddiamart to Lead Creations
@frappe.whitelist()
def trade_india_to_lead(
    user,
    name,
    full_name,
    mobile,
    # email,
    # phone,
    mobile_2,
    # phone_2,
    product_name,
    city,
    state,
    message,
    company,
    # product_category,
):
    data1 = frappe.db.sql(
        "select name,status from `tabLead` where mobile_no=%s", mobile, as_dict=True
    )
    # dt = ""
    # for i1 in data1:
    #     for j1 in i1:
    #         dt = j1
    #         print(dt)

    if len(data1) == 0:
        data = frappe.new_doc("Lead")
        data.first_name = full_name
        #  data.lead_name = full_name
        data.mobile_no = mobile
        # data.email_id = email
        data.company_name = company
        # data.phone = phone
        data.whatsapp_no = mobile_2
        # data.phone_ext = phone_2
        data.state_name = state
        data.city = city
        data.lead_owner = user
        # data.product_group = product_category
        data.source = "TradeIndia"
        data.save()
        frappe.db.commit()

        doc12 = frappe.get_doc("Lead", data.name)
        doc12.append(
            "follow_up",
            {
                "date": datetime.today(),
                "product": product_name,
                # "product_category": product_category,
                "remark": message,
                "user": user,
                "follow_up_status": "Direct",
            },
        )
        doc12.save()
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

    else:
        if data1[0]["status"] != "Do Not Contact":
            doc = frappe.get_doc("Lead", data1[0]["name"])
            doclen = frappe.db.sql(
                "select idx from `tabFollow Up Details` where parent=%s",
                data1[0]["name"],
            )
            doc1 = []
            for i in doclen:
                for j in i:
                    doc1.append(j)
            len1 = len(doc1)

            print(doc1)
            print(len1)

            new_row = doc.append("follow_up", {})
            new_row.update(
                {
                    "date": datetime.today(),
                    "product": product_name,
                    # "product_category": product_category,
                    "remark": message,
                    "user": user,
                    "idx": 0,
                    "follow_up_status": "Direct",
                }
            )
            doc.save()

            frappe.db.commit()
            frappe.db.set_value(
                "TradeIndia Enquiry",
                name,
                {
                    "lead": data1[0]["name"],
                    "status": "Approach",
                    "lead_status": "Updated",
                    "owner1": user,
                },
            )