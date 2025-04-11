# tests/test_paper_filter.py

from get_papers.paper_filter import is_non_academic, filter_papers


def test_is_non_academic_true():
    affil = "Pfizer Inc. Research Division"
    assert is_non_academic(affil) is True


def test_is_non_academic_false():
    affil = "Department of Biology, Stanford University"
    assert is_non_academic(affil) is False


def test_filter_papers_extracts_company_authors():
    fake_paper = {
        "PubmedID": "123456",
        "Title": "Cool Biotech Paper",
        "PublicationDate": "2024-01-01",
        "Authors": [
            {"name": "John Doe", "affiliation": "Biogen Inc.", "email": "john@biogen.com"},
            {"name": "Jane Smith", "affiliation": "Harvard University", "email": "jane@harvard.edu"},
        ],
    }

    results = filter_papers([fake_paper])
    assert len(results) == 1
    assert "Biogen Inc." in results[0]["CompanyAffiliations"]
    assert "John Doe" in results[0]["NonAcademicAuthors"]
    assert results[0]["CorrespondingEmail"] == "john@biogen.com"
