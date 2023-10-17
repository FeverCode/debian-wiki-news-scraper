import unittest
from debian_wiki_scraper import (
    fetch_page_content,
    update_links,
    extract_content_and_footer,
    convert_to_markdown,
    save_to_file
)
from bs4 import BeautifulSoup
import os
from unittest.mock import patch, Mock

class TestScraperFunctions(unittest.TestCase):

    def setUp(self):
        # Mock response for 404 status code
        self.mock_response_404 = self.create_mock_response(404, "Page Not Found")

        # Mock response for requests.get
        self.mock_response = self.create_mock_response(200, "Mocked content")
        self.test_filename = 'test_output.md'

    def create_mock_response(self, status_code, text):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.text = text
        return mock_response

    def tearDown(self):
        # Clean up any test file created
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_fetch_page_content(self):
        with patch('requests.get', return_value=self.mock_response):
            content = fetch_page_content('https://www.example.com')
            self.assertTrue(content)
            self.assertEqual(content, "Mocked content")

    def test_update_links(self):
        soup = BeautifulSoup("<a href='/link'>Link</a>", 'html.parser')
        update_links(soup)
        self.assertEqual(soup.find('a')['href'], 'https://wiki.debian.org/link')

    def test_extract_content_and_footer(self):
        html_content = "<div id='content'>Content</div><div id='footer'>Footer</div>"
        content, footer = extract_content_and_footer(html_content)
        self.assertEqual(content.text, 'Content')
        self.assertEqual(footer.text, 'Footer')

    def test_convert_to_markdown(self):
        soup = BeautifulSoup("<div id='content'>Content</div><div id='footer'>Footer</div>", 'html.parser')
        markdown_content, markdown_footer = convert_to_markdown(soup.find(id='content'), soup.find(id='footer'))
        self.assertIn('Content', markdown_content)
        self.assertIn('Footer', markdown_footer)

    def test_save_to_file(self):
        test_content = "Test Content"
        test_footer = "Test Footer"
        save_to_file(test_content, test_footer, self.test_filename)
        with open(self.test_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        self.assertIn(test_content, content)
        self.assertIn(test_footer, content)


    def test_fetch_page_content_404_status(self):
        with patch('requests.get', return_value=self.mock_response_404):
            with self.assertRaises(ValueError):
                fetch_page_content('https://www.example.com')


if __name__ == '__main__':
    unittest.main()
