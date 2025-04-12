import unittest
from unittest.mock import patch, MagicMock
from scraper import download_table_content, download_all_tables

class TestScraper(unittest.TestCase):

    @patch('scraper.webdriver.Chrome')
    @patch('scraper.gspread.Client')
    def test_download_table_content(self, mock_gspread_client, mock_webdriver):
        # Mock the WebDriver instance
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver

        # Mock the Google Sheets client and spreadsheet
        mock_spreadsheet = MagicMock()
        mock_gspread_client.open_by_key.return_value = mock_spreadsheet

        # Simulate the behavior of the function
        result = download_table_content(mock_driver, "Witel Performance")

        # Assertions
        self.assertTrue(result)
        mock_driver.find_elements.assert_called()
        mock_spreadsheet.add_worksheet.assert_called()

    @patch('scraper.webdriver.Chrome')
    @patch('scraper.gspread.Client')
    def test_download_all_tables(self, mock_gspread_client, mock_webdriver):
        # Mock the WebDriver instance
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver

        # Mock the Google Sheets client and spreadsheet
        mock_spreadsheet = MagicMock()
        mock_gspread_client.open_by_key.return_value = mock_spreadsheet

        # Simulate the behavior of the function
        result = download_all_tables(mock_driver)

        # Assertions
        self.assertTrue(result)
        mock_driver.find_elements.assert_called()
        mock_spreadsheet.add_worksheet.assert_called()

if __name__ == '__main__':
    unittest.main()