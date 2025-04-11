# tests/test_pubmed_client.py

from get_papers import pubmed_client
import pytest
from unittest.mock import patch, Mock


@patch("get_papers.pubmed_client.requests.get")
def test_fetch_pubmed_ids(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "esearchresult": {"idlist": ["12345", "67890"]}
    }
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    result = pubmed_client.fetch_pubmed_ids("cancer")
    assert result == ["12345", "67890"]
    mock_get.assert_called_once()


@patch("get_papers.pubmed_client.requests.get")
def test_fetch_details(mock_get):
    xml_response = """
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <PMID>12345</PMID>
          <Article>
            <ArticleTitle>Sample Title</ArticleTitle>
            <Journal>
              <JournalIssue>
                <PubDate>
                  <Year>2024</Year><Month>03</Month><Day>01</Day>
                </PubDate>
              </JournalIssue>
            </Journal>
            <AuthorList>
              <Author>
                <LastName>Doe</LastName>
                <ForeName>John</ForeName>
                <AffiliationInfo>
                  <Affiliation>Biogen Inc. john@biogen.com</Affiliation>
                </AffiliationInfo>
              </Author>
            </AuthorList>
          </Article>
        </MedlineCitation>
      </PubmedArticle>
    </PubmedArticleSet>
    """
    mock_response = Mock()
    mock_response.text = xml_response
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    result = pubmed_client.fetch_details(["12345"])
    assert len(result) == 1
    assert result[0]["PubmedID"] == "12345"
    assert result[0]["Title"] == "Sample Title"
    assert result[0]["PublicationDate"] == "2024-03-01"
    assert result[0]["Authors"][0]["name"] == "John Doe"
    assert result[0]["Authors"][0]["email"] == "john@biogen.com"
