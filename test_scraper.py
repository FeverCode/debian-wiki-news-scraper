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

class TestScraperFunctions(unittest.TestCase):

    def test_fetch_page_content(self):
        content = fetch_page_content('https://www.example.com')
        self.assertTrue(content)

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
        test_filename = 'test_output.md'
        save_to_file(test_content, test_footer, test_filename)
        with open(test_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        self.assertIn(test_content, content)
        self.assertIn(test_footer, content)
        os.remove(test_filename)  # Clean up test file

if __name__ == '__main__':
    unittest.main()
