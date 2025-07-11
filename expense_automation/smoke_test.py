import unittest
import os
import io
import builtins
import HtmlTestRunner
from expense_testcases.authentication.login import LoginPage
from expense_testcases.category import Category
from expense_testcases.subcategory import SubCategory
import HtmlTestRunner
from expense_testcases.expenses import Expenses
from test_base import TestBase
from expense_testcases.expense_report import exp_report
from expense_testcases.categorywiseledger import category_ledger
from expense_testcases.authentication.logout import Logout
from expense_testcases.dashboard import TestDashboard
from test_base import TestBase
import HtmlTestRunner.result
from openpyxl import Workbook
from datetime import datetime

# === Monkey patch to fix traceback level ===
def _count_relevant_tb_levels(self, tb):
    length = 0
    while tb and not self._is_relevant_tb_level(tb):
        tb = tb.tb_next
        length += 1
    return length

HtmlTestRunner.result.HtmlTestResult._count_relevant_tb_levels = _count_relevant_tb_levels

# === Monkey patch to fix UnicodeEncodeError ===
original_open = open
def utf8_open(*args, **kwargs):
    if len(args) >= 1 and args[0].endswith(".html"):
        kwargs["encoding"] = "utf-8"
    return original_open(*args, **kwargs)
builtins.open = utf8_open  # Apply patch

