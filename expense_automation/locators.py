from selenium.webdriver.common.by import By

class Locators:
    """
    Centralized locator definitions.
    """
    EMAIL_INPUT = (By.XPATH, "//input[@id='EmailId']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='Password']")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")
    LOGIN_INVALID_CREDENTIALS=(By.XPATH, "//p[normalize-space()='Invalid email or password.']")

    DASHBOARD_HEADER = (By.XPATH, "//div[@class='page-header']")
    LOGIN_PASSWORD_ONLY_REQUIRED = (By.XPATH, "//*[contains(text(),'The Password field is required.')]")
    LOGIN_USERNAME_ONLY_REQUIRED = (By.XPATH, "//*[contains(text(),'The EmailId field is required.')]")
    INVALID_ERROR_MSG = (By.XPATH, "(//p[normalize-space()='Invalid email or password.'])[1]")


    CATEGORY_SIDEBAR=(By.XPATH, "(//span[normalize-space()='Category'])[1]")
    PER_PAGE=(By.XPATH, "//select[@id='perPage']")
    NEW_CATEGORY_BUTTON=(By.XPATH, "(//a[normalize-space()='New Category'])[1]")
    CATEGORY_NAME_INPUT=(By.XPATH, "//input[@id='CategoryName']")
    EXPENSE_RADIO_BUTTON=(By.XPATH, "(//label[normalize-space()='Expense'])[1]")
    CATEGORY_REQUIRED_MSG=(By.XPATH,"//span[@id='CategoryName-error']")
    CATEGORY_CODE_LINK = (By.XPATH, "(//a[normalize-space()='Category Code'])[1]")
    CATEGORY_CODE_LINK_TEXT = (By.XPATH, "//a[normalize-space()='Category Code']")
    DUPLICATE_MSG=(By.XPATH,"(//span[@class='text-danger small field-validation-error'])[1]")
    BACK_CATEGORY=(By.XPATH, "(//a[normalize-space()='Back'])[1]")


    SAVE_CATEGORY_BUTTON=(By.XPATH, "(//button[normalize-space()='Save'])[1]")

    EDIT_CATEGORY_BUTTON=(By.XPATH, "(//i[@class='mdi mdi-pencil'])[1]")
    EDIT_CATEGORY_NAME_INPUT=(By.XPATH, "//input[@id='CategoryName']")
    EDIT_INCOME_RADIO_BUTTON=(By.XPATH, "(//label[normalize-space()='Income'])[1]")
    UPDATE_CATEGORY_BUTTON=(By.XPATH, "(//button[normalize-space()='Update'])[1]")
    DELETE_BUTTON=(By.XPATH, "(//i[@class='mdi mdi-delete'])[1]")
    DELETE_CONFIRM_BUTTON=(By.XPATH, "//button[@id='confirmDeleteBtn']")


    # subcategory page

    SUBCATEGORY_SIDEBAR=(By.XPATH,"(//span[normalize-space()='Subcategory'])[1]")
    SUBCATEGORY_PER_PAGE=(By.XPATH, "(//select[@id='catPageSize'])[1]")
    SUBCATEGORY_CATEGORY=(By.XPATH, "(//select[@id='CategoryID'])[1]")
    SUBCATEGORY_SEARCH_INPUT=(By.XPATH, "(//input[@id='categorySearch'])[1]")
    SUBCATEGORY_NEW_BUTTON=(By.XPATH, "(//button[normalize-space()='New Subcategory'])[1]")
    SUBCATEGORY_NAME_INPUT=(By.XPATH, "(//input[@id='SubCategoryName'])[1]")
    SUBCATEGORY_CATEGORY_REQUIRED_MSG=(By.XPATH, "(//span[@id='CategoryID-error'])[1]")
    SUBCATEGORY_REQUIRED_MSG=(By.XPATH, "(//span[@data-valmsg-for='SubCategoryName'])[1]")
    SUBCATEGORY_CODE_REQUIRED_MSG=(By.XPATH, "(//span[@data-valmsg-for='SubCategoryName'])[1]")
    SUBCATEGORY_CODE_LINK = (By.XPATH, "(//a[normalize-space()='Subcategory Code'])[1]")
    SUBCATEGORY_CODE_LINK_TEXT = (By.XPATH, "(//a[normalize-space()='Subcategory Code'])[1]")
    SUBCATEGORY_DUPLICATE_MSG=(By.XPATH,"(//span[@class='text-danger small field-validation-error'])[1]")
    SUBCATEGORY_BACK_BUTTON=(By.XPATH, "(//a[normalize-space()='Back'])[1]")
    SUBCATEGORY_SAVE_BUTTON=(By.XPATH, "(//button[normalize-space()='Save'])[1]")
    SUBCATEGORY_EDIT_BUTTON=(By.XPATH, "(//a[@title='Edit'])[1]")
    SUBCATEGORY_EDIT_NAME_INPUT=(By.XPATH, "(//input[@id='SubCategoryName'])[1]")
    SUBCATEGORY_UPDATE_BUTTON=(By.XPATH, "(//button[normalize-space()='Update'])[1]")
    SUBCATEGORY_DELETE_BUTTON=(By.XPATH, "(//i)[20]")
    SUBCATEGORY_DELETE_CONFIRM_BUTTON=(By.XPATH, "(//button[normalize-space()='Yes, Delete'])[1]")
    SUBCATEGORY_DELETE_CANCEL=(By.XPATH, "(//button[@type='button'][normalize-space()='Cancel'])[1]")

    # expense page
    EXPENSE_SIDEBAR=(By.XPATH, "(//span[normalize-space()='Expenses'])[1]")
    EXPENSE_PERPAGE=(By.XPATH, "(//select[@id='catPageSize'])[1]")
    EXPENSE_DELETE=(By.XPATH, "(//i[@class='mdi mdi-delete'])[1]")
    EXPENSE_SEARCH=(By.ID, "categorySearch")
    EXPENSE_ACTION_TEXT=(By.XPATH,"(//th[@class='text-dark text-center fw-semibold'])[1]")
    EXPENSE_SEARCH_RESULTS=(By.XPATH,"(//td[contains(text(),'WATER CAN')])[1]")
    # add income in expense page
    EXPENSES_ADD_INCOME_BT=(By.XPATH, "(//a[normalize-space()='Add Income'])[1]")
    EXPENSES_ADD_EXPENSE_BT=(By.XPATH, "(//a[normalize-space()='Add Expense'])[1]")
    EXPENSES_INCOME_DATE=(By.XPATH, "(//input[@id='ExpenseDate'])[1]")
    EXPENSES_INCOME_CATEGORY=(By.XPATH, "(//select[@id='CategoryID'])[1]")
    EXPENSES_INCOME_SUBCATEGORY=(By.XPATH, "(//select[@id='SubCategoryID'])[1]")
    EXPENSES_INCOME_AMOUNT=(By.XPATH, "(//input[@id='Amount'])[1]")
    EXPENSES_INCOME_NOTES=(By.XPATH, "(//textarea[@id='Notes'])[1]")
    EXPENSES_ATTACH_FILE=(By.NAME, "file")
    EXPENSES_INCOME_SAVE=(By.XPATH, "(//button[normalize-space()='Save'])[1]")
    EXPENSES_INCOME_BACK=(By.XPATH, "(//a[normalize-space()='Back'])[1]")

    #add expensein expense page
    EXPENSES_ADD_EXPENSE_BT=(By.XPATH, "(//a[normalize-space()='Add Expense'])[1]")
    EXPENSES_EXPENSE_DATE=(By.XPATH, "(//input[@id='ExpenseDate'])[1]")
    EXPENSES_EXPENSE_CATEGORY=(By.XPATH, "(//select[@id='CategoryID'])[1]")
    EXPENSE_SUBCATEGORY=(By.XPATH, "(//select[@id='SubCategoryID'])[1]")
    EXPENSES_EXPENSE_AMOUNT=(By.XPATH, "(//input[@id='Amount'])[1]")
    EXPENSES_EXPENSE_NOTES=(By.XPATH, "(//textarea[@id='Notes'])[1]")
    EXPENSES_ATTACH_FILE=(By.ID, "file")
    EXPENSES_EXPENSE_SAVE=(By.XPATH, "(//button[normalize-space()='Save'])[1]")
    EXPENSES_EXPENSE_BACK=(By.XPATH, "(//a[normalize-space()='Back'])[1]")

    EXPENSES_EDIT_BUTTON=(By.XPATH, "(//a[@title='Edit'])[1]")
    EXPENSES_EDIT_DATE=(By.XPATH, "(//input[@id='ExpenseDate'])[1]")
    EXPENSES_EDIT_AMOUNT= (By.XPATH, "(//input[@id='Amount'])[1]")
    EXPENSES_EDIT_NOTES=(By.XPATH, "(//textarea[@id='Notes'])[1]")
    EXPENSE_1_EDIT= (By.XPATH, "(//i[@class='mdi mdi-pencil'])[1]")
    EXPENSE_1_DELETE=(By.XPATH, "(//i[@class='mdi mdi-delete'])[1]")
    EXPENSE_DELETE1_CONFIRM_BUTTON=(By.XPATH, "(//button[normalize-space()='Delete'])[1]")
    EXPENSE_DELETE1_CANCEL_BUTTON=(By.XPATH, "(//button[normalize-space()='Cancel'])[1]")
    EXPENSES_EDIT_SAVE=(By.XPATH, "(//button[normalize-space()='Submit'])[1]")

