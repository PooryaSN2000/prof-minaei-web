#!/usr/bin/env python3
"""
sync_scholar.py
Full Crawler for Prof. Behrouz Minaei-Bidgoli's Google Scholar Profile:
https://scholar.google.com/citations?user=M8tgU-wAAAAJ&hl=en

Crawls:
- Complete list of publications (460+ articles) sorted by pubdate
- Exact annual citation counts (2005-2026) for interactive charting
- Overall bibliometric indicators (Citations, h-index, i10-index)
- Semantic topical categorization for filtering
- Auto-generates clean BibTeX entries
"""

import os
import json
import urllib.request
import re
import html
import time
from datetime import datetime, timezone

SCHOLAR_ID = "M8tgU-wAAAAJ"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

TRANS_MAP = {
    "\u0631\u0646\u0647 \u0633\u0648\u062f\u0631\u0641 \u06cc\u0645\u0644\u0639 \u06c0\u0645\u0627\u0646\u0644\u0635\u0641": "Ferdows Art Academic Journal",
}

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    cleaned = html.unescape(text).strip()
    for fa, en in TRANS_MAP.items():
        cleaned = cleaned.replace(fa, en)
    return cleaned

def categorize_publication(title, venue):
    text = f"{title} {venue}".lower()
    
    # 1. NLP & LLMs
    if any(k in text for k in [
        'rag', 'llm', 'large language model', 'language model', 'question answering',
        'qa', 'sentiment', 'aspect-based', 'retrieval-augmented', 'embedding',
        'sentence embedding', 'transformer', 'bert', 'gpt', 'token', 'corpus',
        'arabic', 'persian', 'farsi', 'hadith', 'morphological', 'stemming',
        'nlp', 'natural language', 'text classification', 'parsing', 'translation',
        'summarization', 'speech recognition', 'dialogue', 'argumentation'
    ]):
        return "NLP & Large Language Models"
        
    # 2. Knowledge Graphs & Semantic Web
    if any(k in text for k in [
        'knowledge graph', 'knowledge base', 'farsbase', 'ontology', 'semantic web',
        'link prediction', 'triple', 'rdf', 'sparql', 'dbpedia', 'wikidata',
        'entity alignment', 'entity linking', 'relation extraction', 'graphrag',
        'concept net', 'description logic'
    ]):
        return "Knowledge Graphs & Semantic Web"

    # 3. Computer Games & Interactive Media
    if any(k in text for k in [
        'game', 'gaming', 'player', 'npc', 'gameplay', 'serious game',
        'interactive entertainment', 'virtual reality', 'video game', 'arcade'
    ]):
        return "Computer Games & Interactive Entertainment"

    # 4. Educational Data Mining
    if any(k in text for k in [
        'educational', 'lon-capa', 'learning analytics', 'e-learning', 'online learning',
        'student performance', 'course management', 'pedagogical', 'tutor'
    ]):
        return "Educational Data Mining & Learning Analytics"

    # 5. Recommender Systems & Data Mining
    if any(k in text for k in [
        'recommender', 'recommendation', 'collaborative filtering', 'clustering',
        'cluster ensemble', 'association rule', 'data mining', 'stream mining',
        'anomaly detection', 'knn', 'nearest neighbor', 'bipartite', 'feature selection',
        'churn', 'fraud detection', 'customer'
    ]):
        return "Recommender Systems & Data Mining"

    return "Artificial Intelligence & Software Engineering"

def generate_bibtex(title, authors_str, venue, year, scholar_link):
    first_author_last = "paper"
    if authors_str:
        first_author = authors_str.split(",")[0].strip()
        parts = first_author.split()
        first_author_last = parts[-1].lower() if parts else "paper"
    first_author_last = re.sub(r'[^a-zA-Z0-9]', '', first_author_last)
    
    first_word_title = "study"
    title_words = re.findall(r'[a-zA-Z0-9]+', title)
    if title_words:
        first_word_title = title_words[0].lower()
    
    y = str(year) if year else "2025"
    key = f"minaei{y}{first_author_last}_{first_word_title}"
    
    bib_authors = " and ".join([a.strip() for a in authors_str.split(",") if a.strip()]) if authors_str else "Minaei-Bidgoli, Behrouz"

    bib = [
        f"@article{{{key},",
        f"  title = {{{{{title}}}}},",
        f"  author = {{{bib_authors}}},",
    ]
    if venue:
        bib.append(f"  journal = {{{venue}}},")
    if year:
        bib.append(f"  year = {{{year}}},")
    if scholar_link:
        bib.append(f"  url = {{{scholar_link}}},")
    bib.append("}")
    return "\n".join(bib)

def fetch_page(cstart=0, pagesize=100, sortby="pubdate"):
    url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&cstart={cstart}&pagesize={pagesize}&sortby={sortby}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode('utf-8', errors='replace')

