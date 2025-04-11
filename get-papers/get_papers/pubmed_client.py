# get_papers/pubmed_client.py

from typing import List, Dict, Optional
import requests
from xml.etree import ElementTree as ET


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EMAIL = "your-email@example.com"  # Replace with a real email if needed


def fetch_pubmed_ids(query: str, retmax: int = 100) -> List[str]:
    """Fetch PubMed IDs matching the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "email": EMAIL,
    }
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch full details for a list of PubMed IDs."""
    if not pubmed_ids:
        return []

    ids = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml",
        "email": EMAIL,
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper = {
            "PubmedID": article.findtext(".//PMID"),
            "Title": article.findtext(".//ArticleTitle"),
            "PublicationDate": extract_pub_date(article),
            "Authors": extract_authors(article),
        }
        papers.append(paper)

    return papers


def extract_pub_date(article: ET.Element) -> Optional[str]:
    """Extract publication date from XML."""
    date_elem = article.find(".//PubDate")
    if date_elem is not None:
        year = date_elem.findtext("Year") or ""
        month = date_elem.findtext("Month") or ""
        day = date_elem.findtext("Day") or ""
        return f"{year}-{month}-{day}".strip("-")
    return None


def extract_authors(article: ET.Element) -> List[Dict]:
    """Extract author info (name, affiliation, email)."""
    authors = []
    for author in article.findall(".//Author"):
        name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
        affil = author.findtext(".//AffiliationInfo/Affiliation")
        email = extract_email(affil)
        authors.append({"name": name, "affiliation": affil, "email": email})
    return authors


def extract_email(affiliation: Optional[str]) -> Optional[str]:
    """Try to extract email address from affiliation."""
    if affiliation and "@" in affiliation:
        parts = affiliation.split()
        for part in parts:
            if "@" in part and "." in part:
                return part.strip(";.,()")
    return None