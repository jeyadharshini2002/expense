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

    def f_login_successful(self):
        """Authentication: Login"""
        self.login.f_login_successful()

    def test_dashboard_amounts_displayed(self):
        """Dashboard: Amounts Display"""
        self.dash.test_dashboard_amounts_displayed()

    def test_02_category_tab(self):
        """Category: Open Category Tab"""
        self.configu.cat_tab()

    def test_03_create_new_category(self):
        """Category: Create New Category"""
        self.configu.test_create_new_category()

    def test_09_edit_category(self):
        """Category: Edit Category"""
        self.configu.test_edit_category()

    def test_12_delete_category(self):
        """Category: Delete Category"""
        self.configu.delete_category_and_verify()

    def test_15_subcategory_tab(self):
        """Subcategory: Open Subcategory Tab"""
        self.subconfigu.sub_tab()

    def test_16_create_new_subcategory(self):
        """Subcategory: Create New Subcategory"""
        self.subconfigu.test_create_new_subcategory()

    def test_23_edit_subcategory(self):
        """Subcategory: Edit Subcategory"""
        self.subconfigu.test_edit_subcategory()

    def test_25_delete_subcategory(self):
        """Subcategory: Delete Subcategory"""
        self.subconfigu.test_delete_subcategory()

    def test_28_expense_tab(self):
        """Expense: Open Expense Tab"""
        self.expenses.expense_tab()

    def test_30_add_income(self):
        """Expense: Add Income"""
        self.expenses.test_valid_income_add()

    def test_add_expense(self):
        """Expense: Add Expense"""
        self.expenses.test_valid_expense_add()

    def test_40_edit_expense(self):
        """Expense: Edit Expense"""
        self.expenses.test_expense_edit()

    def test_45_expense_delete(self):
        """Expense: Delete Expense"""
        self.expenses.test_expense_delete()

    def test_47_expense_report(self):
        """Report: Open Expense Report Tab"""
        self.expreport.exprep_tab()

    def test_50_export_expense_to_excel(self):
        """Report: Export Expense to Excel"""
        self.expreport.test_03_filter_by_date_range()
        self.expreport.test_04_export_to_excel()

    def test_51_category_ledger(self):
        """Report: Open Category Ledger Tab"""
        self.category_ledger.catledg_tab()

    def test_54_export_category_ledger_to_excel(self):
        """Report: Export Category Ledger to Excel"""
        self.category_ledger.test_export_to_excel()

    def logout(self):
        """Authentication: Logout"""
        self.out.logout()  


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORT_DIR = os.path.join(current_dir, 'reports')
    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"[DEBUG] Report will be generated at: {REPORT_DIR}")

     # === Manual Test Suite in Execution Order ===
    suite = unittest.TestSuite()

    suite.addTest(SmokeTests('f_login_successful'))

    suite.addTest(SmokeTests('test_dashboard_amounts_displayed'))

    
    suite.addTest(SmokeTests('test_02_category_tab'))
    suite.addTest(SmokeTests('test_03_create_new_category'))
    suite.addTest(SmokeTests('test_09_edit_category'))
    suite.addTest(SmokeTests('test_12_delete_category'))



    suite.addTest(SmokeTests('test_15_subcategory_tab'))
    suite.addTest(SmokeTests('test_16_create_new_subcategory'))
    suite.addTest(SmokeTests('test_23_edit_subcategory'))
    suite.addTest(SmokeTests('test_25_delete_subcategory'))



    suite.addTest(SmokeTests('test_28_expense_tab'))
    suite.addTest(SmokeTests('test_30_add_income'))
    suite.addTest(SmokeTests('test_add_expense'))
    suite.addTest(SmokeTests('test_40_edit_expense'))
    suite.addTest(SmokeTests('test_45_expense_delete'))



    suite.addTest(SmokeTests('test_47_expense_report'))
    suite.addTest(SmokeTests('test_50_export_expense_to_excel'))


    suite.addTest(SmokeTests('test_51_category_ledger'))
    suite.addTest(SmokeTests('test_54_export_category_ledger_to_excel'))
    suite.addTest(SmokeTests('logout'))


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