import unittest
import os
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

class AllTests(TestBase):
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

    def setUp(self) -> None:
        super().setUp()

    def test_01_login_invalid_credentials(self):
        self.login.a_login_invalid_credentials()

    def b_login_invalid_password(self):
        self.login.b_login_invalid_password()
    def c_login_invalid_username(self):
        self.login.c_login_invalid_username()
    def d_login_without_password(self):
        self.login.d_login_without_password()
    def e_login_without_username(self):
        self.login.e_login_without_username()
    def f_login_successful(self):
        self.login.f_login_successful()
    
    def test_dashboard_balance_calculation(self):
        self.dash.test_dashboard_balance_calculation()
    def test_dashboard_balance_non_negative(self):
        self.dash.test_dashboard_balance_non_negative()
    def test_dashboard_amounts_displayed(self):
        self.dash.test_dashboard_amounts_displayed()
    

    def test_02_category_tab(self):
        self.configu.cat_tab()

    def test_03_create_new_category(self):
        self.configu.test_create_new_category()

    def test_04_empty_category_name(self):
        self.configu.test_empty_category_name()

    def test_05_category_whitespace_only(self):
        self.configu.test_category_name_whitespace_only()

    def test_06_invalid_category_name(self):
        self.configu.test_invalid_category_name()

    def test_07_duplicate_category_name(self):
        self.configu.test_duplicate_category_name()

    def test_08_long_category_name(self):
        self.configu.test_long_category_name()

    def test_09_edit_category(self):
        self.configu.test_edit_category()

    def test_10_edit_category_empty_name(self):
        self.configu.test_edit_category_empty_name()

    def test_11_edit_to_duplicate_category_name(self):
        self.configu.test_edit_to_duplicate_category_name()

    def test_12_delete_category(self):
        self.configu.delete_category_and_verify()

    def test_13_category_snackbar_add(self):
        self.configu.snackbar_add_category()

    def test_14_category_snackbar_edit(self):
        self.configu.snackbar_edit_category()

    def test_15_subcategory_tab(self):
        self.subconfigu.sub_tab()

    def test_16_create_new_subcategory(self):
        self.subconfigu.test_create_new_subcategory()

    def test_17_empty_subcategory_name(self):
        self.subconfigu.test_empty_subcategory_name()

    def test_18_whitespace_subcategory_name(self):
        self.subconfigu.test_whitespace_subcategory_name()

    def test_19_invalid_subcategory_name(self):
        self.subconfigu.test_invalid_subcategory_name()

    def test_20_duplicate_subcategory_name(self):
        self.subconfigu.test_duplicate_subcategory_name()

    def test_21_subcategory_without_category(self):
        self.subconfigu.test_subcategory_without_category()

    def test_22_long_subcategory_name(self):
        self.subconfigu.test_long_subcategory_name()

    def test_23_edit_subcategory(self):
        self.subconfigu.test_edit_subcategory()

    def test_24_edit_subcategory_empty_name(self):
        self.subconfigu.test_edit_subcategory_empty_name()

    def test_25_delete_subcategory(self):
        self.subconfigu.test_delete_subcategory()

    def test_26_subcategory_snackbar_add(self):
        self.subconfigu.snackbar_add_subcategory()

    def test_27_subcategory_snackbar_edit(self):
        self.subconfigu.snackbar_edit_subcategory()

    def test_28_expense_tab(self):
        self.expenses.expense_tab()

    def test_29_expense_search(self):
        self.expenses.test_expense_search_functionality()

    def test_30_add_income(self):
        self.expenses.test_valid_income_add()

    def test_31_income_empty_required_fields_add(self):
        self.expenses.test_income_empty_required_fields_add()

    def test_32_income_file_upload_invalid_type_add(self):
        self.expenses.test_income_file_upload_invalid_type_add()

    def test_33_income_snackbar_add(self):
        self.expenses.test_income_snackbar_add()

    def test_34_income_invalid_date_add(self):
        self.expenses.income_invalid_date_add()

    def test_35_valid_expense_add(self):
        self.expenses.test_valid_expense_add()

    def test_36_expense_empty_required_fields_add(self):
        self.expenses.test_expense_empty_required_fields_add()

    def test_37_expense_file_upload_invalid_type_add(self):
        self.expenses.test_expense_file_upload_invalid_type_add()

    def test_38_expense_snackbar_add(self):
        self.expenses.test_expense_snackbar_add()

    def test_39_expense_invalid_date_add(self):
        self.expenses.expense_invalid_date_add()

    def test_40_edit_expense(self):
        self.expenses.test_expense_edit()

    def test_41_expense_edit_empty_required_fields(self):
        self.expenses.test_expense_edit_empty_required_fields()

    def test_42_expense_edit_invalid_amount(self):
        self.expenses.test_expense_edit_invalid_amount()

    def test_43_snackbar_expense_edit(self):
        self.expenses.test_snackbar_expense_edit()

    def test_44_expense_edit_delete(self):
        self.expenses.test_expense_edit_delete()

    def test_45_expense_delete(self):
        self.expenses.test_expense_delete()

    def test_46_snackbar_expense_delete(self):
        self.expenses.snackbar_expense_delete()

    def test_47_expense_report(self):
        self.expreport.exprep_tab()

    def test_48_filter_by_month_and_year(self):
        self.expreport.test_02_filter_by_month_and_year()

    def test_49_filter_by_date_range(self):
        self.expreport.test_03_filter_by_date_range()

    def test_50_export_expense_to_excel(self):
        self.expreport.test_04_export_to_excel()

    def test_51_category_ledger(self):
        self.category_ledger.catledg_tab()

    def test_52_filter_category_ledger_by_date(self):
        self.category_ledger.test_filter_by_date()

    def test_53_totals_calculation(self):
        self.category_ledger.test_totals_calculation()

    def test_54_export_category_ledger_to_excel(self):
        self.category_ledger.test_export_to_excel()
        
    def logout(self):
        """
        Logout after all tests
        """
        self.out.logout()
    

    


