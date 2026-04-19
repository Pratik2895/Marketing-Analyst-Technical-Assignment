# 📊 Multi-Channel Marketing Analytics

> **Analytics engineering project** — unified KPI model across Facebook, Google Ads, and TikTok with built-in data-quality checks and an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)

🔗 **Portfolio case study →** https://pratik2895.github.io/projects/marketing-analytics/

---

## 🎯 The problem

Marketing teams running campaigns across **Facebook, Google Ads, and TikTok** get three different schemas, three different KPI definitions, and three different timezone conventions. Comparing cross-channel performance in that state is guesswork.

## 🧱 The solution

An analytics-engineering layer that standardizes the three platforms into **one model** with a dashboard on top.

```
 ┌──────────┐
 │ FB Ads   │─┐
 ├──────────┤ │   ┌──────────────┐   ┌──────────────┐
 │ Google   │─┼──▶│  Unified     │──▶│   Streamlit  │
 │  Ads     │ │   │  KPI Model   │   │  + Plotly    │
 ├──────────┤ │   │  (pandas)    │   │  dashboard   │
 │ TikTok   │─┘   └──────┬───────┘   └──────────────┘
 └──────────┘          QC checks
                       (validate vs CSV)
```

---

## 📐 KPIs computed

Consistent formulas across all three channels — documented in [`src/kpis.py`](./src/kpis.py):

| KPI | Formula | Why |
|---|---|---|
| **CTR** | clicks / impressions | creative effectiveness |
| **CPC** | spend / clicks | cost per interaction |
| **CPA** | spend / conversions | cost per outcome |
| **ROAS** | revenue / spend | return on ad spend |
| **CPM** | (spend / impressions) × 1000 | reach efficiency |

---

## ✅ Data quality

The dedicated [`qc.py`](./qc.py) script validates every number shown in the dashboard against the source CSVs. Mismatch → fail loud. Real analytics engineering is about **trust**, not just SQL.

```bash
python qc.py
# ✓ FB revenue matches source (3,412,809.42)
# ✓ Google conversions match source (48,201)
# ✗ TikTok CPA drift: 0.03% (above 0.01% tolerance)
```

---

## 🚀 Run it

```bash
# 1. Clone
git clone https://github.com/Pratik2895/Marketing-Analyst-Technical-Assignment
cd Marketing-Analyst-Technical-Assignment

# 2. Install
pip install -r requirements.txt

# 3. Validate data
python qc.py

# 4. Launch the dashboard
streamlit run app.py
# → http://localhost:8501
```

Deploy to Streamlit Cloud: push to GitHub → connect the repo → deploy. No extra config.

---

## 🧭 Repo structure

```
.
├── app.py                # Streamlit dashboard entry
├── qc.py                 # Data-quality validation script
├── src/
│   ├── loaders/          # Channel-specific loaders (FB, Google, TikTok)
│   ├── unified.py        # Standardized cross-channel model
│   ├── kpis.py           # KPI formulas (CTR, CPC, CPA, ROAS, CPM)
│   └── viz/              # Plotly chart builders
├── data/                 # Sample CSVs
└── requirements.txt
```

---

## 🧠 Why this project matters

Shows the **analytics-engineer** half of my title: business-facing metrics with defensible definitions, not just pipelines moving bytes. The QC script is the tell — real analytics engineering is as much about **trust** as it is about SQL.

---

## 📫 Contact

**Pratik Bhikadiya** · Data & Analytics Engineer
[Portfolio](https://pratik2895.github.io) · [LinkedIn](https://www.linkedin.com/in/pratikbhikadiya/) · bhikadi@uwindsor.ca
