from urllib.parse import urlparse

from youtube import get_transcripts_from_youtube
from website import scrape_website_links

def is_youtube_url(url):
    domain = urlparse(url).netloc
    if 'youtube' in domain:
        return True
    return False

def handle_links(links, db_name):
    urls = [url for url in links.split("\n") if url]

    for url in urls:
        if is_youtube_url(url):
            get_transcripts_from_youtube(url, db_name)
        else:
            scrape_website_links(url, db_name)
