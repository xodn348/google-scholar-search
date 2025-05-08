# Google Scholar Search v1.01

A Python tool to search and analyze Google Scholar articles by keywords, sort by citations, and extract useful information.

---

## Features

- Search Google Scholar for academic papers
- Sort results by citation count
- Extract keywords from abstracts
- Save results to CSV file

---

## Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/xodn348/google-scholar-search.git
    cd google-scholar-search
    ```

2. **Install required packages:**
    ```bash
    pip install serpapi pandas nltk python-dotenv
    ```

---

## Setup

1. **Create a `.env` file with your SerpAPI key and search parameters:**
    ```
    SERPAPI_KEY=your_serpapi_key_here
    ```
2. **Get a SerpAPI key from [https://serpapi.com/](https://serpapi.com/) (free tier available)**

---

## Usage

Run the script:
```bash
python3 serp.py
```

The tool will:
1. Search Google Scholar for your keyword
2. Retrieve up to 100 papers
3. Sort them by citation count
4. Extract keywords from abstracts
5. Save results to a CSV file (e.g., `byzantine_fault_tolerance_papers.csv`)

---

## Required Modules

The script requires these Python modules:
- `serpapi`: For Google Scholar API access
- `pandas`: For data handling and CSV export
- `nltk`: For natural language processing and keyword extraction
- `python-dotenv`: For loading environment variables

---

## Example Output

The CSV output includes:
- Paper title
- Snippet/abstract
- Link to paper
- Citation count
- Extracted keywords

The script also prints the top 10 most frequent keywords in the results.

---

## License

Apache-2.0 License

---

## Author

Junhyuk Lee ([@xodn348](https://github.com/xodn348))
