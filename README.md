# 🥛 Amul Focus Product Sales Conversion Dashboard

> An outlet-level FMCG field sales intelligence system for tracking coverage, conversion, objections, and follow-up actions across Amul focus products.

## 🎯 What This Solves

Given daily outlet visits for selected Amul focus products, this dashboard answers:

- **Which products convert best?** — Product-wise pitch-to-order conversion rates
- **Which outlets respond best?** — Outlet type and individual outlet performance
- **What blocks conversion?** — Objection patterns, competitor presence, execution gaps
- **Where should follow-up go?** — Prioritized action items based on field signals
- **What needs better execution?** — Visibility, availability, scheme communication analysis

## 📦 Focus Products

| Product | Group | Storage |
|---------|-------|---------|
| More Tin Paneer | Dairy | Chilled |
| Amul Aata | Staples | Ambient |
| Amul Cookies | Snacks | Ambient |
| Amul Chocolates | Confectionery | Ambient |
| Organic Kabuli Chana | Organics | Ambient |
| Organic Toor Dal | Organics | Ambient |
| Organic Masoor Dal | Organics | Ambient |
| Organic Rajma | Organics | Ambient |

## 📊 Dashboard Pages

### 1. Executive Overview
KPI cards, daily trends, product/outlet type conversion, objection distribution

### 2. Product Intelligence
Product performance table, conversion bars, product×objection heatmap, product-outlet fit matrix

### 3. Outlet Intelligence
Outlet scatter plots, outlet type comparison, opportunity outlets, range selling analysis

### 4. Execution Quality
Sales funnel (visit→pitch→interest→order), conversion by visibility/scheme/availability

### 5. Follow-up Planner
AI-powered recommendations with 12 FMCG-specific rules, prioritized action table

### 6. AI Summary
Gemini-powered or template-based weekly performance narrative

## 🏗️ Tech Stack

- **Python** 3.9+
- **Streamlit** — dashboard framework
- **Pandas** — data processing
- **Plotly** — interactive charts
- **Google Gemini API** — AI summaries (optional)

## 🚀 Setup

```bash
# Clone/navigate to project
cd amul-sales-dashboard

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
amul-sales-dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md
├── .streamlit/
│   └── config.toml                 # Streamlit theme config
├── data/
│   ├── raw/
│   │   └── field_sales_log.csv     # Raw field data (one row = one product pitch)
│   ├── master/
│   │   ├── products_master.csv     # Product reference data
│   │   ├── outlets_master.csv      # Outlet reference data
│   │   └── objections_master.csv   # Objection categories
│   └── processed/                  # Cleaned data output
└── src/
    ├── __init__.py
    ├── data_loader.py              # CSV loading with validation
    ├── data_cleaning.py            # Text standardization, defaults
    ├── features.py                 # Derived fields (flags, scores)
    ├── kpis.py                     # All KPI calculations
    ├── analysis_products.py        # Product-level analytics
    ├── analysis_outlets.py         # Outlet-level analytics
    ├── recommendations.py          # Rule-based recommendation engine
    ├── ai_summary.py               # AI/template summary generation
    ├── charts.py                   # Plotly chart library
    └── generate_demo_data.py       # Synthetic data generator
```

## 📐 Data Model

**Unit of analysis**: One product pitched at one outlet on one date

### Key Columns
- **Visit**: date, distributor, salesman, beat, area
- **Outlet**: outlet_id, outlet_type, outlet_size, cold_storage, footfall
- **Product**: product_name, product_group
- **Execution**: pitched, availability, visibility, scheme_explained, interest
- **Conversion**: order_booked, bill_cut, pieces_ordered
- **Intelligence**: objection, competitor, follow_up, observation

## 📈 Key KPIs

| KPI | Formula |
|-----|---------|
| Strike Rate | Productive Calls / Total Pitches × 100 |
| Conversion Rate | Orders Booked / Total Pitches × 100 |
| Bill Cut Rate | Bills Cut / Orders Booked × 100 |
| Avg Pieces/Order | Total Pieces / Orders Booked |
| Numeric Distribution | Outlets Carrying Product / Total Target Outlets × 100 |
| Range Selling | Products Ordered per Outlet / Products Pitched per Outlet |

## 🔧 Using Your Own Data

1. Replace `data/raw/field_sales_log.csv` with your real field data
2. Ensure column names match the expected format
3. Update `data/master/` files with your actual products and outlets
4. Restart the dashboard: `streamlit run app.py`

## 📝 For Internship Report

This project demonstrates:
- Built an outlet-level sales conversion dashboard for Amul focus products
- Tracked strike rate, product-wise conversion, objection patterns, and outlet opportunity
- Identified key conversion barriers including demand perception, pricing, and product-outlet mismatch
- Developed rule-based follow-up recommendations for improving field sales productivity

## 📄 License

For educational and internship use.
