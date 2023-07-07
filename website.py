import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import nltk.data

nltk.download("punkt")
tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

visited_urls = set()
DATA_DIR = "data"

def is_valid(target_url, start_url):
    parsed_target = urlparse(target_url)
    parsed_start = urlparse(start_url)
    
    if parsed_target.fragment:
        return False
    
    return (parsed_target.netloc == parsed_start.netloc and 
            bool(parsed_target.scheme) and bool(parsed_target.netloc))

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError):
        return None

    return response.text

def extract_text_from_html(soup):
    text_parts = []
    for tag in soup.find_all(["title", "p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        part = " ".join(tag.stripped_strings)
        if part:
            text_parts.append(part)

    return " ".join(text_parts)

def segment_sentences(text):
    return tokenizer.tokenize(text)

def save_text_to_file(db_name, url, text):
    filename = urlparse(url).path
    if filename.endswith("/"):
        filename = filename[1:-1]
    filename = filename.replace("/", "_") + ".txt"

    dir_path = os.path.join(DATA_DIR, db_name)
    os.makedirs(dir_path, exist_ok=True)

    filepath = os.path.join(dir_path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

def scrape_website(start_url, db_name, max_depth=1):
    if start_url not in visited_urls and max_depth >= 0:
        print(f"[*] Parsing {start_url}")
        visited_urls.add(start_url)
        content = get_page_content(start_url)
        if content:
            soup = BeautifulSoup(content, "lxml")

            for tag_name in ["script", "style", "header", "footer"]:
                for tag in soup(tag_name):
                    tag.decompose()

            text = extract_text_from_html(soup)
            sentences = segment_sentences(text)
            text_to_save = " ".join(sentences)
            save_text_to_file(db_name, start_url, text_to_save)

            for div in soup.find_all("div"):
                for link in div.find_all("a"):
                    href = link.get("href")
                    if href:
                        full_url = urljoin(start_url, href)
                        if is_valid(full_url, start_url):
                            scrape_website(full_url, db_name, max_depth - 1)

def scrape_website_links(links, db_name, max_depth=1):
    start_urls = [url for url in links.split("\n") if url]

    for start_url in start_urls:
        scrape_website(start_url, db_name, max_depth)
