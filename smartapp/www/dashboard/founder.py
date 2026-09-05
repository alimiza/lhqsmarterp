import frappe
from smartapp.api.dashboard import setup_dashboard_context, get_founder_financial_kpi


def get_context(context):
	setup_dashboard_context(context, "Founder")
	context.page_title = "Dashboard Founder"
	context.target_company = "Little Hafidz Qur'an (Demo)"
	try:
		context.initial_financial_kpi = get_founder_financial_kpi(context.target_company)
	except Exception:
		context.initial_financial_kpi = None

