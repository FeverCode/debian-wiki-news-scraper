# Debian Wiki News Scraper

This Python script allows you to scrape the latest articles and links from the Debian Wiki News page and save them in Markdown format. Stay updated with the latest news and announcements from the Debian community!

## Prerequisites

- Python 3.x installed on your system.

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/debian-wiki-news-scraper.git

2. Navigate to the project directory:

    ```bash
    cd debian-wiki-news-scraper

3. Create and activate a virtual environment (venv) to 
    isolate project dependecies:     
    
    ```bash
    python -m venv venv
    
    source venv/bin/activate

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt

## Usage

* To run the Debian Wiki News scraper, execute the following command:

    ```bash
    python debian_wiki_scraper.py

The script will create a new file named `debian_news.md` in the project directory. The file will contain the latest news and announcements from the Debian community in Markdown format.

## Deactivating the Virtual Environment
* When you're done using the script, you can deactivate the virtual environment with the following command:

    ```bash
    deactivate

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.
