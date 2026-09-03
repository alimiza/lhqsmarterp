import frappe
from smartapp.api.dashboard import setup_dashboard_context


def get_context(context):
	setup_dashboard_context(context, "Sarpras")
	context.page_title = "Dashboard Sarpras"
