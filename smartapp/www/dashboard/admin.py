import frappe
from smartapp.api.dashboard import setup_dashboard_context


def get_context(context):
	setup_dashboard_context(context, "Admin")
	context.page_title = "Dashboard Admin"
