# get_papers/paper_filter.py

from typing import List, Dict, Tuple
import re


NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "inc", "corp", "ltd", "gmbh", "llc", "therapeutics", "laboratories", "research center"
]

ACADEMIC_KEYWORDS = [
    "university", "college", "hospital", "institute", "centre", "center", "faculty", "school", "department"
]


def is_non_academic(affiliation: str) -> bool:
    """Heuristic to detect non-academic affiliation."""
    affil_lower = affiliation.lower()

    # Return False if it contains academic keywords
    if any(keyword in affil_lower for keyword in ACADEMIC_KEYWORDS):
        return False

    # Return True if it contains non-academic / industry keywords
    return any(keyword in affil_lower for keyword in NON_ACADEMIC_KEYWORDS)


def filter_papers(papers: List[Dict]) -> List[Dict]:
    """Filter papers that have at least one non-academic author."""
    filtered = []
    for paper in papers:
        non_academic_authors = []
        company_affiliations = []

        for author in paper.get("Authors", []):
            affil = author.get("affiliation") or ""
            if is_non_academic(affil):
                non_academic_authors.append(author["name"])
                company_affiliations.append(affil)

        if non_academic_authors:
            # Add to paper info
            filtered.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "PublicationDate": paper["PublicationDate"],
                "NonAcademicAuthors": "; ".join(non_academic_authors),
                "CompanyAffiliations": "; ".join(company_affiliations),
                "CorrespondingEmail": find_corresponding_email(paper.get("Authors", [])),
            })

    return filtered


def find_corresponding_email(authors: List[Dict]) -> str:
    """Return the first email found among authors."""
    for author in authors:
        email = author.get("email")
        if email:
            return email
    return ""
