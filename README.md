# 🧬 PubMed-Based Assignment – `get-papers`

A command-line Python tool to fetch and filter research papers from PubMed, identifying papers with at least one **non-academic author** affiliated with a **pharmaceutical or biotech company**.

---

## 📂 Project Structure

```
get-papers/
├── get_papers/
│   ├── pubmed_client.py       # Handles PubMed API calls
│   ├── paper_filter.py        # Filters for non-academic authors
│   ├── csv_writer.py          # Outputs CSV results
│   └── __init__.py
├── cli.py                     # CLI entrypoint using Typer
├── tests/                     # Unit tests for all modules
├── README.md
└── requirements.txt           # Python dependencies
```

---

## ⚙️ Setup Instructions

> 📌 You do **not** need Poetry. Just use Python + venv.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd get-papers
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the CLI with a PubMed query:

```bash
python cli.py "cancer immunotherapy"
```

To save results to a CSV:

```bash
python cli.py "covid vaccine response" --file results.csv
```

With debug output:

```bash
python cli.py "AI in drug discovery" --debug
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests
```

---

## 🧠 How It Works

- Fetches articles from PubMed via `eutils` API.
- Parses authors and affiliations.
- Applies heuristics to filter non-academic authors:
  - Excludes terms like "university", "hospital", etc.
  - Includes keywords like "Inc", "Biotech", "LLC", etc.
- Outputs matching papers and authors to a CSV or console.

---

## 🧰 Libraries Used

- [`requests`](https://docs.python-requests.org/)
- [`typer`](https://typer.tiangolo.com/)
- [`pandas`](https://pandas.pydata.org/)
- [`lxml`](https://lxml.de/)
- [`pytest`](https://docs.pytest.org/) (for testing)

---

## 📌 Notes

- Make sure your internet connection is stable while using the PubMed API.
- You may need to increase `retmax` in the API client for larger result sets.

---

## 📧 Author

Your Name — [shefali.jain1311@gmail.com](mailto:shefali.jain1311@gmail.com)