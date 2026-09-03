import frappe


def get_context(context):
	context.no_cache = 1
	context.title = "SmartApp — Sistem Manajemen Lembaga Pendidikan"

	# Detect if user is already logged in
	context.is_logged_in = frappe.session.user != "Guest"
	context.user_fullname = ""
	context.default_dashboard_route = "/"

	if context.is_logged_in:
		try:
			from smartapp.api.dashboard import get_user_dashboards
			user_data = get_user_dashboards()
			default_dash = user_data.get("default_dashboard")
			if default_dash:
				context.default_dashboard_route = default_dash.get("route", "/")
			context.user_fullname = user_data.get("full_name", frappe.session.user)
		except Exception:
			pass
