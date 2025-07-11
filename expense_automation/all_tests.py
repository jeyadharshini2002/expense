import unittest
import os
import io
import builtins
import HtmlTestRunner
from expense_testcases.authentication.login import LoginPage
from expense_testcases.category import Category
from expense_testcases.subcategory import SubCategory
from expense_testcases.expenses import Expenses
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

# === Test Class ===
class AllTests(TestBase):
    """Run all test cases in a single Chrome session"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.login = LoginPage(cls.driver)
        cls.dash = TestDashboard(cls.driver)
        cls.configu = Category(cls.driver)
        cls.subconfigu = SubCategory(cls.driver)
        cls.expenses = Expenses(cls.driver)
        cls.expreport = exp_report(cls.driver)
        cls.category_ledger = category_ledger(cls.driver)
        cls.out = Logout(cls.driver)


    def setUp(self) -> None:
        """
        Setup before each test - no new driver or page objects
        """
        super().setUp()
    # === Login Tests ===
    def test_01_login_invalid_credentials(self):
        print("Page: Login")
        print()
        print("Expected output: Invalid credentials message should be shown")
        self.login.a_login_invalid_credentials()

    def test_02_login_invalid_password(self):
        print("Page: Login")
        print("Expected output: Invalid password message should be shown")
        self.login.b_login_invalid_password()

    def test_03_login_invalid_username(self):
        print("Page: Login")
        print("Expected output: Invalid username message should be shown")
        self.login.c_login_invalid_username()

    def test_04_login_without_password(self):
        print("Page: Login")
        print("Expected output: Error shown when password is missing")
        self.login.d_login_without_password()

    def test_05_login_without_username(self):
        print("Page: Login")
        print("Expected output: Error shown when username is missing")
        self.login.e_login_without_username()

    def test_06_login_successful(self):
        print("Page: Login")
        print("Expected output: User logged in successfully and redirected to dashboard")
        self.login.f_login_successful()


    # === Dashboard ===
    def test_07_dashboard_header(self):
        print("Page: Dashboard")
        print("Expected output: Dashboard header is displayed correctly")
        self.dash.dash_header()

    def test_08_dashboard_balance_calculation(self):
        print("Page: Dashboard")
        print("Expected output: Dashboard balance calculation is accurate")
        self.dash.test_dashboard_balance_calculation()

    def test_09_dashboard_balance_non_negative(self):
        print("Page: Dashboard")
        print("Expected output: Dashboard balance is non-negative")
        self.dash.test_dashboard_balance_non_negative()

    def test_10_dashboard_amounts_displayed(self):
        print("Page: Dashboard")
        print("Expected output: Dashboard shows correct income and expense amounts")
        self.dash.test_dashboard_amounts_displayed()


    # === Category ===
    def test_11_category_tab(self):
        print("Page: Category")
        print("Expected output: Category tab is accessible")
        self.configu.cat_tab()

    def test_12_cat_header(self):
        print("Page: Category")
        print("Expected output: Category header is displayed correctly")
        self.configu.cat_header()

    def test_13_create_new_category(self):
        print("Page: Category")
        print("Expected output: New category created successfully")
        self.configu.test_create_new_category()

    def test_14_empty_category_name(self):
        print("Page: Category")
        print("Expected output: Error shown for empty category name")
        self.configu.test_empty_category_name()

    def test_15_category_whitespace_only(self):
        print("Page: Category")
        print("Expected output: Error shown for whitespace-only category name")
        self.configu.test_category_name_whitespace_only()

    def test_16_invalid_category_name(self):
        print("Page: Category")
        print("Expected output: Error shown for invalid category name")
        self.configu.test_invalid_category_name()

    def test_17_duplicate_category_name(self):
        print("Page: Category")
        print("Expected output: Error shown for duplicate category name")
        self.configu.test_duplicate_category_name()

    def test_18_long_category_name(self):
        print("Page: Category")
        print("Expected output: Error shown for overly long category name")
        self.configu.test_long_category_name()

    def test_19_edit_category(self):
        print("Page: Category")
        print("Expected output: Existing category is edited successfully")
        self.configu.test_edit_category()

    def test_20_edit_category_empty_name(self):
        print("Page: Category")
        print("Expected output: Error shown when editing category with empty name")
        self.configu.test_edit_category_empty_name()

    def test_21_edit_to_duplicate_category_name(self):
        print("Page: Category")
        print("Expected output: Error shown when editing to duplicate name")
        self.configu.test_edit_to_duplicate_category_name()

    def test_22_delete_category(self):
        print("Page: Category")
        print("Expected output: Category deleted successfully")
        self.configu.delete_category_and_verify()

    def test_23_category_snackbar_add(self):
        print("Page: Category")
        print("Expected output: Snackbar message shown on adding category")
        self.configu.snackbar_add_category()

    def test_24_category_snackbar_edit(self):
        print("Page: Category")
        print("Expected output: Snackbar message shown on editing category")
        self.configu.snackbar_edit_category()


    # === Subcategory ===
    def test_25_subcategory_tab(self):
        print("Page: Subcategory")
        print("Expected output: Subcategory tab is accessible")
        self.subconfigu.sub_tab()

    def test_26_subcategory_header(self):
        print("Page: Subcategory")
        print("Expected output: Subcategory header is displayed correctly")
        self.subconfigu.sub_header()

    def test_27_create_new_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: New subcategory created successfully")
        self.subconfigu.test_create_new_subcategory()

    def test_28_empty_subcategory_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for empty subcategory name")
        self.subconfigu.test_empty_subcategory_name()

    def test_29_whitespace_subcategory_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for whitespace-only subcategory name")
        self.subconfigu.test_whitespace_subcategory_name()

    def test_30_invalid_subcategory_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for invalid subcategory name")
        self.subconfigu.test_invalid_subcategory_name()

    def test_31_duplicate_subcategory_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for duplicate subcategory name")
        self.subconfigu.test_duplicate_subcategory_name()

    def test_32_subcategory_without_category(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for subcategory without category")
        self.subconfigu.test_subcategory_without_category()

    def test_33_long_subcategory_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown for overly long subcategory name")
        self.subconfigu.test_long_subcategory_name()

    def test_34_edit_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: Existing subcategory edited successfully")
        self.subconfigu.test_edit_subcategory()

    def test_35_edit_subcategory_empty_name(self):
        print("Page: Subcategory")
        print("Expected output: Error shown when editing subcategory with empty name")
        self.subconfigu.test_edit_subcategory_empty_name()

    def test_36_delete_subcategory(self):
        print("Page: Subcategory")
        print("Expected output: Subcategory deleted successfully")
        self.subconfigu.test_delete_subcategory()

    def test_37_subcategory_snackbar_add(self):
        print("Page: Subcategory")
        print("Expected output: Snackbar shown when subcategory is added")
        self.subconfigu.snackbar_add_subcategory()

    def test_38_subcategory_snackbar_edit(self):
        print("Page: Subcategory")
        print("Expected output: Snackbar shown when subcategory is edited")
        self.subconfigu.snackbar_edit_subcategory()


    # === Expenses ===
    def test_39_expense_tab(self):
        print("Page: Expenses")
        print("Expected output: Expense tab is accessible")
        self.expenses.expense_tab()

    def test_40_expense_header(self):
        print("Page: Expenses")
        print("Expected output: Expense header displayed correctly")
        self.expenses.exp_header()

    def test_41_expense_search(self):
        print("Page: Expenses")
        print("Expected output: Expense search works correctly")
        self.expenses.test_expense_search_functionality()

    def test_42_add_income(self):
        print("Page: Expenses")
        print("Expected output: Valid income added successfully")
        self.expenses.test_valid_income_add()

    def test_43_income_empty_required_fields_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown when adding income with empty required fields")
        self.expenses.test_income_empty_required_fields_add()

    def test_44_income_file_upload_invalid_type_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown for invalid file type upload")
        self.expenses.test_income_file_upload_invalid_type_add()

    def test_45_income_snackbar_add(self):
        print("Page: Expenses")
        print("Expected output: Snackbar shown when income is added")
        self.expenses.test_income_snackbar_add()

    def test_46_income_invalid_date_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown for invalid date while adding income")
        self.expenses.income_invalid_date_add()

    def test_47_valid_expense_add(self):
        print("Page: Expenses")
        print("Expected output: Valid expense added successfully")
        self.expenses.test_valid_expense_add()

    def test_48_expense_empty_required_fields_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown for empty required fields while adding expense")
        self.expenses.test_expense_empty_required_fields_add()

    def test_49_expense_file_upload_invalid_type_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown for invalid file type upload for expense")
        self.expenses.test_expense_file_upload_invalid_type_add()

    def test_50_expense_snackbar_add(self):
        print("Page: Expenses")
        print("Expected output: Snackbar shown when expense is added")
        self.expenses.test_expense_snackbar_add()

    def test_51_expense_invalid_date_add(self):
        print("Page: Expenses")
        print("Expected output: Error shown for invalid date while adding expense")
        self.expenses.expense_invalid_date_add()

    def test_52_edit_expense(self):
        print("Page: Expenses")
        print("Expected output: Existing expense edited successfully")
        self.expenses.test_expense_edit()

    def test_53_expense_edit_empty_required_fields(self):
        print("Page: Expenses")
        print("Expected output: Error shown for empty required fields while editing expense")
        self.expenses.test_expense_edit_empty_required_fields()

    def test_54_expense_edit_invalid_amount(self):
        print("Page: Expenses")
        print("Expected output: Error shown for invalid amount while editing expense")
        self.expenses.test_expense_edit_invalid_amount()

    def test_55_snackbar_expense_edit(self):
        print("Page: Expenses")
        print("Expected output: Snackbar shown when expense is edited")
        self.expenses.test_snackbar_expense_edit()

    def test_56_expense_edit_delete(self):
        print("Page: Expenses")
        print("Expected output: Edited expense deleted successfully")
        self.expenses.test_expense_edit_delete()

    def test_57_expense_delete(self):
        print("Page: Expenses")
        print("Expected output: Expense deleted successfully")
        self.expenses.test_expense_delete()

    def test_58_snackbar_expense_delete(self):
        print("Page: Expenses")
        print("Expected output: Snackbar shown when expense is deleted")
        self.expenses.snackbar_expense_delete()


    # === Expense Report ===
    def test_59_expense_report(self):
        print("Page: Expense Report")
        print("Expected output: Expense report tab loads successfully")
        self.expreport.exprep_tab()

    def test_60_expreport_header(self):
        print("Page: Expense Report")
        print("Expected output: Expense report header displayed correctly")
        self.expreport.exprep_header()

    def test_61_filter_by_month_and_year(self):
        print("Page: Expense Report")
        print("Expected output: Expenses filtered by month and year correctly")
        self.expreport.test_02_filter_by_month_and_year()

    def test_62_filter_by_date_range(self):
        print("Page: Expense Report")
        print("Expected output: Expenses filtered by date range correctly")
        self.expreport.test_03_filter_by_date_range()

    def test_63_export_expense_to_excel(self):
        print("Page: Expense Report")
        print("Expected output: Expense report exported to Excel successfully")
        self.expreport.test_04_export_to_excel()


    # === Category Ledger ===
    def test_64_category_ledger(self):
        print("Page: Category Ledger")
        print("Expected output: Category ledger tab loads successfully")
        self.category_ledger.catledg_tab()

    def test_65_category_ledger_header(self):
        print("Page: Category Ledger")
        print("Expected output: Category ledger header displayed correctly")
        self.category_ledger.catledger_header()

    def test_66_filter_category_ledger_by_date(self):
        print("Page: Category Ledger")
        print("Expected output: Ledger records filtered by date correctly")
        self.category_ledger.test_filter_by_date()

    def test_67_totals_calculation(self):
        print("Page: Category Ledger")
        print("Expected output: Totals calculation is accurate")
        self.category_ledger.test_totals_calculation()

    def test_68_export_category_ledger_to_excel(self):
        print("Page: Category Ledger")
        print("Expected output: Category ledger exported to Excel successfully")
        self.category_ledger.test_export_to_excel()


    # === Logout ===
    def test_69_logout(self):
        print("Page: Logout")
        print("Expected output: User logged out and redirected to login page")
        self.out.logout()

        

# === Main Runner ===
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORT_DIR = os.path.join(current_dir, 'reports')
    os.makedirs(REPORT_DIR, exist_ok=True)

    print(f"[DEBUG] Report will be generated at: {REPORT_DIR}")

    # === Manual Test Suite in Execution Order ===
    suite = unittest.TestSuite()

    # Login
    suite.addTest(AllTests('test_01_login_invalid_credentials'))
    suite.addTest(AllTests('test_02_login_invalid_password'))
    suite.addTest(AllTests('test_03_login_invalid_username'))
    suite.addTest(AllTests('test_04_login_without_password'))
    suite.addTest(AllTests('test_05_login_without_username'))
    suite.addTest(AllTests('test_06_login_successful'))

    # # Dashboard
    suite.addTest(AllTests('test_07_dashboard_header'))
    suite.addTest(AllTests('test_08_dashboard_balance_calculation'))
    suite.addTest(AllTests('test_09_dashboard_balance_non_negative'))
    suite.addTest(AllTests('test_10_dashboard_amounts_displayed'))

    # # Category
    suite.addTest(AllTests('test_11_category_tab'))
    suite.addTest(AllTests('test_12_cat_header'))
    suite.addTest(AllTests('test_13_create_new_category'))
    suite.addTest(AllTests('test_14_empty_category_name'))
    suite.addTest(AllTests('test_15_category_whitespace_only'))
    suite.addTest(AllTests('test_16_invalid_category_name'))
    suite.addTest(AllTests('test_17_duplicate_category_name'))
    suite.addTest(AllTests('test_18_long_category_name'))
    suite.addTest(AllTests('test_19_edit_category'))
    suite.addTest(AllTests('test_20_edit_category_empty_name'))
    suite.addTest(AllTests('test_21_edit_to_duplicate_category_name'))
    suite.addTest(AllTests('test_22_delete_category'))
    suite.addTest(AllTests('test_23_category_snackbar_add'))
    suite.addTest(AllTests('test_24_category_snackbar_edit'))

    # # Subcategory
    suite.addTest(AllTests('test_25_subcategory_tab'))
    suite.addTest(AllTests('test_26_subcategory_header'))
    suite.addTest(AllTests('test_27_create_new_subcategory'))
    suite.addTest(AllTests('test_28_empty_subcategory_name'))
    suite.addTest(AllTests('test_29_whitespace_subcategory_name'))
    suite.addTest(AllTests('test_30_invalid_subcategory_name'))
    suite.addTest(AllTests('test_31_duplicate_subcategory_name'))
    suite.addTest(AllTests('test_32_subcategory_without_category'))
    suite.addTest(AllTests('test_33_long_subcategory_name'))
    suite.addTest(AllTests('test_34_edit_subcategory'))
    suite.addTest(AllTests('test_35_edit_subcategory_empty_name'))
    suite.addTest(AllTests('test_36_delete_subcategory'))
    suite.addTest(AllTests('test_37_subcategory_snackbar_add'))
    suite.addTest(AllTests('test_38_subcategory_snackbar_edit'))

    # # Expenses
    suite.addTest(AllTests('test_39_expense_tab'))
    suite.addTest(AllTests('test_40_expense_header'))
    suite.addTest(AllTests('test_41_expense_search'))
    suite.addTest(AllTests('test_42_add_income'))
    suite.addTest(AllTests('test_43_income_empty_required_fields_add'))
    suite.addTest(AllTests('test_44_income_file_upload_invalid_type_add'))
    suite.addTest(AllTests('test_45_income_snackbar_add'))
    suite.addTest(AllTests('test_46_income_invalid_date_add'))
    suite.addTest(AllTests('test_47_valid_expense_add'))
    suite.addTest(AllTests('test_48_expense_empty_required_fields_add'))
    suite.addTest(AllTests('test_49_expense_file_upload_invalid_type_add'))
    suite.addTest(AllTests('test_50_expense_snackbar_add'))
    suite.addTest(AllTests('test_51_expense_invalid_date_add'))
    suite.addTest(AllTests('test_52_edit_expense'))
    suite.addTest(AllTests('test_53_expense_edit_empty_required_fields'))
    suite.addTest(AllTests('test_54_expense_edit_invalid_amount'))
    suite.addTest(AllTests('test_55_snackbar_expense_edit'))
    suite.addTest(AllTests('test_56_expense_edit_delete'))
    suite.addTest(AllTests('test_57_expense_delete'))
    suite.addTest(AllTests('test_58_snackbar_expense_delete'))

    # # Expense Report
    suite.addTest(AllTests('test_59_expense_report'))
    suite.addTest(AllTests('test_60_expreport_header'))
    suite.addTest(AllTests('test_61_filter_by_month_and_year'))
    suite.addTest(AllTests('test_62_filter_by_date_range'))
    suite.addTest(AllTests('test_63_export_expense_to_excel'))

    # # Category Ledger
    suite.addTest(AllTests('test_64_category_ledger'))
    suite.addTest(AllTests('test_65_category_ledger_header'))
    suite.addTest(AllTests('test_66_filter_category_ledger_by_date'))
    suite.addTest(AllTests('test_67_totals_calculation'))
    suite.addTest(AllTests('test_68_export_category_ledger_to_excel'))

    # Logout
    suite.addTest(AllTests('test_69_logout'))

    # === Run HTMLTestRunner ===
    runner = HtmlTestRunner.HTMLTestRunner(
        output=REPORT_DIR,
        report_name='Expense_Automation_Report',
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

    # === Excel Report Generation ===
    excel_path = os.path.join(REPORT_DIR, 'Expense_Automation_Report.xlsx')
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Results"

    # Start time and summary
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    duration = 0  # Can calculate if needed

    failed_tests = {test.test_name.split('.')[-1] for test in result.failures}
    errored_tests = {test.test_name.split('.')[-1] for test in result.errors}
    total_tests = result.testsRun
    passed_tests = total_tests - len(failed_tests) - len(errored_tests)

    # Summary row
    ws.append(["Start Time", "Duration (s)", "Total", "Pass", "Fail", "Errors"])
    ws.append([start_time, duration, total_tests, passed_tests, len(failed_tests), len(errored_tests)])
    ws.append([])

    # Table header
    ws.append(["Module","Test Case", "Expected Result", "Status"])

    # === Define mapping of test names to descriptions ===
    # You can expand this list with more expected outputs per test case
    test_cases_info = {
        # Login
        "test_01_login_invalid_credentials": ("Login", "Invalid credentials message should be shown"),
        "test_02_login_invalid_password": ("Login", "Login should fail with incorrect password"),
        "test_03_login_invalid_username": ("Login", "Login should fail with incorrect username"),
        "test_04_login_without_password": ("Login", "Error shown for missing password"),
        "test_05_login_without_username": ("Login", "Error shown for missing username"),
        "test_06_login_successful": ("Login", "User should login successfully"),

        # Dashboard
        "test_07_dashboard_header": ("Dashboard", "Dashboard header should be visible"),
        "test_08_dashboard_balance_calculation": ("Dashboard", "Balance should be calculated correctly"),
        "test_09_dashboard_balance_non_negative": ("Dashboard", "Balance should not be negative"),
        "test_10_dashboard_amounts_displayed": ("Dashboard", "All amounts displayed correctly"),

        # Category
        "test_11_category_tab": ("Category", "Category tab opens"),
        "test_12_cat_header": ("Category", "Header visible"),
        "test_13_create_new_category": ("Category", "New category created"),
        "test_14_empty_category_name": ("Category", "Error on empty name"),
        "test_15_category_whitespace_only": ("Category", "Error on whitespace"),
        "test_16_invalid_category_name": ("Category", "Invalid name rejected"),
        "test_17_duplicate_category_name": ("Category", "Duplicate name blocked"),
        "test_18_long_category_name": ("Category", "Max length validated"),
        "test_19_edit_category": ("Category", "Category edited"),
        "test_20_edit_category_empty_name": ("Category", "Empty edit rejected"),
        "test_21_edit_to_duplicate_category_name": ("Category", "Duplicate edit blocked"),
        "test_22_delete_category": ("Category", "Category deleted"),
        "test_23_category_snackbar_add": ("Category", "Snackbar shown on add"),
        "test_24_category_snackbar_edit": ("Category", "Snackbar shown on edit"),

        # Subcategory
        "test_25_subcategory_tab": ("Subcategory", "Tab opens"),
        "test_26_subcategory_header": ("Subcategory", "Header visible"),
        "test_27_create_new_subcategory": ("Subcategory", "New subcategory created"),
        "test_28_empty_subcategory_name": ("Subcategory", "Error on empty"),
        "test_29_whitespace_subcategory_name": ("Subcategory", "Error on whitespace"),
        "test_30_invalid_subcategory_name": ("Subcategory", "Invalid name rejected"),
        "test_31_duplicate_subcategory_name": ("Subcategory", "Duplicate rejected"),
        "test_32_subcategory_without_category": ("Subcategory", "Category selection required"),
        "test_33_long_subcategory_name": ("Subcategory", "Max length checked"),
        "test_34_edit_subcategory": ("Subcategory", "Edit success"),
        "test_35_edit_subcategory_empty_name": ("Subcategory", "Empty edit rejected"),
        "test_36_delete_subcategory": ("Subcategory", "Delete success"),
        "test_37_subcategory_snackbar_add": ("Subcategory", "Snackbar on add"),
        "test_38_subcategory_snackbar_edit": ("Subcategory", "Snackbar on edit"),

        # Expenses
        "test_39_expense_tab": ("Expenses", "Expense tab opens"),
        "test_40_expense_header": ("Expenses", "Header visible"),
        "test_41_expense_search": ("Expenses", "Search works"),
        "test_42_add_income": ("Expenses", "Income added"),
        "test_43_income_empty_required_fields_add": ("Expenses", "Empty fields error"),
        "test_44_income_file_upload_invalid_type_add": ("Expenses", "Invalid file rejected"),
        "test_45_income_snackbar_add": ("Expenses", "Snackbar shown"),
        "test_46_income_invalid_date_add": ("Expenses", "Invalid date rejected"),
        "test_47_valid_expense_add": ("Expenses", "Expense added"),
        "test_48_expense_empty_required_fields_add": ("Expenses", "Empty fields error"),
        "test_49_expense_file_upload_invalid_type_add": ("Expenses", "Invalid file rejected"),
        "test_50_expense_snackbar_add": ("Expenses", "Snackbar shown"),
        "test_51_expense_invalid_date_add": ("Expenses", "Invalid date rejected"),
        "test_52_edit_expense": ("Expenses", "Edit success"),
        "test_53_expense_edit_empty_required_fields": ("Expenses", "Empty edit error"),
        "test_54_expense_edit_invalid_amount": ("Expenses", "Invalid amount rejected"),
        "test_55_snackbar_expense_edit": ("Expenses", "Snackbar on edit"),
        "test_56_expense_edit_delete": ("Expenses", "Deleted after edit"),
        "test_57_expense_delete": ("Expenses", "Delete success"),
        "test_58_snackbar_expense_delete": ("Expenses", "Snackbar on delete"),

        # Expense Report
        "test_59_expense_report": ("Expense Report", "Page opens"),
        "test_60_expreport_header": ("Expense Report", "Header shown"),
        "test_61_filter_by_month_and_year": ("Expense Report", "Filter works"),
        "test_62_filter_by_date_range": ("Expense Report", "Range filter works"),
        "test_63_export_expense_to_excel": ("Expense Report", "Export success"),

        # Category Ledger
        "test_64_category_ledger": ("Category Ledger", "Page opens"),
        "test_65_category_ledger_header": ("Category Ledger", "Header shown"),
        "test_66_filter_category_ledger_by_date": ("Category Ledger", "Filter by date"),
        "test_67_totals_calculation": ("Category Ledger", "Totals correct"),
        "test_68_export_category_ledger_to_excel": ("Category Ledger", "Export success"),

        # Logout
        "test_69_logout": ("Logout", "User logs out"),
    }

    # Add rows to Excel
    for test_case, (module, expected) in test_cases_info.items():
        if test_case in failed_tests:
            status = "Fail"
        elif test_case in errored_tests:
            status = "Error"
        else:
            status = "Pass"
        ws.append([ module,test_case, expected, status])

    # Save workbook
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