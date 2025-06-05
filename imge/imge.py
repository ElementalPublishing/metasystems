import requests
from bs4 import BeautifulSoup

class WebMetaExtractor:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None

    def fetch(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self.html = response.text
        self.soup = BeautifulSoup(self.html, "html.parser")

    def extract_images(self):
        if not self.soup:
            self.fetch()
        images = []
        for img in self.soup.find_all("img"):
            src = img.get("src")
            alt = img.get("alt", "")
            images.append({"src": src, "alt": alt})
        return images

    def extract_metadata(self):
        if not self.soup:
            self.fetch()
        metadata = {}
        # Standard meta tags
        for meta in self.soup.find_all("meta"):
            name = meta.get("name") or meta.get("property")
            content = meta.get("content")
            if name and content:
                metadata[name] = content
        # Title
        title_tag = self.soup.find("title")
        if title_tag:
            metadata["title"] = title_tag.text
        return metadata

if __name__ == "__main__":
    url = input("Enter a website URL: ")
    extractor = WebMetaExtractor(url)
    extractor.fetch()
    print("\nImages found:")
    for img in extractor.extract_images():
        print(f" - src: {img['src']}, alt: {img['alt']}")
    print("\nMetadata found:")
    for k, v in extractor.extract_metadata().items():
        print(f" - {k}: {v}")

    input("\nPress Enter to exit...")