# expenses report
    EXPENSES_REPORT_SIDEBAR=(By.XPATH, "(//span[normalize-space()='Expense Report'])[1]")
    EXPENSES_REPORT_PERPAGE=(By.XPATH, "(//select[@id='catPageSize'])[1]")
    EXPENSES_MONTHS=(By.XPATH, "(//select[@id='month'])[1]")
    EXPENSES_YEAR=(By.XPATH, "(//select[@id='year'])[1]")
    EXPENSES_REPORT_START_DATE=(By.XPATH, "(//input[@id='startDate'])[1]")
    EXPENSES_REPORT_END_DATE=(By.XPATH, "(//input[@id='endDate'])[1]")
    EXPENSES_REPORT_SEARCH_BUTTON=(By.XPATH, "(//button[normalize-space()='Search'])[1]")
    EXPENSES_REPORT_CLEAR_BUTTON=(By.XPATH, "(//a[normalize-space()='Clear'])[1]")
    EXPENSE_REPORT_EXCEL_BUTTON=(By.XPATH, "(//button[normalize-space()='Excel'])[1]")
    RESULT_JULY=(By.XPATH,"(//td[contains(text(),'01-07-2025')])[1]")
    RESULT_2025=(By.XPATH,"(//td[normalize-space()='05-06-2025'])[1]")