if __name__ == "__main__":
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    REPORT_DIR = os.path.join(current_dir, 'reports')

    # Create reports directory if it doesn't exist
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        print(f"[DEBUG] Created reports directory: {REPORT_DIR}")

    print(f"[DEBUG] Report will be generated at: {REPORT_DIR}")

     # === Manual Test Suite in Execution Order ===
    suite = unittest.TestSuite()
    suite.addTest(AllTests('test_01_login_invalid_credentials'))
    suite.addTest(AllTests('b_login_invalid_password'))
    suite.addTest(AllTests('c_login_invalid_username'))
    suite.addTest(AllTests('d_login_without_password'))
    suite.addTest(AllTests('e_login_without_username'))
    suite.addTest(AllTests('f_login_successful'))

    suite.addTest(AllTests('test_dashboard_balance_calculation'))
    suite.addTest(AllTests('test_dashboard_balance_non_negative'))
    suite.addTest(AllTests('test_dashboard_amounts_displayed'))

    
    suite.addTest(AllTests('test_02_category_tab'))
    suite.addTest(AllTests('test_03_create_new_category'))
    suite.addTest(AllTests('test_04_empty_category_name'))
    suite.addTest(AllTests('test_05_category_whitespace_only'))
    suite.addTest(AllTests('test_06_invalid_category_name'))
    suite.addTest(AllTests('test_07_duplicate_category_name'))
    suite.addTest(AllTests('test_08_long_category_name'))
    suite.addTest(AllTests('test_09_edit_category'))
    suite.addTest(AllTests('test_10_edit_category_empty_name'))
    suite.addTest(AllTests('test_11_edit_to_duplicate_category_name'))
    suite.addTest(AllTests('test_12_delete_category'))
    suite.addTest(AllTests('test_13_category_snackbar_add'))
    suite.addTest(AllTests('test_14_category_snackbar_edit'))



    suite.addTest(AllTests('test_15_subcategory_tab'))
    suite.addTest(AllTests('test_16_create_new_subcategory'))
    suite.addTest(AllTests('test_17_empty_subcategory_name'))
    suite.addTest(AllTests('test_18_whitespace_subcategory_name'))
    suite.addTest(AllTests('test_19_invalid_subcategory_name'))
    suite.addTest(AllTests('test_20_duplicate_subcategory_name'))
    suite.addTest(AllTests('test_21_subcategory_without_category'))
    suite.addTest(AllTests('test_22_long_subcategory_name'))
    suite.addTest(AllTests('test_23_edit_subcategory'))
    suite.addTest(AllTests('test_24_edit_subcategory_empty_name'))
    suite.addTest(AllTests('test_25_delete_subcategory'))
    suite.addTest(AllTests('test_26_subcategory_snackbar_add'))
    suite.addTest(AllTests('test_27_subcategory_snackbar_edit'))



    suite.addTest(AllTests('test_28_expense_tab'))
    suite.addTest(AllTests('test_29_expense_search'))
    suite.addTest(AllTests('test_30_add_income'))
    suite.addTest(AllTests('test_31_income_empty_required_fields_add'))
    suite.addTest(AllTests('test_32_income_file_upload_invalid_type_add'))
    suite.addTest(AllTests('test_33_income_snackbar_add'))
    suite.addTest(AllTests('test_34_income_invalid_date_add'))
    suite.addTest(AllTests('test_35_valid_expense_add'))
    suite.addTest(AllTests('test_36_expense_empty_required_fields_add'))
    suite.addTest(AllTests('test_37_expense_file_upload_invalid_type_add'))
    suite.addTest(AllTests('test_38_expense_snackbar_add'))
    suite.addTest(AllTests('test_39_expense_invalid_date_add'))
    suite.addTest(AllTests('test_40_edit_expense'))
    suite.addTest(AllTests('test_41_expense_edit_empty_required_fields'))
    suite.addTest(AllTests('test_42_expense_edit_invalid_amount'))
    suite.addTest(AllTests('test_43_snackbar_expense_edit'))
    suite.addTest(AllTests('test_44_expense_edit_delete'))
    suite.addTest(AllTests('test_45_expense_delete'))
    suite.addTest(AllTests('test_46_snackbar_expense_delete'))



    suite.addTest(AllTests('test_47_expense_report'))
    suite.addTest(AllTests('test_48_filter_by_month_and_year'))
    suite.addTest(AllTests('test_49_filter_by_date_range'))
    suite.addTest(AllTests('test_50_export_expense_to_excel'))


    suite.addTest(AllTests('test_51_category_ledger'))
    suite.addTest(AllTests('test_52_filter_category_ledger_by_date'))
    suite.addTest(AllTests('test_53_totals_calculation'))
    suite.addTest(AllTests('test_54_export_category_ledger_to_excel'))
    suite.addTest(AllTests('logout'))


    # Run tests with HTML report
    runner = HtmlTestRunner.HTMLTestRunner(
        output=REPORT_DIR,
        report_name='Expense_Automation_Report',
        combine_reports=True,
        add_timestamp=True,
        verbosity=2
    )

    print(f"[DEBUG] Starting test execution with single Chrome session...")
    result = runner.run(suite)

    # List generated reports
    if os.path.exists(REPORT_DIR):
        print(f"[DEBUG] Generated reports:")
        for file in os.listdir(REPORT_DIR):
            if file.endswith('.html'):
                full_path = os.path.join(REPORT_DIR, file)
                print(f"  - {file}")
                print(f"    Full path: {full_path}")

    print(f"[DEBUG] Test execution completed!")
    print(f"[DEBUG] Tests run: {result.testsRun}")
    print(f"[DEBUG] Failures: {len(result.failures)}")
    print(f"[DEBUG] Errors: {len(result.errors)}")
    print(f"[DEBUG] Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100:.1f}%")