class SmokeTests(TestBase):
    """
    Run all test cases here - Single Chrome session for all tests
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize Chrome driver and page objects once for all tests
        """
        super().setUpClass()
        cls.login = LoginPage(cls.driver)
        cls.dash = TestDashboard(cls.driver)  # Use TestDashboard for dashboard tests
        cls.configu = Category(cls.driver)
        cls.subconfigu = SubCategory(cls.driver)
        cls.expenses = Expenses(cls.driver)
        cls.expreport= exp_report(cls.driver)
        cls.category_ledger = category_ledger(cls.driver)
        cls.out= Logout(cls.driver)  # Reuse the logout method from LoginPage
    def shortDescription(self):
        return self._testMethodDoc 

    def setUp(self) -> None:
        """
        Setup before each test - no new driver or page objects
        """
        super().setUp()

    def setUp(self) -> None:
        super().setUp()

    def test_01_login_successful(self):
        print("Page: Login")
        print("Expected output: User should login successfully")
        print()
        self.login.f_login_successful()

    def test_02_dashboard_amounts_displayed(self):
        print("Page: Dashboard")
        print("Expected output: All amounts should be displayed correctly on the dashboard")
        print()
        self.dash.test_dashboard_amounts_displayed()

    def test_03_category_tab(self):
        print("Page: Category")
        print("Expected output: Category tab should open successfully")
        print()
        self.configu.cat_tab()

    def test_04_create_new_category(self):
        print("Page: Category")
        print("Expected output: New category should be created successfully")
        print()
        self.configu.test_create_new_category()

    def test_05_edit_category(self):
        print("Page: Category")
        print("Expected output: Existing category should be edited successfully")
        print()
        self.configu.test_edit_category()

    def test_06_delete_category(self):
        print("Page: Category")
        print("Expected output: Category should be deleted successfully and verified")
        print()
        self.configu.delete_category_and_verify()

    def test_07_subcategory_tab(self):
        print("Page: Subcategory")
        print("Expected output: Subcategory tab should open successfully")
        print()
        self.subconfigu.sub_tab()

    def test_08_create_new_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: New subcategory should be created successfully")
        print()
        self.subconfigu.test_create_new_subcategory()

    def test_09_edit_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: Existing subcategory should be edited successfully")
        print()
        self.subconfigu.test_edit_subcategory()

    def test_10_delete_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: Subcategory should be deleted successfully")
        print()
        self.subconfigu.test_delete_subcategory()

    def test_11_expense_tab(self):
        print("Page: Expenses")
        print("Expected output: Expense tab should open successfully")
        print()
        self.expenses.expense_tab()

    def test_12_add_income(self):
        print("Page: Expenses")
        print("Expected output: Income should be added successfully")
        print()
        self.expenses.test_valid_income_add()

    def test_13_add_expense(self):
        print("Page: Expenses")
        print("Expected output: Expense should be added successfully")
        print()
        self.expenses.test_valid_expense_add()

    def test_14_edit_expense(self):
        print("Page: Expenses")
        print("Expected output: Existing expense should be edited successfully")
        print()
        self.expenses.test_expense_edit()

    def test_15_delete_expense(self):
        print("Page: Expenses")
        print("Expected output: Expense should be deleted successfully")
        print()
        self.expenses.test_expense_delete()

    def test_16_expense_report_tab(self):
        print("Page: Expense Report")
        print("Expected output: Expense Report tab should open successfully")
        print()
        self.expreport.exprep_tab()

    def test_17_export_expense_to_excel(self):
        print("Page: Expense Report")
        print("Expected output: Expense data should be filtered and exported to Excel successfully")
        print()
        self.expreport.test_03_filter_by_date_range()
        self.expreport.test_04_export_to_excel()

    def test_18_category_ledger_tab(self):
        print("Page: Category Ledger")
        print("Expected output: Category Ledger tab should open successfully")
        print()
        self.category_ledger.catledg_tab()

    def test_19_export_category_ledger_to_excel(self):
        print("Page: Category Ledger")
        print("Expected output: Category Ledger should be exported to Excel successfully")
        print()
        self.category_ledger.test_export_to_excel()

    def test_20_logout(self):
        print("Page: Logout")
        print("Expected output: User should logout successfully")
        print()
        self.out.logout()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORT_DIR = os.path.join(current_dir, 'reports')
    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"[DEBUG] Report will be generated at: {REPORT_DIR}")

     # === Manual Test Suite in Execution Order ===
    suite = unittest.TestSuite()

    suite.addTest(SmokeTests('test_01_login_successful'))
    suite.addTest(SmokeTests('test_02_dashboard_amounts_displayed'))

    suite.addTest(SmokeTests('test_03_category_tab'))
    suite.addTest(SmokeTests('test_04_create_new_category'))
    suite.addTest(SmokeTests('test_05_edit_category'))
    suite.addTest(SmokeTests('test_06_delete_category'))

    suite.addTest(SmokeTests('test_07_subcategory_tab'))
    suite.addTest(SmokeTests('test_08_create_new_subcategory'))
    suite.addTest(SmokeTests('test_09_edit_subcategory'))
    suite.addTest(SmokeTests('test_10_delete_subcategory'))

    suite.addTest(SmokeTests('test_11_expense_tab'))
    suite.addTest(SmokeTests('test_12_add_income'))
    suite.addTest(SmokeTests('test_13_add_expense'))
    suite.addTest(SmokeTests('test_14_edit_expense'))
    suite.addTest(SmokeTests('test_15_delete_expense'))

    suite.addTest(SmokeTests('test_16_expense_report_tab'))
    suite.addTest(SmokeTests('test_17_export_expense_to_excel'))

    suite.addTest(SmokeTests('test_18_category_ledger_tab'))
    suite.addTest(SmokeTests('test_19_export_category_ledger_to_excel'))

    suite.addTest(SmokeTests('test_20_logout'))


    # Run tests with HTML report
    runner = HtmlTestRunner.HTMLTestRunner(
        output=REPORT_DIR,
        report_name='Smoketest_Report',
        combine_reports=True,
        # add_timestamp=True,
        verbosity=2,
        descriptions=True
    )
    print(f"[DEBUG] Starting test execution with single Chrome session...")
    result = runner.run(suite)

    # === Restore original open function ===
    builtins.open = original_open

    # === Print generated report info ===
    if os.path.exists(REPORT_DIR):
        print(f"[DEBUG] Generated reports:")
        for file in os.listdir(REPORT_DIR):
            if file.endswith('.html'):
                full_path = os.path.join(REPORT_DIR, file)
                print(f"  - {file}")
                print(f"    Full path: {full_path}")
        # === Excel report generation ===
    excel_path = os.path.join(REPORT_DIR, 'Smoketest_Report.xlsx')
    wb = Workbook()
    ws = wb.active
    ws.title = "Smoke Test Results"

    # Track time
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    duration = 0  # Set manually if needed

    # Summary
    failed_tests = {test.test_name.split('.')[-1] for test in result.failures}
    errored_tests = {test.test_name.split('.')[-1] for test in result.errors}
    total_tests = result.testsRun
    passed_tests = total_tests - len(failed_tests) - len(errored_tests)

    # === Summary row ===
    ws.append(["Start Time", "Duration (s)", "Total", "Pass", "Fail", "Errors"])
    ws.append([start_time, duration, total_tests, passed_tests, len(failed_tests), len(errored_tests)])
    ws.append([])

    # === Table header ===
    ws.append(["Page",  "Test Case","Expected Result", "Status"])

    # === Map test method names to expected output ===
    test_cases = [
        ("test_01_login_successful", "Login", "User should login successfully"),
        ("test_02_dashboard_amounts_displayed", "Dashboard", "All amounts should be displayed correctly on the dashboard"),
        ("test_03_category_tab", "Category", "Category tab should open successfully"),
        ("test_04_create_new_category", "Category", "New category should be created successfully"),
        ("test_05_edit_category", "Category", "Existing category should be edited successfully"),
        ("test_06_delete_category", "Category", "Category should be deleted successfully and verified"),
        ("test_07_subcategory_tab", "Subcategory", "Subcategory tab should open successfully"),
        ("test_08_create_new_subcategory", "Subcategory", "New subcategory should be created successfully"),
        ("test_09_edit_subcategory", "Subcategory", "Existing subcategory should be edited successfully"),
        ("test_10_delete_subcategory", "Subcategory", "Subcategory should be deleted successfully"),
        ("test_11_expense_tab", "Expenses", "Expense tab should open successfully"),
        ("test_12_add_income", "Expenses", "Income should be added successfully"),
        ("test_13_add_expense", "Expenses", "Expense should be added successfully"),
        ("test_14_edit_expense", "Expenses", "Existing expense should be edited successfully"),
        ("test_15_delete_expense", "Expenses", "Expense should be deleted successfully"),
        ("test_16_expense_report_tab", "Expense Report", "Expense Report tab should open successfully"),
        ("test_17_export_expense_to_excel", "Expense Report", "Expense data should be filtered and exported to Excel successfully"),
        ("test_18_category_ledger_tab", "Category Ledger", "Category Ledger tab should open successfully"),
        ("test_19_export_category_ledger_to_excel", "Category Ledger", "Category Ledger should be exported to Excel successfully"),
        ("test_20_logout", "Logout", "User should logout successfully"),
    ]

    # === Populate Excel rows ===
    for case_name, page, expected in test_cases:
        if case_name in failed_tests:
            status = "Fail"
        elif case_name in errored_tests:
            status = "Error"
        else:
            status = "Pass"
        ws.append([page, expected, case_name, status])

    # === Save Excel file ===
    wb.save(excel_path)
    print(f"[DEBUG] Excel report saved at: {excel_path}")


    # === Test summary ===
    print(f"[DEBUG] Test execution completed!")
    print(f"[DEBUG] Tests run: {result.testsRun}")
    print(f"[DEBUG] Failures: {len(result.failures)}")
    print(f"[DEBUG] Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"[DEBUG] Success rate: {success_rate:.1f}%")
    else:
        print("[DEBUG] No tests were run. Success rate: 0.0%")