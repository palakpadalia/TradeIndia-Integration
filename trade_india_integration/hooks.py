from . import __version__ as app_version

app_name = "trade_india_integration"
app_title = "Trade India Integration"
app_publisher = "Sanskar Technolab"
app_description = "Trade India Integration"
app_email = "palak@sanskartechnolab.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/trade_india_integration/css/trade_india_integration.css"
# app_include_js = "/assets/trade_india_integration/js/trade_india_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/trade_india_integration/css/trade_india_integration.css"
# web_include_js = "/assets/trade_india_integration/js/trade_india_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "trade_india_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "trade_india_integration.utils.jinja_methods",
# 	"filters": "trade_india_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "trade_india_integration.install.before_install"
# after_install = "trade_india_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "trade_india_integration.uninstall.before_uninstall"
# after_uninstall = "trade_india_integration.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "trade_india_integration.utils.before_app_install"
# after_app_install = "trade_india_integration.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "trade_india_integration.utils.before_app_uninstall"
# after_app_uninstall = "trade_india_integration.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "trade_india_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"trade_india_integration.tasks.all"
# 	],
# 	"daily": [
# 		"trade_india_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"trade_india_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"trade_india_integration.tasks.weekly"
# 	],
# 	"monthly": [
# 		"trade_india_integration.tasks.monthly"
# 	],
# }

scheduler_events = {
    # "cron": {
    #     "* * * * *": [
    #  		"trade_india_integration.api.trade_india_code"
    #  	]
    # },
    "trade_india_code": {
        "*/5 * * * *": [
            "trade_india_integration.trade_india_integration.doctype.tradeindia_enquiry.tradeindia_enquiry.trade_india_code"
        ]
    },
}

# Testing
# -------

# before_tests = "trade_india_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "trade_india_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "trade_india_integration.task.get_dashboard_data"hc
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["trade_india_integration.utils.before_request"]
# after_request = ["trade_india_integration.utils.after_request"]

# Job Events
# ----------
# before_job = ["trade_india_integration.utils.before_job"]
# after_job = ["trade_india_integration.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"trade_india_integration.auth.validate"
# ]
