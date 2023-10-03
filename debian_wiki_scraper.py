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
        # Find all the links in the content div
        links = content_div.find_all('a')

        # Extract the text and href attributes from the links
        link_data = [(link.get_text(), link['href']) for link in links if link.has_attr('href')]

        # Convert relative links to absolute links
        link_data = [(text, debian_wiki_url + href if href.startswith('/') else href) for text, href in link_data]

        # Convert the extracted links to Markdown format
        markdown_links = [f"[{text}]({href})" for text, href in link_data]

        # Extract the text from the content div
        content_text = content_div.prettify()

        # Extract the footer content
        footer = soup.find(id='footer').prettify()
                
        # Convert the extracted text, links, and footer to Markdown format
        converter = html2text.HTML2Text()
        markdown_content = converter.handle(content_text)
        markdown_footer = converter.handle(footer)

        # Write the Markdown content and links to a file
        with open('debian_news.md', 'w', encoding='utf-8') as file:
            file.write('# News\n\n')
            file.write('\n\n')
            file.write(markdown_content)
            file.write('\n\n')
            file.write(markdown_footer)
            
        print('Debian News page and links have been successfully converted to Markdown and saved to debian_news.md.')
    else:
        print('Content div not found on the Debian News page.')
else:
    print('Failed to fetch the Debian News page.')
