import requests
from bs4 import BeautifulSoup
import html2text

# Define the URL of the Debian Wiki News page
debian_wiki_url = 'https://wiki.debian.org/News'

# Send an HTTP GET request to the URL
response = requests.get(debian_wiki_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the content div on the page
    if (content_div := soup.find(id='content')):
        # Preprocess the links to make them absolute
        for a in content_div.find_all('a'):
            if a.has_attr('href') and a['href'].startswith('/'):
                a['href'] = 'https://wiki.debian.org' + a['href']

        # Convert the modified HTML to markdown
        converter = html2text.HTML2Text()
        markdown_content = converter.handle(content_div.prettify())

        # Extract the footer content and convert to markdown
        footer = soup.find(id='footer').prettify()
        markdown_footer = converter.handle(footer)

        # Write the Markdown content to a file
        with open('debian_news.md', 'w', encoding='utf-8') as file:
            file.write('# News\n\n')
            file.write(markdown_content)
            file.write('\n\n')
            file.write(markdown_footer)
            
        print('Debian News page has been successfully converted to Markdown and saved to debian_news.md.')
    else:
        print('Content div not found on the Debian News page.')
else:
    print('Failed to fetch the Debian News page.')
