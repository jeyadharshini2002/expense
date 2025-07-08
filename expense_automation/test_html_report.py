import unittest
import HtmlTestRunner
import os

class SimpleTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
    

if __name__ == "__main__":
    REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    print(f"[DEBUG] Running simple test, report will be generated at: {REPORT_DIR}")
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output=REPORT_DIR,
            report_name='Simple_Test_Report',
            combine_reports=True,
            add_timestamp=True,
            verbosity=2,
            descriptions=True
        )
    )
