import frappe

ROLES = [
	"SmartApp Founder",
	"SmartApp Admin",
	"SmartApp Academic Head",
	"SmartApp Teacher",
	"SmartApp Parent",
	"SmartApp Facility Manager",
]

DASHBOARD_TYPES = [
	{"name": "Founder", "route": "/dashboard/founder"},
	{"name": "Admin", "route": "/dashboard/admin"},
	{"name": "Akademik", "route": "/dashboard/akademik"},
	{"name": "Guru", "route": "/dashboard/guru"},
	{"name": "Wali Santri", "route": "/dashboard/wali-santri"},
	{"name": "Sarpras", "route": "/dashboard/sarpras"},
]

DEFAULT_MAPPINGS = [
	{
		"role": "SmartApp Founder",
		"dashboards": ["Founder", "Admin", "Akademik", "Guru", "Sarpras"],
		"default": "Founder",
	},
	{
		"role": "SmartApp Academic Head",
		"dashboards": ["Akademik", "Guru"],
		"default": "Akademik",
	},
	{
		"role": "SmartApp Teacher",
		"dashboards": ["Guru"],
		"default": "Guru",
	},
	{
		"role": "SmartApp Parent",
		"dashboards": ["Wali Santri"],
		"default": "Wali Santri",
	},
	{
		"role": "SmartApp Facility Manager",
		"dashboards": ["Sarpras"],
		"default": "Sarpras",
	},
	{
			"role": "SmartApp Admin",
			"dashboards": ["Admin"],
			"default": "Admin",
	},
]


def setup_roles_and_dashboards():
	"""Ensure standard roles, dashboard types, and default access rules exist."""
	create_roles()
	create_dashboard_types()
	seed_dashboard_settings()


def create_roles():
	for role_name in ROLES:
		if not frappe.db.exists("Role", role_name):
			role_doc = frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
				"is_custom": 0,
			})
			role_doc.insert(ignore_permissions=True)
	frappe.db.commit()


def create_dashboard_types():
	for dt in DASHBOARD_TYPES:
		if not frappe.db.exists("SmartApp Dashboard Type", dt["name"]):
			doc = frappe.get_doc({
				"doctype": "SmartApp Dashboard Type",
				"name": dt["name"],
				"dashboard_name": dt["name"],
				"route": dt["route"],
			})
			doc.insert(ignore_permissions=True)
		else:
			doc = frappe.get_doc("SmartApp Dashboard Type", dt["name"])
			doc.route = dt["route"]
			doc.save(ignore_permissions=True)
	frappe.db.commit()


def seed_dashboard_settings():
	setting = frappe.get_single("SmartApp Dashboard Setting")
	setting.set("access_rules", [])
	for mapping in DEFAULT_MAPPINGS:
		setting.append("access_rules", {
			"role": mapping["role"],
			"allowed_dashboards": ", ".join(mapping["dashboards"]),
			"default_dashboard": mapping["default"],
		})
	setting.flags.ignore_permissions = True
	setting.save()
	frappe.db.commit()


def create_test_users():
	"""Helper to create sample users for manual testing in browser."""
	test_users = [
		("founder@smartapp.test", "SmartApp Founder", "Founder Demo"),
		("admin@smartapp.test", "SmartApp Admin", "Admin Demo"),
		("akademik@smartapp.test", "SmartApp Academic Head", "Akademik Demo"),
		("guru@smartapp.test", "SmartApp Teacher", "Guru Demo"),
		("wali@smartapp.test", "SmartApp Parent", "Wali Santri Demo"),
		("sarpras@smartapp.test", "SmartApp Facility Manager", "Sarpras Demo"),
		("guru_wali@smartapp.test", "SmartApp Teacher", "Guru dan Wali"),
	]

	for email, role, full_name in test_users:
		if not frappe.db.exists("User", email):
			user = frappe.get_doc({
				"doctype": "User",
				"email": email,
				"first_name": full_name,
				"send_welcome_email": 0,
				"new_password": "Password@123",
			})
			user.insert(ignore_permissions=True)
			user.add_roles(role)
			if email == "guru_wali@smartapp.test":
				user.add_roles("SmartApp Parent")
	frappe.db.commit()
