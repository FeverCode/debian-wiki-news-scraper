import requests
from bs4 import BeautifulSoup
import html2text

# Define the URL of the Debian Wiki News page
debian_wiki_url = 'https://wiki.debian.org/News'

# Send an HTTP GET request to the URL
response = requests.get(debian_wiki_url)

# Function to update relative links to absolute ones
def update_links(element):
    for a in element.find_all('a'):
        if a.has_attr('href') and a['href'].startswith('/'):
            # Only prefix the base URL for relative links
            a['href'] = 'https://wiki.debian.org' + a['href']

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the content div on the page and update its links
    if (content_div := soup.find(id='content')):
        update_links(content_div)

    # Extract the footer content and update its links
    footer = soup.find(id='footer')
    if footer:
        update_links(footer)

    # Convert the modified HTML to markdown
    converter = html2text.HTML2Text()
    markdown_content = converter.handle(content_div.prettify())
    markdown_footer = converter.handle(footer.prettify())

    # Write the Markdown content to a file
    with open('debian_news.md', 'w', encoding='utf-8') as file:
        file.write('# News\n\n')
        file.write(markdown_content)
        file.write('\n\n')
        file.write(markdown_footer)
            
    print('Debian News page has been successfully converted to Markdown and saved to debian_news.md.')
else:
    print('Failed to fetch the Debian News page.')
