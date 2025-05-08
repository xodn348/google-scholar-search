"""
Google Scholar Search
---------------------
A Python tool to search and analyze Google Scholar articles.

Copyright 2024 Junhyuk Lee (@xodn348)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import ssl
import os
from serpapi import GoogleSearch
import pandas as pd
import nltk
import time
import string
from dotenv import load_dotenv  # python-dotenv 라이브러리 추가

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 가져오기
api_key = os.getenv("SERPAPI_KEY")

# Handle SSL certificate verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Set NLTK data path if needed
nltk_data_dir = os.path.expanduser('~/nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download NLTK data with explicit force=True to ensure download
print("Downloading NLTK resources...")
nltk.download('punkt', download_dir=nltk_data_dir, force=True)
nltk.download('stopwords', download_dir=nltk_data_dir, force=True)

# Import these after downloads to avoid errors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Set search keyword
search_keyword = "Byzantine Fault Tolerance"

# Initialize results storage
all_papers = []

# Paginate through more pages to get up to 100 papers
for start in range(0, 200, 20):  # Increased range to get more papers
    params = {
        "engine": "google_scholar",
        "q": search_keyword,
        "api_key": api_key,
        "hl": "en",
        "as_ylo": "2021",
        "as_yhi": "2024",
        "num": "100",
        "start": start,
        "scisbd": "0"  # Sort by citation count (0 = relevance by default, but with more results we'll get high-citation papers)
    }

    # Execute search with retry
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        all_papers.extend(organic_results)
        print(f"Found {len(organic_results)} papers on page {start//20 + 1}, total: {len(all_papers)}")
        if len(all_papers) >= 100:  # Stop after collecting 100 papers
            all_papers = all_papers[:100]
            break
    except Exception as e:
        print(f"Error at start={start}: {e}")
        time.sleep(5)
        continue
    time.sleep(2)  # Avoid rate limits

# Citation 순으로 정렬
all_papers.sort(key=lambda x: x.get("inline_links", {}).get("cited_by", {}).get("total", 0), reverse=True)

# Keyword extraction function - simplified to avoid punkt_tab dependency
def extract_keywords(text):
    try:
        stop_words = set(stopwords.words('english'))
        # Simple tokenization as fallback if word_tokenize fails
        try:
            words = word_tokenize(text.lower())
        except:
            # Fallback to simple tokenization
            words = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
        keywords = [word for word in words if word.isalnum() and word not in stop_words]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# Prepare data for CSV
data = []
for result in all_papers:
    snippet = result.get("snippet", "No snippet available")
    keywords = extract_keywords(snippet)
    data.append({
        "Title": result.get("title", "No title"),
        "Snippet": snippet,
        "Link": result.get("link", "No link"),
        "Cites_by": result.get("inline_links", {}).get("cited_by", {}).get("total", 0),
        "Keywords": ", ".join(keywords)
    })

# Save to CSV with keyword in filename
keyword_filename = search_keyword.lower().replace(" ", "_")
csv_filename = f"{keyword_filename}_papers.csv"
df = pd.DataFrame(data)
df.to_csv(csv_filename, index=False)
print(f"Results saved to {csv_filename}")

# Print keyword frequency
from collections import Counter
all_keywords = [kw for keywords in df["Keywords"].str.split(", ") for kw in keywords if kw]
keyword_counts = Counter(all_keywords)
print("Top 10 Keywords:", keyword_counts.most_common(10))