def sync():
    print(f"📡 Initiating comprehensive crawl of Google Scholar profile: {SCHOLAR_ID}...")
    
    # 1. Fetch first page (0-100)
    try:
        html_p1 = fetch_page(cstart=0, pagesize=100, sortby="pubdate")
    except Exception as e:
        print(f"❌ Failed to fetch page 1: {e}")
        return False

    # Extract Citation Metrics Table
    stats = {}
    table_match = re.search(r'<table id="gsc_rsb_st"[^>]*>(.*?)</table>', html_p1, re.DOTALL)
    if table_match:
        table_html = table_match.group(1)
        cells = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', table_html)
        if len(cells) >= 6:
            stats = {
                "citations": {"all": int(cells[0]), "since_recent": int(cells[1])},
                "h_index": {"all": int(cells[2]), "since_recent": int(cells[3])},
                "i10_index": {"all": int(cells[4]), "since_recent": int(cells[5])}
            }

    # Extract Citations per year history
    years = re.findall(r'<span class="gsc_g_t"[^>]*>(\d{4})</span>', html_p1)
    counts = re.findall(r'<span class="gsc_g_al"[^>]*>(\d+)</span>', html_p1)
    history = []
    for y, c in zip(years, counts):
        history.append({"year": int(y), "citations": int(c)})
    stats["history"] = history
    stats["last_synced"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    stats["scholar_url"] = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"

    print(f"📊 Citations: {stats.get('citations', {}).get('all')} | h-index: {stats.get('h_index', {}).get('all')} | i10-index: {stats.get('i10_index', {}).get('all')}")
    print(f"📈 Extracted {len(history)} years of citation history ({history[0]['year']} to {history[-1]['year']})")

    # 2. Paginate all publications until exhaustion
    all_rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', html_p1, re.DOTALL)
    print(f"   Batch 1 (0-100): {len(all_rows)} rows")

    cstart = 100
    while True:
        time.sleep(1)
        try:
            p_html = fetch_page(cstart=cstart, pagesize=100, sortby="pubdate")
            rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', p_html, re.DOTALL)
            print(f"   Batch ({cstart}-{cstart+100}): {len(rows)} rows")
            if not rows:
                break
            all_rows.extend(rows)
            if len(rows) < 100:
                break
            cstart += 100
        except Exception as e:
            print(f"   ⚠️ Error at cstart={cstart}: {e}")
            break

    print(f"📚 Total rows harvested: {len(all_rows)}")

    # 3. Parse and structure publications
    parsed_publications = []
    seen_titles = set()

    for idx, r in enumerate(all_rows, start=1):
        title_m = re.search(r'<a href="([^"]*)" class="gsc_a_at">([^<]+)</a>', r)
        gray_divs = re.findall(r'<div class="gs_gray">(.*?)</div>', r, re.DOTALL)
        cite_m = re.search(r'<a href="([^"]*)" class="gsc_a_ac[^"]*">(\d+)</a>', r)
        year_m = re.search(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(\d{4})</span>', r)

        if not title_m:
            continue

        raw_link = html.unescape(title_m.group(1))
        title = clean_html(title_m.group(2))
        
        title_norm = re.sub(r'\s+', ' ', title.lower().strip())
        if title_norm in seen_titles:
            continue
        seen_titles.add(title_norm)

        scholar_link = f"https://scholar.google.com{raw_link}" if raw_link.startswith("/") else raw_link
        
        authors_raw = gray_divs[0] if len(gray_divs) > 0 else ""
        authors = clean_html(authors_raw)
        
        venue_raw = gray_divs[1] if len(gray_divs) > 1 else ""
        venue = clean_html(venue_raw)
        
        citations = int(cite_m.group(2)) if cite_m else 0
        citations_link = ""
        if cite_m and cite_m.group(1):
            clink = html.unescape(cite_m.group(1))
            citations_link = f"https://scholar.google.com{clink}" if clink.startswith("/") else clink

        year = int(year_m.group(1)) if year_m and year_m.group(1) else None

        category = categorize_publication(title, venue)
        bibtex = generate_bibtex(title, authors, venue, year, scholar_link)

        parsed_publications.append({
            "id": f"pub-{idx:03d}",
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "category": category,
            "citations": citations,
            "scholar_link": scholar_link,
            "citations_link": citations_link,
            "bibtex": bibtex
        })

    stats["total_publications"] = len(parsed_publications)

    # 4. Save to files in local repo and sibling project if present
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_repo_dir = os.path.dirname(script_dir)
    parent_dir = os.path.dirname(current_repo_dir)

    target_dirs = [
        os.path.join(current_repo_dir, "src", "data"),
        os.path.join(parent_dir, "minaei-faculty", "src", "data"),
        os.path.join(parent_dir, "dml-lab", "src", "data")
    ]
    seen_dirs = set()
    destinations = []
    for td in target_dirs:
        norm = os.path.normpath(td)
        if os.path.exists(norm) and norm not in seen_dirs:
            seen_dirs.add(norm)
            destinations.append(norm)

    for d in destinations:
        if not os.path.exists(d):
            continue
        pubs_path = os.path.join(d, "publications.json")
        stats_path = os.path.join(d, "scholar_stats.json")
        
        with open(pubs_path, "w", encoding="utf-8") as f:
            json.dump(parsed_publications, f, ensure_ascii=False, indent=2)
            
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
            
        print(f"✅ Saved {pubs_path} ({len(parsed_publications)} categorized articles)")
        print(f"✅ Saved {stats_path}")

    # Category Breakdown
    cat_counts = {}
    for p in parsed_publications:
        c = p["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1
    print("\n📂 Category Breakdown:")
    for c, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"   - {c}: {cnt} papers")

    return True

if __name__ == "__main__":
    sync()
