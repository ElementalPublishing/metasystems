import requests
from urllib.parse import urlparse
import socket
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast

COMMON_SUBDOMAINS = [
    "www", "blog", "mail", "api", "dev", "test", "shop", "forum", "news", "m"
]

MY_USER_AGENT = "roboter"

class RobotsRules:
    def __init__(self):
        self.disallow = []
        self.allow = []
        self.crawl_delay = None

    def is_path_allowed(self, path):
        # If any Allow matches, it's allowed, unless a more specific Disallow matches
        allowed = False
        for rule in self.allow:
            if path.startswith(rule):
                allowed = True
        for rule in self.disallow:
            if path.startswith(rule):
                allowed = False
        return allowed if self.allow or self.disallow else True

class Roboter:
    def __init__(self, url):
        # Parse the input URL and construct the root domain
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        self.root_domain = parsed.netloc or parsed.path
        self.scheme = parsed.scheme or "https"
        self.root_url = f"{self.scheme}://{self.root_domain}".rstrip("/")
        self.rules = {}
        self.found_subdomains = set()
        self.robots_parsed = {}

    def fetch_robots(self, domain):
        robots_url = f"{self.scheme}://{domain}/robots.txt"
        try:
            response = requests.get(robots_url, timeout=10)
            response.raise_for_status()
            self.rules[domain] = response.text
            self.robots_parsed[domain] = self.parse_robots(response.text)
            return response.text
        except requests.RequestException:
            self.rules[domain] = ""
            self.robots_parsed[domain] = None
            return ""

    def parse_robots(self, robots_txt):
        # Parse robots.txt for our user-agent and *
        if not robots_txt:
            return None
        groups = re.split(r'(?i)^User-agent:', robots_txt, flags=re.MULTILINE)
        relevant = []
        for group in groups:
            lines = group.strip().splitlines()
            if not lines:
                continue
            agent = lines[0].strip().lower()
            if agent == "*" or agent == MY_USER_AGENT.lower():
                relevant.append(lines[1:])
        # Merge all relevant groups
        rules = RobotsRules()
        for lines in relevant:
            for line in lines:
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        rules.disallow.append(path)
                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        rules.allow.append(path)
                elif line.lower().startswith("crawl-delay:"):
                    try:
                        delay = float(line.split(":", 1)[1].strip())
                        rules.crawl_delay = delay
                    except Exception:
                        pass
        return rules

    def find_subdomains(self):
        found = set()
        for sub in COMMON_SUBDOMAINS:
            subdomain = f"{sub}.{self.root_domain}"
            try:
                socket.gethostbyname(subdomain)
                found.add(subdomain)
            except socket.gaierror:
                continue
        self.found_subdomains = found
        return found

    def can_crawl(self, domain, path="/"):
        rules = self.robots_parsed.get(domain)
        if not rules:
            return True  # No robots.txt, so allowed
        return rules.is_path_allowed(path)

    def get_crawl_delay(self, domain):
        rules = self.robots_parsed.get(domain)
        if rules and rules.crawl_delay is not None:
            return rules.crawl_delay
        return 0

    def print_rules(self):
        start_time = time.time()
        # 1. Always check the root domain FIRST
        robots_txt = self.fetch_robots(self.root_domain)
        if not self.can_crawl(self.root_domain, "/"):
            print(f"\nCrawling is disallowed for user-agent '{MY_USER_AGENT}' or all bots on {self.root_domain}. Aborting.")
            print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
            return

        crawl_delay = self.get_crawl_delay(self.root_domain)
        if crawl_delay:
            print(f"Crawl-delay for {self.root_domain}: {crawl_delay} seconds")
            print(f"Respecting crawl-delay: Waiting {crawl_delay} seconds before continuing...")
            time.sleep(crawl_delay)

        # 2. Only after root, check discovered subdomains in parallel
        subdomains = self.find_subdomains()

        def process_sub(sub):
            robots_txt_sub = self.fetch_robots(sub)
            if not self.can_crawl(sub, "/"):
                print(f"\nCrawling is disallowed for user-agent '{MY_USER_AGENT}' or all bots on {sub}. Skipping.")
                return
            sub_crawl_delay = self.get_crawl_delay(sub)
            if sub_crawl_delay:
                print(f"Crawl-delay for {sub}: {sub_crawl_delay} seconds")
                print(f"Respecting crawl-delay: Waiting {sub_crawl_delay} seconds before continuing...")
                time.sleep(sub_crawl_delay)

        if subdomains:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(process_sub, sub) for sub in sorted(subdomains)]
                for future in as_completed(futures):
                    pass  # Output is handled in process_sub

        self.write_markdown()
        elapsed = time.time() - start_time
        print(f"\nTime elapsed: {elapsed:.2f} seconds")

    def write_markdown(self):
        filename = f"{self.root_domain.replace('.', '_')}_robots.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# robots.txt Results for {self.root_domain}\n\n")
            f.write(f"## Root Domain: {self.root_domain}\n")
            if self.rules[self.root_domain]:
                f.write(f"### robots.txt\n```\n{self.rules[self.root_domain]}\n```\n")
            else:
                f.write("No robots.txt found for root domain.\n")
            if self.found_subdomains:
                f.write("\n## Subdomains Found:\n")
                for sub in sorted(self.found_subdomains):
                    f.write(f"\n### {sub}\n")
                    if self.rules[sub]:
                        f.write(f"```\n{self.rules[sub]}\n```\n")
                    else:
                        f.write("No robots.txt found.\n")
            else:
                f.write("\nNo common subdomains found.\n")
        print(f"\nResults written to {filename}")

    def analyze_outputs(filepath):
        outputs = []
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
        for node in ast.walk(tree):
            # Detect file writes
            if isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id == 'open':
                if len(node.args) >= 2 and hasattr(node.args[1], 's'):
                    mode = node.args[1].s
                    if 'w' in mode:
                        if hasattr(node.args[0], 's'):
                            outputs.append({
                                "type": "file",
                                "filename": node.args[0].s,
                                "mode": mode,
                                "description": "File written by program"
                            })
            # Detect print statements
            if isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id == 'print':
                outputs.append({
                    "type": "console",
                    "description": "Prints output to the terminal"
                })
        return outputs

def main(*args):
    """
    Entry point for roboter as a meta system.
    Usage: main(url)
    Example: main("example.com")
    """
    if not args:
        print("Usage: roboter <website_url>")
        return
    url = args[0]
    roboter = Roboter(url)
    roboter.print_rules()

if __name__ == "__main__":
    print("NOTICE: This tool checks robots.txt and will not crawl if your user-agent or all bots are disallowed.")
    print("It also respects crawl-delay and path rules. You are responsible for complying with all applicable laws and the website's Terms of Service.\n")
    url = input("Enter a website URL (any page or domain): ").strip()
    roboter = Roboter(url)
    roboter.print_rules()
    input("\nPress Enter to exit...")