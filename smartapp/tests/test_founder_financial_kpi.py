"""
Unit tests for Founder Dashboard Financial KPI REST API.
Run with: bench --site smarterp.localhost run-tests --module smartapp.tests.test_founder_financial_kpi
"""

import unittest
import frappe
from smartapp.api.dashboard import get_founder_financial_kpi


class TestFounderFinancialKPI(unittest.TestCase):

	def setUp(self):
		self.company = "Little Hafidz Qur'an (Demo)"

	def test_get_founder_financial_kpi_structure(self):
		"""Endpoint should return all required financial KPI keys with correct types."""
		data = get_founder_financial_kpi(company=self.company)

		required_keys = [
			"company",
			"period",
			"saldo_kas_bank",
			"pemasukan_bulan_ini",
			"pengeluaran_bulan_ini",
			"surplus_defisit",
			"laba_operasional",
			"total_piutang_spp",
			"unpaid_students_count",
		]

		for key in required_keys:
			self.assertIn(key, data, f"Key '{key}' must be present in response")

		self.assertEqual(data["company"], self.company)
		self.assertIsInstance(data["period"], dict)
		self.assertIn("from_date", data["period"])
		self.assertIn("to_date", data["period"])

		self.assertIsInstance(data["saldo_kas_bank"], float)
		self.assertIsInstance(data["pemasukan_bulan_ini"], float)
		self.assertIsInstance(data["pengeluaran_bulan_ini"], float)
		self.assertIsInstance(data["surplus_defisit"], float)
		self.assertIsInstance(data["laba_operasional"], float)
		self.assertIsInstance(data["total_piutang_spp"], float)
		self.assertIsInstance(data["unpaid_students_count"], int)

	def test_get_founder_financial_kpi_calculation_integrity(self):
		"""Surplus / defisit and operating profit must equal income minus expense."""
		data = get_founder_financial_kpi(company=self.company)

		expected_surplus = round(data["pemasukan_bulan_ini"] - data["pengeluaran_bulan_ini"], 2)
		self.assertEqual(round(data["surplus_defisit"], 2), expected_surplus)
		self.assertEqual(round(data["laba_operasional"], 2), expected_surplus)

	def test_get_founder_financial_kpi_custom_date_period(self):
		"""Passing a specific date should correctly adjust the period calculation."""
		custom_date = "2026-03-15"
		data = get_founder_financial_kpi(company=self.company, date=custom_date)

		self.assertEqual(data["period"]["from_date"], "2026-03-01")
		self.assertEqual(data["period"]["to_date"], "2026-03-31")
		# In March 2026, Penjualan was recorded in demo transactions
		self.assertGreaterEqual(data["pemasukan_bulan_ini"], 0.0)

	def test_get_founder_financial_kpi_fallback_for_nonexistent_company(self):
		"""Querying a nonexistent company should return zeroed values safely without exceptions."""
		data = get_founder_financial_kpi(company="Nonexistent Company ABC XYZ")

		self.assertEqual(data["saldo_kas_bank"], 0.0)
		self.assertEqual(data["pemasukan_bulan_ini"], 0.0)
		self.assertEqual(data["pengeluaran_bulan_ini"], 0.0)
		self.assertEqual(data["surplus_defisit"], 0.0)
		self.assertEqual(data["total_piutang_spp"], 0.0)
		self.assertEqual(data["unpaid_students_count"], 0)
