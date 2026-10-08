"""Regression checks for ledger loading and the generated workbook."""

import contextlib
import io
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook, load_workbook

from KingdeeZwyCashFlowGenerator.configuration.settings import Config, Environment
from KingdeeZwyCashFlowGenerator.core.generator import CashFlowReportGenerator
from KingdeeZwyCashFlowGenerator.core.paths import CONFIG_PATH, TEMPLATE_DIR


class CashFlowWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.work_dir = Path(self.temporary_directory.name)
        self.ledger_path = self.work_dir / "明细账.xlsx"

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "明细账#测试"
        for column, name in {
            "A": "日期",
            "B": "凭证字号",
            "C": "摘要",
            "D": "对方科目",
            "E": "借方",
            "F": "贷方",
            "I": "余额",
        }.items():
            sheet[f"{column}4"] = name
        sheet["B6"] = "期初余额"
        sheet["I6"] = 1000
        sheet["A7"] = datetime(2026, 1, 5)
        sheet["B7"] = "记-001"
        sheet["C7"] = "收客户款"
        sheet["D7"] = "1122_应收账款_测试公司"
        sheet["E7"] = 100
        sheet["I7"] = 1100
        sheet["A8"] = datetime(2026, 1, 6)
        sheet["B8"] = "记-002"
        sheet["C8"] = "采购款"
        sheet["D8"] = "2202_应付账款_供应商公司"
        sheet["F8"] = 40
        sheet["I8"] = 1060
        workbook.save(self.ledger_path)

        Config._instance = None
        self.addCleanup(setattr, Config, "_instance", None)
        with contextlib.redirect_stdout(io.StringIO()):
            self.generator = CashFlowReportGenerator(Environment.DEVELOPMENT)

    def test_ledger_keeps_opening_balance_and_skips_total_row(self):
        with contextlib.redirect_stdout(io.StringIO()):
            transactions = self.generator.load_transactions(self.ledger_path)
            opening_balance = self.generator._extract_opening_balance_from_file(self.ledger_path)

        self.assertEqual(opening_balance, Decimal("1000"))
        self.assertEqual([item.voucher for item in transactions], ["记-001", "记-002"])
        self.assertEqual([item.amount for item in transactions], [Decimal("100"), Decimal("40")])
        self.assertEqual([item.balance for item in transactions], [Decimal("1100"), Decimal("1060")])

    def test_complete_flow_uses_project_resources_and_balance_formulas(self):
        self.assertTrue(CONFIG_PATH.is_file())
        self.assertTrue((TEMPLATE_DIR / "现金流原始表.xlsx").is_file())
        output_path = self.work_dir / "现金流.xlsx"
        self.generator.set_output_path(output_path)
        self.generator.bank_name = "测试银行"
        self.generator.period_value = "2026年第1期"
        self.generator.sheet_name = "测试银行_Q1"
        self.generator.output_filename = output_path.name

        with contextlib.redirect_stdout(io.StringIO()):
            completed = self.generator.run_full_flow(self.ledger_path, "Q1")

        self.assertTrue(completed)
        self.assertTrue(output_path.is_file())
        workbook = load_workbook(output_path)
        self.addCleanup(workbook.close)
        sheet = workbook["测试银行_Q1"]
        self.assertEqual(sheet["R4"].value, 1000)
        self.assertEqual(sheet["R5"].value, "=R4+SUM(N5:Q5)-SUM(J5:M5)")
        self.assertEqual(sheet["R6"].value, "=R5+SUM(N6:Q6)-SUM(J6:M6)")
        self.assertEqual(sheet["R7"].value, "=R4+SUM(O7:Q7)-SUM(K7:N7)-J7")
        self.assertEqual(sheet["U5"].value, "收客户款")
        self.assertEqual(sheet["U6"].value, "采购款")


if __name__ == "__main__":
    unittest.main()
