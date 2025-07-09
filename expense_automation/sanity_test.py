import unittest
import os
import io
import builtins
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

class SanityTests(TestBase):
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

    def setUp(self) -> None:
        """
        Setup before each test - no new driver or page objects
        """
        super().setUp()



    def f_login_successful(self):
        self.login.f_login_successful()

    def bug1_invalid_category_adding(self):
        self.configu.cat_tab()
        self.configu.test_invalid_category_name()


    def bug2_category_edit_snackbar(self):
        self.configu.cat_tab()
        self.configu.snackbar_edit_category()

    def bug3_required_msg_on_whitespace(self):
        self.subconfigu.sub_tab()
        self.subconfigu.test_whitespace_subcategory_name()


    def bug4_invalid_subcategory_adding(self):
        self.subconfigu.sub_tab()
        self.subconfigu.test_invalid_subcategory_name()
    
    def bug5_subcategory_edit_snackbar(self):
        self.subconfigu.sub_tab()
        self.subconfigu.snackbar_edit_subcategory()

  
    def bug6_expense_income_invalid_file_upload(self):
        self.expenses.expense_tab()
        self.expenses.test_income_file_upload_invalid_type_add()
    
    def bug7_expense_expense_invalid_file_upload(self):
        self.expenses.expense_tab()
        self.expenses.test_expense_file_upload_invalid_type_add()

    def bug8_expense_edit_empty_required_fields(self):
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_empty_required_fields()

    def bug9_expense_edit_invalid_amount(self):
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_invalid_amount()


    def bug10_snackbar_expense_edit(self):
        self.expenses.expense_tab()
        self.expenses.test_snackbar_expense_edit()

    def bug11_expense_edit_delete(self):
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_delete()


    def bug12_snackbar_expense_delete(self):
        self.expenses.expense_tab()
        self.expenses.snackbar_expense_delete()

    def logout(self):
        """
        Logout after all tests
        """
        self.out.logout()
    

    


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORT_DIR = os.path.join(current_dir, 'reports')
    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"[DEBUG] Report will be generated at: {REPORT_DIR}")

     # === Manual Test Suite in Execution Order ===
    suite = unittest.TestSuite()

    suite.addTest(SanityTests('f_login_successful'))

    suite.addTest(SanityTests('bug1_invalid_category_adding'))
    suite.addTest(SanityTests('bug2_category_edit_snackbar'))
    suite.addTest(SanityTests('bug3_required_msg_on_whitespace'))
    suite.addTest(SanityTests('bug4_invalid_subcategory_adding'))
    suite.addTest(SanityTests('bug5_subcategory_edit_snackbar'))
    suite.addTest(SanityTests('bug6_expense_income_invalid_file_upload'))
    suite.addTest(SanityTests('bug7_expense_expense_invalid_file_upload'))
    suite.addTest(SanityTests('bug8_expense_edit_empty_required_fields'))
    suite.addTest(SanityTests('bug9_expense_edit_invalid_amount'))
    suite.addTest(SanityTests('bug10_snackbar_expense_edit'))
    suite.addTest(SanityTests('bug11_expense_edit_delete'))
    suite.addTest(SanityTests('bug12_snackbar_expense_delete'))

    suite.addTest(SanityTests('logout'))

    # Run tests with HTML report
    runner = HtmlTestRunner.HTMLTestRunner(
        output=REPORT_DIR,
        report_name='Sanity_test_Report',
        combine_reports=True,
        # add_timestamp=True,
        verbosity=2
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