# tests/test_csv_writer.py

from get_papers.csv_writer import write_to_csv
from io import StringIO
import pandas as pd
import sys


def test_write_to_csv_prints_to_stdout(monkeypatch):
    test_data = [
        {
            "PubmedID": "123",
            "Title": "Test Paper",
            "PublicationDate": "2024-01-01",
            "NonAcademicAuthors": "John Doe",
            "CompanyAffiliations": "Pfizer Inc.",
            "CorrespondingEmail": "john@pfizer.com"
        }
    ]

    output = StringIO()
    monkeypatch.setattr(sys, "stdout", output)

    write_to_csv(test_data)
    result = output.getvalue()
    assert "Test Paper" in result
    assert "Pfizer Inc." in result
