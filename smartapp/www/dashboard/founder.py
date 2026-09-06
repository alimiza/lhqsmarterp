import frappe
from smartapp.api.dashboard import setup_dashboard_context, get_founder_financial_kpi


def get_context(context):
	setup_dashboard_context(context, "Founder")
	context.page_title = "Dashboard Founder"

	companies = []
	try:
		companies = frappe.get_all(
			"Company",
			fields=["name", "company_name", "default_currency", "country"],
			order_by="name asc"
		)
	except Exception:
		pass

	context.companies = companies

	requested_company = frappe.form_dict.get("company")
	selected_company = None

	if requested_company:
		for c in companies:
			if c.name == requested_company or c.company_name == requested_company:
				selected_company = c.name
				break
		if not selected_company:
			selected_company = requested_company

	if not selected_company:
		user_default = frappe.defaults.get_user_default("Company")
		if user_default and any(c.name == user_default for c in companies):
			selected_company = user_default
		elif companies:
			selected_company = companies[0].name
		else:
			selected_company = "Little Hafidz Qur'an (Demo)"

	context.target_company = selected_company
	try:
		context.initial_financial_kpi = get_founder_financial_kpi(context.target_company)
	except Exception:
		context.initial_financial_kpi = None