# CATEGORY WISE LEDGER
    CATEGORY_WISE_LEDGER_SIDEBAR=(By.XPATH, "(//span[normalize-space()='Categorywise Ledger'])[1]")
    CATEGORY_WISE_LEDGER_PERPAGE=(By.XPATH, "(//select[@id='catPageSize'])[1]")
    CATEGORY_WISE_LEDGER_STARTDATE= (By.XPATH, "(//input[@id='startDate'])[1]")
    CATEGORY_WISE_LEDGER_ENDDATE=(By.XPATH, "(//input[@id='endDate'])[1]")
    CATEGORY_WISE_LEDGER_SEARCH_BUTTON=(By.XPATH, "(//button[normalize-space()='Search'])[1]")
    CATEGORY_WISE_LEDGER_CLEAR_BUTTON=(By.XPATH, "(//a[normalize-space()='Clear'])[1]")
    CATEGORY_WISE_LEDGER_EXCEL_BUTTON=(By.XPATH, "(//button[normalize-space()='Excel'])[1]")
    CATEGORY_WISE_LEDGER_RESULT=(By.XPATH, "(//td[contains(text(),'05-06-2025')])[1]")
    CATEGORY_WISE_LEDGER_RESULT2=(By.XPATH, "(//td[contains(text(),'01-07-2025')])[1]")

    LOGOUT_BT=(By.XPATH, "(//i[@class='mdi mdi-power'])[1]")
    LOGOUT_CONFIRM_BUTTON=(By.XPATH, "(//button[normalize-space()='Logout'])[1]")

    ADD_USER_BT=(By.XPATH, "(//i[@class='mdi mdi-account-plus'])[1]")
    USER_LIST=(By.XPATH,"(//a[normalize-space()='User List'])[1]")
    ADD_USER=(By.XPATH, "(//a[normalize-space()='Add User'])[1]")
    FNAME=(By.XPATH, "(//input[@id='FirstName'])[1]")
    LNAME=(By.XPATH, "(//input[@id='LastName'])[1]")
    EMAIL=(By.XPATH, "(//input[@id='EmailId'])[1]")
    PASSWORD=(By.XPATH, "(//input[@id='Password'])[1]")







    
    


