# Marketing Analytics Dashboard

A cross-channel marketing analytics dashboard that unifies and visualizes advertising data from Facebook, Google, and TikTok platforms.

## Overview

This project is a technical assignment for a Senior Marketing Analyst position, demonstrating the ability to:
- Unify multi-channel advertising data into a single data model
- Create interactive visualizations for cross-channel performance analysis
- Generate actionable insights and recommendations

## Dashboard Preview

The dashboard provides:
- **Key Performance Indicators**: Total spend, impressions, clicks, conversions, revenue
- **Platform Comparison**: Spend and conversions by platform (Facebook, Google, TikTok)
- **Trend Analysis**: Daily spend and conversion trends over time
- **Campaign Analysis**: Top performers, ROAS vs Spend analysis
- **Cost Efficiency**: CPA analysis and click distribution
- **Auto-generated Insights & Recommendations**

## Data Sources

The dashboard integrates data from three advertising platforms:
- `01_facebook_ads.csv` - Facebook advertising metrics
- `02_google_ads.csv` - Google Ads campaign data
- `03_tiktok_ads.csv` - TikTok advertising engagement

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/Pratik2895/Marketing-Analyst-Technical-Assignment.git
cd Marketing-Analyst-Technical-Assignment
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
Marketing-Analyst-Technical-Assignment/
├── app.py                    # Streamlit dashboard application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── 01_facebook_ads.csv       # Facebook Ads data
├── 02_google_ads.csv         # Google Ads data
└── 03_tiktok_ads.csv        # TikTok Ads data
```

## Features

### Key Metrics
| Metric | Description |
|--------|-------------|
| Total Spend | Combined ad spend across all platforms |
| Total Impressions | Number of times ads were displayed |
| Total Clicks | Number of ad clicks |
| Total Conversions | Number of conversions attributed to ads |
| Total Revenue | Estimated revenue from conversions |

### Calculated Metrics
| Metric | Formula |
|--------|---------|
| CTR (Click-Through Rate) | (Clicks / Impressions) × 100 |
| CPC (Cost Per Click) | Spend / Clicks |
| CPA (Cost Per Acquisition) | Spend / Conversions |
| ROAS (Return on Ad Spend) | Revenue / Spend |
| CPM (Cost Per Mille) | (Spend / Impressions) × 1000 |

### Unified Data Model

The dashboard creates a unified data model with standardized columns:
- `date` - Campaign date
- `platform` - Advertising platform (Facebook/Google/TikTok)
- `campaign_id` - Unique campaign identifier
- `campaign_name` - Campaign name
- `impressions` - Number of impressions
- `clicks` - Number of clicks
- `cost` - Ad spend
- `conversions` - Number of conversions
- `ctr` - Click-through rate
- `conversion_value` - Revenue from conversions

## Dashboard Widgets

### 1. KPI Cards
- Total Spend, Impressions, Clicks, Conversions, Revenue
- Average CTR, CPC, CPA, ROAS

### 2. Platform Performance
- Bar charts comparing spend and conversions by platform
- Metrics summary table with platform-level KPIs

### 3. Trend Analysis
- Daily spend trends by platform
- Daily conversion trends by platform

### 4. Campaign Analysis
- Top 10 campaigns by conversions
- ROAS vs Spend scatter plot
- Full campaign performance table

### 5. Cost Efficiency
- CPA vs Total Spend analysis
- Click distribution by platform (pie chart)

### 6. Insights & Recommendations
- Auto-generated insights based on data analysis
- Actionable recommendations for budget optimization

## Data Export

The dashboard allows exporting:
- Unified marketing data (CSV)
- Platform metrics summary (CSV)
- Campaign metrics summary (CSV)

## Live Demo

[View the live dashboard on Streamlit Cloud](https://marketing-analyst-technical-assignment.streamlit.app)

*Note: Link will be active after deployment*

## Technologies Used

- **Python 3.8+** - Programming language
- **Streamlit** - Dashboard framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **SQLite** - Data storage

## Deployment on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository
6. Set the main file path to `app.py`
7. Click "Deploy"

## Author

**Pratik**

## License

This project is created for educational purposes as part of a technical assignment.