import requests
from bs4 import BeautifulSoup
import html2text

BASE_URL = 'https://wiki.debian.org'

def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the page content.")
    return response.text

def update_links(element):
    for a in element.find_all('a'):
        if a.has_attr('href') and a['href'].startswith('/'):
            a['href'] = BASE_URL + a['href']

def extract_content_and_footer(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.find(id='content')
    footer = soup.find(id='footer')
    return content, footer

def convert_to_markdown(content, footer):
    converter = html2text.HTML2Text()
    markdown_content = converter.handle(content.prettify())
    markdown_footer = converter.handle(footer.prettify())
    return markdown_content, markdown_footer

def save_to_file(markdown_content, markdown_footer, filename='debian_news.md'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('# News\n\n')
        file.write(markdown_content)
        file.write('\n\n')
        file.write(markdown_footer)

def main():
    html_content = fetch_page_content(f"{BASE_URL}/News")
    content, footer = extract_content_and_footer(html_content)
    update_links(content)
    update_links(footer)
    markdown_content, markdown_footer = convert_to_markdown(content, footer)
    save_to_file(markdown_content, markdown_footer)
    print("Markdown file saved successfully!")

if __name__ == '__main__':
    main()
