from bs4 import BeautifulSoup
import re
from collections import Counter

def extract_keywords(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    text = soup.get_text()
    words = re.findall(r'\b[A-Za-z]{3,}\b', text)

    links = [a.get('href', '') for a in soup.find_all('a')]
    link_text = " ".join(links).lower()

    scored = Counter()
    for w in words:
        weight = 2 if w.lower() in link_text else 1
        scored[w] += weight

    top5 = [w for w, _ in scored.most_common(5)]
    return top5

def keyword_url_match_score(keywords, domain):
    domain_lower = domain.lower()
    matches = sum(1 for k in keywords if k.lower() in domain_lower)
    return matches / max(len(keywords), 1)