# Faculty Webpage: Prof. Behrouz Minaei-Bidgoli

Official academic homepage for **Prof. Behrouz Minaei-Bidgoli **, Professor at the **School of Computer Engineering, Iran University of Science and Technology (IUST)**.

**Faculty Domain**: `http://minaei.iust.ac.ir/`

---

## 🏛️ Design & Features

- **Classic Academic Faculty Aesthetic**: Authentic MIT/Stanford/Berkeley CS professor style. Clean serif/sans typography, high information density, paper abstracts, and BibTeX citations.
- **Pure Light Mode**: No dark mode, no glowing neon effects, no AI-agent card styles.
- **Automated Google Scholar Synchronization**:
  - Live metric extraction for **Citations (9,800+)**, **h-index (51)**, and **i10-index (171)**.
  - Automatically fetches publications from Google Scholar profile [`M8tgU-wAAAAJ`](https://scholar.google.com/citations?user=M8tgU-wAAAAJ&hl=en).
  - Includes a zero-dependency Python script (`scripts/sync_scholar.py`) and a GitHub Action workflow (`.github/workflows/scholar-sync.yml`) that runs weekly on cron.
- **Active Advisees & Alumni**: Lists all active Ph.D. candidates and M.Sc. researchers from the laboratory records (`Data Mining Lab.xlsx`) with searchable topic filters.
- **Teaching Syllabi**: Comprehensive course syllabus archives for Doctoral, Master's, and Undergraduate courses at IUST, University of Qom, and Michigan State University.

---

## 📂 Project Structure

```
minaei-faculty/
├── index.html           # Executive profile, bio, live Scholar metric bar, recent papers
├── publications.html    # Chronological publications with search, topic filter, BibTeX modal
├── teaching.html        # Courses taught (Advanced AI, NLP, Mining Massive Datasets, etc.)
├── students.html        # Ph.D. candidates, active M.Sc. advisees (searchable), alumni
├── contact.html         # Office 312 CE building, phone, office hours, campus transit
├── scripts/
│   └── sync_scholar.py  # Zero-dependency Python script to scrape & update Scholar metrics
├── .github/workflows/
│   └── scholar-sync.yml # Weekly GitHub Actions cron workflow to auto-commit fresh stats
├── src/
│   ├── styles/main.css  # Academic typography and Tailwind CSS v4 styling
│   └── data/
│       ├── scholar_stats.json # Live metrics (citations, h-index, i10-index, recent articles)
│       ├── publications.json  # Curated high-impact papers with BibTeX
│       ├── students.json      # Active PhD and MSc advisees
│       └── courses.json       # Course descriptions and syllabi
├── package.json
└── vite.config.js       # Vite multi-page build configuration
```

---

## 🔄 Updating Google Scholar Data

### Option A: Manual One-Line Sync
Run:
```bash
npm run sync:scholar
```
*(Or directly: `python3 scripts/sync_scholar.py`)*

This script connects directly to `https://scholar.google.com/citations?user=M8tgU-wAAAAJ&hl=en`, parses the latest citation metrics and publication table, and writes them into `src/data/scholar_stats.json`.

### Option B: Automated via GitHub Actions
The repository includes `.github/workflows/scholar-sync.yml`. Once pushed to GitHub, GitHub Actions will automatically run every Sunday at midnight, scrape the latest metrics, and commit the updated data directly to the repository!

---

## 🚀 Getting Started

### 1. Installation

```bash
cd minaei-faculty
npm install
```

### 2. Local Development

```bash
npm run dev
```

Open `http://localhost:5173/` in your browser.

### 3. Production Build

```bash
npm run build
```

Compiled static output is saved in `minaei-faculty/dist/`.

---

## 🌐 Deployment to `minaei.iust.ac.ir`

Upload the files from `minaei-faculty/dist/` to the university web hosting server allocated for `minaei.iust.ac.ir`.
