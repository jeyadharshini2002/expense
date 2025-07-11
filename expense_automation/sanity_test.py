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
        print("Page: Login")
        print("Expected output: Login is common for All Bugs")
        print()

    def bug1_invalid_category_adding(self):
        print("Page: Category")
        print("Expected output: Invalid category name should be rejected with an error message")
        print()
        self.configu.cat_tab()
        self.configu.test_invalid_category_name()

    def bug2_category_edit_snackbar(self):
        print("Page: Category")
        print("Expected output: Snackbar message should appear when editing category")
        print()
        self.configu.cat_tab()
        self.configu.snackbar_edit_category()

    def bug3_required_msg_on_whitespace(self):
        print("Page: Subcategory")
        print("Expected output: Required validation message should appear for whitespace-only subcategory name")
        print()
        self.subconfigu.sub_tab()
        self.subconfigu.test_whitespace_subcategory_name()

    def bug4_invalid_subcategory_adding(self):
        print("Page: Subcategory")
        print("Expected output: Invalid subcategory name should be rejected with an error message")
        print()
        self.subconfigu.sub_tab()
        self.subconfigu.test_invalid_subcategory_name()

    def bug5_subcategory_edit_snackbar(self):
        print("Page: Subcategory")
        print("Expected output: Snackbar message should appear when editing subcategory")
        print()
        self.subconfigu.sub_tab()
        self.subconfigu.snackbar_edit_subcategory()

    def bug6_expense_income_invalid_file_upload(self):
        print("Page: Expenses")
        print("Expected output: Invalid file type for income upload should be rejected with an error message")
        print()
        self.expenses.expense_tab()
        self.expenses.test_income_file_upload_invalid_type_add()

    def bug7_expense_expense_invalid_file_upload(self):
        print("Page: Expenses")
        print("Expected output: Invalid file type for expense upload should be rejected with an error message")
        print()
        self.expenses.expense_tab()
        self.expenses.test_expense_file_upload_invalid_type_add()

    def bug8_expense_edit_empty_required_fields(self):
        print("Page: Expenses")
        print("Expected output: Required field validation should trigger when editing expense with empty fields")
        print()
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_empty_required_fields()

    def bug9_expense_edit_invalid_amount(self):
        print("Page: Expenses")
        print("Expected output: Invalid amount should be rejected when editing expense")
        print()
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_invalid_amount()

    def bug10_snackbar_expense_edit(self):
        print("Page: Expenses")
        print("Expected output: Snackbar message should appear when expense is edited")
        print()
        self.expenses.expense_tab()
        self.expenses.test_snackbar_expense_edit()

    def bug11_expense_edit_delete(self):
        print("Page: Expenses")
        print("Expected output: Edited expense should be deleted successfully")
        print()
        self.expenses.expense_tab()
        self.expenses.test_expense_edit_delete()

    def bug12_snackbar_expense_delete(self):
        print("Page: Expenses")
        print("Expected output: Snackbar message should appear when expense is deleted")
        print()
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


    
    # === Prepare Excel Workbook ===
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Results"

    # === Metadata Summary Header ===
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    duration = 0  # Fill this in with timing logic if needed

    # Extract test method names from HtmlTestRunner
    failed_tests = {test.test_name.split('.')[-1] for test in result.failures}
    errored_tests = {test.test_name.split('.')[-1] for test in result.errors}
    passed_count = result.testsRun - len(failed_tests) - len(errored_tests)

    # Summary
    ws.append(["Start Time", "Duration (s)", "Total", "Pass", "Fail", "Errors"])
    ws.append([start_time, duration, result.testsRun, passed_count, len(failed_tests), len(errored_tests)])
    ws.append([])

    # Table Headers
    ws.append(["Page","Case", "Expected Result",  "Status"])

    # Your list of test method names (manual order)
    test_methods = [
        "f_login_successful",
        "bug1_invalid_category_adding",
        "bug2_category_edit_snackbar",
        "bug3_required_msg_on_whitespace",
        "bug4_invalid_subcategory_adding",
        "bug5_subcategory_edit_snackbar",
        "bug6_expense_income_invalid_file_upload",
        "bug7_expense_expense_invalid_file_upload",
        "bug8_expense_edit_empty_required_fields",
        "bug9_expense_edit_invalid_amount",
        "bug10_snackbar_expense_edit",
        "bug11_expense_edit_delete",
        "bug12_snackbar_expense_delete",
        "logout"
    ]

    def parse_testname(name):
        if "bug1" in name:
            return "Category", "Invalid category name should be rejected with an error message"
        if "bug2" in name:
            return "Category", "Snackbar message should appear when editing category"
        if "bug3" in name:
            return "Subcategory", "Required validation message should appear for whitespace-only subcategory name"
        if "bug4" in name:
            return "Subcategory", "Invalid subcategory name should be rejected with an error message"
        if "bug5" in name:
            return "Subcategory", "Snackbar message should appear when editing subcategory"
        if "bug6" in name:
            return "Expenses", "Invalid file type for income upload should be rejected with an error message"
        if "bug7" in name:
            return "Expenses", "Invalid file type for expense upload should be rejected with an error message"
        if "bug8" in name:
            return "Expenses", "Required field validation should trigger when editing expense with empty fields"
        if "bug9" in name:
            return "Expenses", "Invalid amount should be rejected when editing expense"
        if "bug10" in name:
            return "Expenses", "Snackbar message should appear when expense is edited"
        if "bug11" in name:
            return "Expenses", "Edited expense should be deleted successfully"
        if "bug12" in name:
            return "Expenses", "Snackbar message should appear when expense is deleted"
        if "f_login" in name:
            return "Login", "Login should be successful"
        if "logout" in name:
            return "Logout", "Logout should be successful"
        return "Unknown", ""

    # Add each test result row
    for method_name in test_methods:
        page, expected = parse_testname(method_name)
        if method_name in failed_tests:
            status = "Fail"
        elif method_name in errored_tests:
            status = "Error"
        else:
            status = "Pass"
        ws.append([page, expected, method_name, status])

    # Save Excel
    excel_path = os.path.join(REPORT_DIR, 'Sanity_test_Report.xlsx')
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