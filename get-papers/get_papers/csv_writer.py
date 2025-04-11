# get_papers/csv_writer.py

from typing import List, Dict, Optional
import pandas as pd
import sys


def write_to_csv(data: List[Dict], filename: Optional[str] = None) -> None:
    """Write the list of paper dictionaries to CSV. If no filename is given, print to stdout."""
    df = pd.DataFrame(data)

    # Ensure all required columns exist
    columns = [
        "PubmedID",
        "Title",
        "PublicationDate",
        "NonAcademicAuthors",
        "CompanyAffiliations",
        "CorrespondingEmail"
    ]

    # Fill missing columns with empty strings
    for col in columns:
        if col not in df.columns:
            df[col] = ""

    if filename:
        df.to_csv(filename, index=False)
        print(f"✅ CSV written to {filename}")
    else:
        df.to_csv(sys.stdout, index=False)
