import frappe
from frappe import _


ALL_DASHBOARDS = [
	{"name": "Founder", "route": "/dashboard/founder", "label": "Dashboard Founder"},
	{"name": "Admin", "route": "/dashboard/admin", "label": "Dashboard Admin"},
	{"name": "Akademik", "route": "/dashboard/akademik", "label": "Dashboard Akademik"},
	{"name": "Guru", "route": "/dashboard/guru", "label": "Dashboard Guru"},
	{"name": "Wali Santri", "route": "/dashboard/wali-santri", "label": "Dashboard Wali Santri"},
	{"name": "Sarpras", "route": "/dashboard/sarpras", "label": "Dashboard Sarpras"},
]


@frappe.whitelist()
def get_user_dashboards(user=None):
	"""Return allowed dashboards and default dashboard for the user (default: current session user)."""
	user = user or frappe.session.user
	if not user or user == "Guest":
		return {
			"logged_in": False,
			"user": "Guest",
			"full_name": "Guest",
			"dashboards": [],
			"default_dashboard": None,
		}

	user_roles = set(frappe.get_roles(user))
	full_name = frappe.utils.get_fullname(user)

	# Founder and Administrator have full access to all dashboards
	if "SmartApp Founder" in user_roles or "Administrator" in user_roles or "System Manager" in user_roles:
		default_name = "Founder" if "SmartApp Founder" in user_roles else "Admin"
		default_dash = next((d for d in ALL_DASHBOARDS if d["name"] == default_name), ALL_DASHBOARDS[0])
		return {
			"logged_in": True,
			"user": user,
			"full_name": full_name,
			"roles": list(user_roles),
			"dashboards": ALL_DASHBOARDS,
			"default_dashboard": default_dash,
		}

	allowed_names, default_name = _get_configured_dashboards(user_roles)
	allowed_dashboards = [d for d in ALL_DASHBOARDS if d["name"] in allowed_names]

	default_dash = None
	if default_name:
		default_dash = next((d for d in allowed_dashboards if d["name"] == default_name), None)
	if not default_dash and allowed_dashboards:
		default_dash = allowed_dashboards[0]

	return {
		"logged_in": True,
		"user": user,
		"full_name": full_name,
		"roles": list(user_roles),
		"dashboards": allowed_dashboards,
		"default_dashboard": default_dash,
	}


@frappe.whitelist()
def check_access(dashboard_name, user=None):
	"""Check if user is authorized to access a specific dashboard."""
	user_data = get_user_dashboards(user=user)
	if not user_data.get("logged_in"):
		return {
			"allowed": False,
			"reason": "not_logged_in",
			"redirect": "/",
		}

	allowed_names = [d["name"] for d in user_data.get("dashboards", [])]
	if dashboard_name in allowed_names:
		return {"allowed": True}

	default_dash = user_data.get("default_dashboard")
	redirect_route = default_dash["route"] if default_dash else "/"
	return {
		"allowed": False,
		"reason": "forbidden",
		"message": _("Anda tidak memiliki akses ke halaman tersebut"),
		"redirect": redirect_route,
	}


def setup_dashboard_context(context, dashboard_name):
	"""Set standard context and enforce access guard for portal dashboard pages."""
	context.no_cache = 1
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/"
		raise frappe.Redirect

	access = check_access(dashboard_name)
	if not access.get("allowed"):
		target = access.get("redirect", "/")
		redirect_to = f"{target}&denied=1" if "?" in target else f"{target}?denied=1"
		frappe.local.flags.redirect_location = redirect_to
		raise frappe.Redirect

	context.title = f"Dashboard {dashboard_name} - SmartApp"
	context.current_dashboard = dashboard_name
	context.user_data = get_user_dashboards()


def _get_configured_dashboards(user_roles):
	"""Resolve allowed and default dashboard from SmartApp Dashboard Setting."""
	try:
		setting = frappe.get_doc("SmartApp Dashboard Setting")
	except Exception:
		return set(), None

	allowed = set()
	default_dashboard = None

	for rule in getattr(setting, "access_rules", []):
		if rule.role in user_roles:
			# 1. Parse comma-separated allowed_dashboards
			dash_raw = getattr(rule, "allowed_dashboards", "") or ""
			if isinstance(dash_raw, str):
				for d in [x.strip() for x in dash_raw.split(",") if x.strip()]:
					allowed.add(d)
			elif isinstance(dash_raw, list):
				for item in dash_raw:
					dash = getattr(item, "dashboard", None) or item
					if dash:
						allowed.add(str(dash).strip())

			# 2. Always allow the default dashboard
			if getattr(rule, "default_dashboard", None):
				default_dash_val = str(rule.default_dashboard).strip()
				allowed.add(default_dash_val)
				if not default_dashboard:
					default_dashboard = default_dash_val

	return allowed, default_dashboard
