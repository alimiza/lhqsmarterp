"""
Unit tests for SmartApp Dashboard Authentication & Access Control.
Run with: bench --site smarterp.localhost run-tests --module smartapp.tests.test_dashboard_auth
"""

import frappe
import unittest
from smartapp.api.dashboard import check_access, get_user_dashboards


class TestDashboardAuth(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		"""Create test users for each role scenario."""
		frappe.set_user("Administrator")
		cls._create_test_user("founder_test@smartapp.test", "SmartApp Founder")
		cls._create_test_user("teacher_test@smartapp.test", "SmartApp Teacher")
		cls._create_test_user("admin_test@smartapp.test", "SmartApp Admin")
		cls._create_test_user(
			"multirole_test@smartapp.test",
			"SmartApp Teacher",
			extra_role="SmartApp Admin",
		)

	@classmethod
	def _create_test_user(cls, email, role, extra_role=None):
		"""Helper to create a Frappe User with a specific role if not exists."""
		if frappe.db.exists("User", email):
			return
		user = frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": email.split("@")[0].replace("_", " ").title(),
			"send_welcome_email": 0,
			"new_password": "Test@123456",
		})
		user.insert(ignore_permissions=True)
		user.add_roles(role)
		if extra_role:
			user.add_roles(extra_role)

	# ------------------------------------------------------------------ #

	def test_founder_has_access_to_all_dashboards(self):
		"""SmartApp Founder should have access to every dashboard."""
		frappe.set_user("founder_test@smartapp.test")
		data = get_user_dashboards()
		dashboard_names = [d["name"] for d in data["dashboards"]]
		self.assertTrue(len(dashboard_names) == 6, "Founder should see all 6 dashboards")
		self.assertIn("Founder", dashboard_names)
		self.assertIn("Guru", dashboard_names)
		self.assertIn("Wali Santri", dashboard_names)

	def test_teacher_allowed_guru_dashboard_only(self):
		"""SmartApp Teacher without additional config should access Guru dashboard."""
		frappe.set_user("teacher_test@smartapp.test")
		access = check_access("Guru")
		self.assertTrue(access.get("allowed"), "Teacher should have access to Guru dashboard")

	def test_guest_redirect_to_landing(self):
		"""Guest user must be redirected to landing page."""
		frappe.set_user("Guest")
		access = check_access("Admin")
		self.assertFalse(access.get("allowed"))
		self.assertEqual(access.get("redirect"), "/")

	def test_unauthorized_user_redirect_to_own_dashboard(self):
		"""Teacher trying to access Founder dashboard should be redirected."""
		frappe.set_user("teacher_test@smartapp.test")
		access = check_access("Founder")
		self.assertFalse(access.get("allowed"))
		redirect = access.get("redirect", "")
		# Redirect should point to their own dashboard, not Founder
		self.assertNotIn("founder", redirect.lower(), "Teacher should not redirect to founder dashboard")

	def test_multirole_user_has_multiple_dashboards(self):
		"""User with Teacher + Admin roles should see both dashboards."""
		frappe.set_user("multirole_test@smartapp.test")
		data = get_user_dashboards()
		dashboard_names = [d["name"] for d in data["dashboards"]]
		self.assertGreaterEqual(len(dashboard_names), 2, "Multi-role user should have at least 2 dashboards")

	@classmethod
	def tearDownClass(cls):
		frappe.set_user("Administrator")
