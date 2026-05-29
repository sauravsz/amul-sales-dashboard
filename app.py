"""
Amul Focus Product Sales Conversion Dashboard v2.0
====================================================
A field sales intelligence system with 12 pages covering:
- Executive overview with smart alerts
- Product & outlet intelligence
- Execution quality & scheme effectiveness
- Follow-up planner with recommendations
- Weekly trends & target tracking
- Beat productivity & competitor intelligence
- Data entry form & CSV upload
- AI summary & report export

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import os
import sys
import io
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(__file__))

from src.data_loader import load_field_log, load_products_master, load_outlets_master
from src.data_cleaning import clean_pipeline
from src.features import create_features
from src.kpis import (
    coverage_kpis, conversion_kpis, product_kpis, execution_kpis,
    funnel_data, daily_trend, outlet_type_stats, weekly_trend,
)
from src.analysis_products import (
    product_performance_table, product_objection_matrix, product_outlet_fit_matrix,
)
from src.analysis_outlets import (
    outlet_performance_table, outlet_type_comparison, opportunity_outlets,
    follow_up_priority_table,
)
from src.recommendations import generate_recommendations, recommendation_summary
from src.ai_summary import (
    generate_template_summary, generate_ai_summary, get_objection_distribution,
)
from src.targets import daily_achievement, weekly_achievement, load_targets, save_targets
from src.beat_analysis import beat_performance_table, beat_product_matrix, beat_ranking
from src.retailer_score import calculate_retailer_scores, health_distribution
from src.competitor_analysis import (
    competitor_overview, competitor_brand_analysis, competitor_by_product,
    competitor_by_outlet_type, competitor_product_matrix,
)
from src.alerts import generate_alerts, format_alert_html
from src.report_export import generate_html_report
from src.charts import (
    kpi_card_html, daily_pitches_vs_orders, daily_conversion_trend,
    product_conversion_bar, pitches_vs_orders_stacked,
    outlet_type_conversion_bar, objection_distribution_bar,
    product_objection_heatmap, product_outlet_matrix_heatmap,
    outlet_scatter, execution_funnel, conversion_by_factor,
    recommendation_priority_donut,
    # V2 charts
    weekly_comparison_bar, weekly_conversion_line, weekly_pieces_bar,
    beat_conversion_bar, beat_productivity_scatter,
    retailer_health_donut, retailer_score_bar,
    competitor_brand_bar, competitor_exposure_bar,
    target_progress_html, scheme_effectiveness_chart,
)

# ───────────────────────────────────────────────
# Page Config
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Amul Sales Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────────────────────────
# Custom CSS
# ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #312e81 50%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .dashboard-header h1 {
        font-size: 1.75rem; font-weight: 800;
        background: linear-gradient(135deg, #e2e8f0, #a5b4fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .dashboard-header p { color: #94a3b8; font-size: 0.9rem; margin: 0; }
    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #e2e8f0;
        padding: 12px 0 8px 0; border-bottom: 1px solid #334155; margin-bottom: 16px;
    }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%); }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b, rgba(99,102,241,0.08));
        border: 1px solid #334155; border-radius: 12px; padding: 16px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8 !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 700 !important; color: #a5b4fc !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 20px; font-weight: 600; }
    hr { border: none; border-top: 1px solid #334155; margin: 20px 0; }
    footer {visibility: hidden;} #MainMenu {visibility: hidden;}
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important;
    }
    .nav-section { color: #475569; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin: 12px 0 4px 0; }
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_CSV = os.path.join(DATA_DIR, "raw", "field_sales_log.csv")

# ───────────────────────────────────────────────
# Load & Process Data
# ───────────────────────────────────────────────
@st.cache_data
def load_and_process():
    df = load_field_log()
    if df.empty:
        return pd.DataFrame()
    df = clean_pipeline(df)
    df = create_features(df)
    return df

df = load_and_process()

if df.empty:
    st.error("⚠️ No data found. Please add field_sales_log.csv to data/raw/ or use the Data Entry page.")
    st.info("Navigate to 📝 **Data Entry** in the sidebar to start adding your field data.")

# ───────────────────────────────────────────────
# Sidebar
# ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:16px 0;">
        <div style="font-size:2rem;">🥛</div>
        <div style="font-size:1.1rem; font-weight:800; color:#a5b4fc; margin-top:4px;">Amul Sales Intel</div>
        <div style="font-size:0.65rem; color:#64748b; margin-top:2px;">v2.0 — Field Sales Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p class="nav-section">📊 Analytics</p>', unsafe_allow_html=True)
    page = st.radio(
        "Dashboard",
        [
            "🏠 Executive Overview",
            "📦 Product Intelligence",
            "🏪 Outlet Intelligence",
            "⚙️ Execution Quality",
            "📋 Follow-up Planner",
            "📈 Weekly Trends",
            "🎯 Targets",
            "🗺️ Beat Analysis",
            "⚔️ Competitor Intel",
            "🤖 AI Summary",
            "📝 Data Entry",
            "📄 Export Report",
        ],
        label_visibility="collapsed",
    )

    if not df.empty:
        st.divider()
        st.markdown('<p class="nav-section">🔍 Filters</p>', unsafe_allow_html=True)

        if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
            min_d, max_d = df["date"].min().date(), df["date"].max().date()
            date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
        else:
            date_range = None

        all_products = sorted(df["product_name"].unique().tolist())
        selected_products = st.multiselect("Products", all_products, default=[])
        all_groups = sorted(df["product_group"].unique().tolist())
        selected_groups = st.multiselect("Product Groups", all_groups, default=[])
        all_otypes = sorted(df["outlet_type"].unique().tolist())
        selected_otypes = st.multiselect("Outlet Types", all_otypes, default=[])

        if "beat_name" in df.columns:
            all_beats = sorted(df["beat_name"].unique().tolist())
            selected_beats = st.multiselect("Beats", all_beats, default=[])
        else:
            selected_beats = []

        st.divider()
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.rerun()

        st.download_button("📥 Download Data", data=df.to_csv(index=False).encode("utf-8"),
                           file_name="amul_field_sales_data.csv", mime="text/csv", use_container_width=True)
    else:
        date_range = None
        selected_products = []
        selected_groups = []
        selected_otypes = []
        selected_beats = []

    st.divider()
    st.markdown('<p style="color:#475569; font-size:0.6rem; text-align:center;">Built for Amul Field Internship • v2.0</p>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
# Apply Filters
# ───────────────────────────────────────────────
filtered = df.copy()
if not df.empty:
    if date_range and len(date_range) == 2:
        s, e = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["date"] >= s) & (filtered["date"] <= e)]
    if selected_products:
        filtered = filtered[filtered["product_name"].isin(selected_products)]
    if selected_groups:
        filtered = filtered[filtered["product_group"].isin(selected_groups)]
    if selected_otypes:
        filtered = filtered[filtered["outlet_type"].isin(selected_otypes)]
    if selected_beats:
        filtered = filtered[filtered["beat_name"].isin(selected_beats)]

# Allow data entry / export pages even with empty data
if filtered.empty and page not in ("📝 Data Entry", "📄 Export Report"):
    if not df.empty:
        st.warning("No data matches your filter selection. Adjust filters or use 📝 Data Entry to add data.")
    st.stop()

# ───────────────────────────────────────────────
# Pre-compute metrics (only if data exists)
# ───────────────────────────────────────────────
if not filtered.empty:
    cov = coverage_kpis(filtered)
    conv = conversion_kpis(filtered)
    exec_k = execution_kpis(filtered)
    prod_k = product_kpis(filtered)
    funnel = funnel_data(filtered)
    daily = daily_trend(filtered)
    otype_stats = outlet_type_stats(filtered)
    objection_dist = get_objection_distribution(filtered)
    weekly = weekly_trend(filtered)
else:
    cov = conv = exec_k = {}
    prod_k = pd.DataFrame()
    funnel = {}
    daily = weekly = pd.DataFrame()
    otype_stats = pd.DataFrame()
    objection_dist = pd.DataFrame()


# ═══════════════════════════════════════════════
# PAGE 1: EXECUTIVE OVERVIEW (+ Alerts)
# ═══════════════════════════════════════════════
if page == "🏠 Executive Overview":
    st.markdown("""<div class="dashboard-header">
        <h1>🏠 Executive Overview</h1>
        <p>Field sales performance at a glance — with smart alerts and key metrics</p>
    </div>""", unsafe_allow_html=True)

    # --- Smart Alerts (Improvement #9) ---
    alerts = generate_alerts(filtered)
    if alerts:
        with st.expander("🔔 **Smart Alerts & Insights**", expanded=True):
            for alert in alerts[:6]:
                st.markdown(format_alert_html(alert), unsafe_allow_html=True)

    # KPI Row
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1: st.markdown(kpi_card_html("Visit Days", cov["total_visit_days"], f"{cov['unique_outlets']} outlets"), unsafe_allow_html=True)
    with k2: st.markdown(kpi_card_html("Total Pitches", cov["total_pitches"], f"{cov['productive_calls']} productive"), unsafe_allow_html=True)
    with k3: st.markdown(kpi_card_html("Strike Rate", f"{conv['strike_rate']}%", "Orders/Pitches", color="#10B981"), unsafe_allow_html=True)
    with k4: st.markdown(kpi_card_html("Pieces Ordered", conv["total_pieces_ordered"], f"Avg {conv['avg_pieces_per_order']}/order"), unsafe_allow_html=True)
    with k5: st.markdown(kpi_card_html("Bill Cut Rate", f"{conv['bill_cut_rate']}%", "", color="#F59E0B"), unsafe_allow_html=True)
    with k6: st.markdown(kpi_card_html("Est. Value", f"₹{conv.get('estimated_total_value',0):,.0f}", "", color="#8B5CF6"), unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(daily_pitches_vs_orders(daily), use_container_width=True)
    with c2: st.plotly_chart(product_conversion_bar(prod_k), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3: st.plotly_chart(outlet_type_conversion_bar(otype_stats), use_container_width=True)
    with c4: st.plotly_chart(objection_distribution_bar(objection_dist), use_container_width=True)

    st.plotly_chart(daily_conversion_trend(daily), use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE 2: PRODUCT INTELLIGENCE
# ═══════════════════════════════════════════════
elif page == "📦 Product Intelligence":
    st.markdown("""<div class="dashboard-header">
        <h1>📦 Product Intelligence</h1>
        <p>Product performance, conversion drivers, objection patterns, and product-outlet fit</p>
    </div>""", unsafe_allow_html=True)

    prod_perf = product_performance_table(filtered)
    if prod_perf.empty:
        st.warning("No product data available.")
    else:
        best, worst = prod_perf.iloc[0], prod_perf.iloc[-1]
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi_card_html("Best Product", best["product_name"], f"{best['conversion_pct']}%", color="#10B981"), unsafe_allow_html=True)
        with k2: st.markdown(kpi_card_html("Weakest", worst["product_name"], f"{worst['conversion_pct']}%", color="#EF4444"), unsafe_allow_html=True)
        with k3: st.markdown(kpi_card_html("Avg Conv", f"{prod_perf['conversion_pct'].mean():.1f}%", f"{len(prod_perf)} products"), unsafe_allow_html=True)
        with k4: st.markdown(kpi_card_html("Total Pieces", int(prod_perf["pieces"].sum()), ""), unsafe_allow_html=True)

        st.markdown("")
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(product_conversion_bar(prod_perf), use_container_width=True)
        with c2: st.plotly_chart(pitches_vs_orders_stacked(prod_perf), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3: st.plotly_chart(product_objection_heatmap(product_objection_matrix(filtered)), use_container_width=True)
        with c4: st.plotly_chart(product_outlet_matrix_heatmap(product_outlet_fit_matrix(filtered)), use_container_width=True)

        st.markdown('<div class="section-header">📊 Detailed Product Performance</div>', unsafe_allow_html=True)
        dcols = ["product_name","product_group","pitches","orders","pieces","conversion_pct","avg_order_size","availability_pct","scheme_pct","competitor_pct","top_objection"]
        dcols = [c for c in dcols if c in prod_perf.columns]
        st.dataframe(prod_perf[dcols].rename(columns={"product_name":"Product","product_group":"Group","pitches":"Pitches","orders":"Orders","pieces":"Pieces","conversion_pct":"Conv %","avg_order_size":"Avg Order","availability_pct":"Avail %","scheme_pct":"Scheme %","competitor_pct":"Comp %","top_objection":"Top Objection"}), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 3: OUTLET INTELLIGENCE (+ Retailer Score)
# ═══════════════════════════════════════════════
elif page == "🏪 Outlet Intelligence":
    st.markdown("""<div class="dashboard-header">
        <h1>🏪 Outlet Intelligence</h1>
        <p>Outlet performance, retailer relationship health, and opportunity identification</p>
    </div>""", unsafe_allow_html=True)

    outlet_perf = outlet_performance_table(filtered)
    otype_comp = outlet_type_comparison(filtered)
    opp_outlets = opportunity_outlets(filtered)

    # --- Retailer Scores (Improvement #5) ---
    scores = calculate_retailer_scores(filtered)
    health_dist = health_distribution(scores)

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(kpi_card_html("Total Outlets", cov["unique_outlets"], f"{cov['outlet_coverage_rate']}% coverage"), unsafe_allow_html=True)
    with k2:
        strong = len(scores[scores["health_status"]=="🟢 Strong"]) if not scores.empty else 0
        st.markdown(kpi_card_html("Strong Retailers", strong, "Score ≥ 60", color="#10B981"), unsafe_allow_html=True)
    with k3:
        at_risk = len(scores[scores["health_status"]=="🔴 At Risk"]) if not scores.empty else 0
        st.markdown(kpi_card_html("At Risk", at_risk, "Score < 35", color="#EF4444"), unsafe_allow_html=True)
    with k4:
        opp_count = len(opp_outlets) if not opp_outlets.empty else 0
        st.markdown(kpi_card_html("Opportunities", opp_count, "High interest, low orders", color="#F59E0B"), unsafe_allow_html=True)

    st.markdown("")

    tab1, tab2 = st.tabs(["📊 Outlet Analytics", "💪 Retailer Health Scores"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(outlet_scatter(outlet_perf), use_container_width=True)
        with c2: st.plotly_chart(outlet_type_conversion_bar(otype_comp), use_container_width=True)

        if not otype_comp.empty:
            st.markdown('<div class="section-header">📊 Outlet Type Comparison</div>', unsafe_allow_html=True)
            st.dataframe(otype_comp[["outlet_type","unique_outlets","pitches","orders","pieces","conversion_pct","avg_pieces_per_order","competitor_pct"]].rename(columns={"outlet_type":"Type","unique_outlets":"Outlets","pitches":"Pitches","orders":"Orders","pieces":"Pieces","conversion_pct":"Conv %","avg_pieces_per_order":"Avg Pcs","competitor_pct":"Comp %"}), use_container_width=True, hide_index=True)

        if not opp_outlets.empty:
            st.markdown('<div class="section-header">🎯 Opportunity Outlets</div>', unsafe_allow_html=True)
            st.dataframe(opp_outlets[["outlet_name","outlet_type","outlet_size","total_pitches","total_orders","avg_interest","high_interest_no_order","top_product"]].rename(columns={"outlet_name":"Outlet","outlet_type":"Type","outlet_size":"Size","total_pitches":"Pitches","total_orders":"Orders","avg_interest":"Avg Interest","high_interest_no_order":"HI/No Order","top_product":"Top Product"}), use_container_width=True, hide_index=True)

    with tab2:
        if not scores.empty:
            c1, c2 = st.columns([0.4, 0.6])
            with c1: st.plotly_chart(retailer_health_donut(health_dist), use_container_width=True)
            with c2: st.plotly_chart(retailer_score_bar(scores), use_container_width=True)

            st.markdown('<div class="section-header">📋 Full Retailer Scoreboard</div>', unsafe_allow_html=True)
            scols = ["outlet_name","outlet_type","health_status","relationship_score","conversion_rate","total_orders","total_pieces","avg_interest"]
            scols = [c for c in scols if c in scores.columns]
            st.dataframe(scores[scols].rename(columns={"outlet_name":"Outlet","outlet_type":"Type","health_status":"Health","relationship_score":"Score","conversion_rate":"Conv %","total_orders":"Orders","total_pieces":"Pieces","avg_interest":"Avg Interest"}), use_container_width=True, hide_index=True)
        else:
            st.info("No retailer data available.")


# ═══════════════════════════════════════════════
# PAGE 4: EXECUTION QUALITY (+ Scheme Effectiveness)
# ═══════════════════════════════════════════════
elif page == "⚙️ Execution Quality":
    st.markdown("""<div class="dashboard-header">
        <h1>⚙️ Execution Quality</h1>
        <p>Availability, visibility, scheme communication, competitor presence — and their impact on conversion</p>
    </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    color_a = "#10B981" if exec_k["availability_pct"] >= 60 else "#F59E0B" if exec_k["availability_pct"] >= 40 else "#EF4444"
    color_s = "#10B981" if exec_k["scheme_explained_pct"] >= 60 else "#F59E0B"
    with k1: st.markdown(kpi_card_html("Availability %", f"{exec_k['availability_pct']}%", "Before pitch", color=color_a), unsafe_allow_html=True)
    with k2: st.markdown(kpi_card_html("Scheme Explained", f"{exec_k['scheme_explained_pct']}%", "", color=color_s), unsafe_allow_html=True)
    with k3: st.markdown(kpi_card_html("Avg Visibility", f"{exec_k['avg_visibility_score']}/3", "", color="#6366F1"), unsafe_allow_html=True)
    with k4: st.markdown(kpi_card_html("Competitor %", f"{exec_k['competitor_presence_pct']}%", "", color="#EF4444"), unsafe_allow_html=True)
    with k5: st.markdown(kpi_card_html("Follow-up %", f"{exec_k['follow_up_needed_pct']}%", f"{exec_k['high_interest_no_order_count']} HI/NoOrder", color="#F59E0B"), unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns([1.2, 0.8])
    with c1: st.plotly_chart(execution_funnel(funnel), use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">📉 Funnel Drop-off</div>', unsafe_allow_html=True)
        fv = list(funnel.values())
        fk = list(funnel.keys())
        for i in range(1, len(fv)):
            if fv[i-1] > 0:
                drop = round((1 - fv[i]/fv[i-1]) * 100, 1)
                icon = "🔴" if drop > 50 else "🟡" if drop > 30 else "🟢"
                st.markdown(f"{icon} **{fk[i-1]} → {fk[i]}**: {drop}% drop-off")

    c3, c4, c5 = st.columns(3)
    with c3: st.plotly_chart(conversion_by_factor(filtered, "display_visibility", "Conversion by Visibility"), use_container_width=True)
    with c4: st.plotly_chart(conversion_by_factor(filtered, "scheme_explained", "Conversion by Scheme Explained"), use_container_width=True)
    with c5: st.plotly_chart(conversion_by_factor(filtered, "availability_before_pitch", "Conversion by Availability"), use_container_width=True)

    # --- Scheme Effectiveness (Improvement #7) ---
    st.markdown('<div class="section-header">💊 Scheme Effectiveness Analysis</div>', unsafe_allow_html=True)
    st.plotly_chart(scheme_effectiveness_chart(filtered), use_container_width=True)

    c6, c7 = st.columns(2)
    with c6: st.plotly_chart(conversion_by_factor(filtered, "retailer_interest_level", "Conversion by Interest Level"), use_container_width=True)
    with c7: st.plotly_chart(conversion_by_factor(filtered, "competitor_present", "Conversion by Competitor Presence"), use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE 5: FOLLOW-UP PLANNER
# ═══════════════════════════════════════════════
elif page == "📋 Follow-up Planner":
    st.markdown("""<div class="dashboard-header">
        <h1>📋 Follow-up Planner</h1>
        <p>AI-powered recommendations — prioritized follow-up actions for your next field visits</p>
    </div>""", unsafe_allow_html=True)

    recs = generate_recommendations(filtered)
    by_rule, by_priority = recommendation_summary(recs)

    if recs.empty:
        st.info("No recommendations generated — conversion is strong! 🎉")
    else:
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi_card_html("Total Actions", len(recs), f"{len(recs[recs['priority']=='High'])} high"), unsafe_allow_html=True)
        with k2: st.markdown(kpi_card_html("Outlets Flagged", recs["outlet_id"].nunique(), "", color="#F59E0B"), unsafe_allow_html=True)
        with k3: st.markdown(kpi_card_html("Products Flagged", recs["product_name"].nunique(), "", color="#EF4444"), unsafe_allow_html=True)
        with k4:
            top_r = by_rule.iloc[0]["rule_name"] if not by_rule.empty else "N/A"
            st.markdown(kpi_card_html("Top Issue", top_r, "", color="#8B5CF6"), unsafe_allow_html=True)

        st.markdown("")
        c1, c2 = st.columns([0.4, 0.6])
        with c1: st.plotly_chart(recommendation_priority_donut(by_priority), use_container_width=True)
        with c2:
            st.markdown('<div class="section-header">🔍 Top Rules Triggered</div>', unsafe_allow_html=True)
            for _, row in by_rule.head(6).iterrows():
                em = "🔴" if row["priority"]=="High" else "🟡" if row["priority"]=="Medium" else "🟢"
                st.markdown(f"{em} **{row['rule_name']}** — {int(row['count'])} cases")

        st.markdown("")
        pf = st.selectbox("Filter by Priority", ["All","High","Medium","Low"])
        dr = recs if pf == "All" else recs[recs["priority"]==pf]
        dcols = ["priority","outlet_name","outlet_type","product_name","rule_name","suggested_action","interest_level","objection"]
        dcols = [c for c in dcols if c in dr.columns]
        st.dataframe(dr[dcols].rename(columns={"priority":"⚡","outlet_name":"🏪 Outlet","outlet_type":"Type","product_name":"📦 Product","rule_name":"🔍 Issue","suggested_action":"💡 Action","interest_level":"Interest","objection":"Objection"}), use_container_width=True, hide_index=True, height=500)
        st.download_button("📥 Download Recommendations", data=dr.to_csv(index=False).encode("utf-8"), file_name="followup_recommendations.csv", mime="text/csv")

    followup_t = follow_up_priority_table(filtered)
    if not followup_t.empty:
        st.markdown('<div class="section-header">📝 Field-Logged Follow-ups</div>', unsafe_allow_html=True)
        st.dataframe(followup_t[["outlet_name","product_name","interest_level","objection","priority","reason","observation"]].rename(columns={"outlet_name":"Outlet","product_name":"Product","interest_level":"Interest","objection":"Objection","priority":"Priority","reason":"Reason","observation":"Observation"}), use_container_width=True, hide_index=True, height=400)


# ═══════════════════════════════════════════════
# PAGE 6: WEEKLY TRENDS (Improvement #2)
# ═══════════════════════════════════════════════
elif page == "📈 Weekly Trends":
    st.markdown("""<div class="dashboard-header">
        <h1>📈 Weekly Trends</h1>
        <p>Week-over-week performance comparison — track your trajectory and improvement</p>
    </div>""", unsafe_allow_html=True)

    if weekly.empty or len(weekly) < 1:
        st.info("Need at least 1 week of data for weekly trends.")
    else:
        # WoW summary cards
        latest_w = weekly.iloc[-1]
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: st.markdown(kpi_card_html("Weeks Tracked", len(weekly), ""), unsafe_allow_html=True)
        with k2: st.markdown(kpi_card_html("Latest Conv %", f"{latest_w['conversion_pct']}%", f"Week {int(latest_w['week_no'])}", color="#10B981"), unsafe_allow_html=True)
        with k3: st.markdown(kpi_card_html("Latest Pieces", int(latest_w['pieces']), f"Week {int(latest_w['week_no'])}"), unsafe_allow_html=True)
        with k4: st.markdown(kpi_card_html("Pitches/Day", latest_w['pitches_per_day'], "Latest week", color="#3B82F6"), unsafe_allow_html=True)
        with k5:
            if len(weekly) >= 2:
                prev = weekly.iloc[-2]
                delta = latest_w['conversion_pct'] - prev['conversion_pct']
                delta_color = "#10B981" if delta >= 0 else "#EF4444"
                st.markdown(kpi_card_html("WoW Change", f"{delta:+.1f}pp", "Conversion", color=delta_color), unsafe_allow_html=True)
            else:
                st.markdown(kpi_card_html("WoW Change", "N/A", "Need 2+ weeks"), unsafe_allow_html=True)

        st.markdown("")
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(weekly_comparison_bar(weekly), use_container_width=True)
        with c2: st.plotly_chart(weekly_conversion_line(weekly), use_container_width=True)

        st.plotly_chart(weekly_pieces_bar(weekly), use_container_width=True)

        st.markdown('<div class="section-header">📊 Weekly Breakdown Table</div>', unsafe_allow_html=True)
        wdisplay = weekly[["week_no","days","unique_outlets","pitches","orders","pieces","conversion_pct","avg_pieces_per_order","pitches_per_day","scheme_pct","competitor_pct"]].rename(columns={"week_no":"Week","days":"Days","unique_outlets":"Outlets","pitches":"Pitches","orders":"Orders","pieces":"Pieces","conversion_pct":"Conv %","avg_pieces_per_order":"Avg Pcs/Order","pitches_per_day":"Pitches/Day","scheme_pct":"Scheme %","competitor_pct":"Comp %"})
        st.dataframe(wdisplay, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 7: TARGETS (Improvement #3)
# ═══════════════════════════════════════════════
elif page == "🎯 Targets":
    st.markdown("""<div class="dashboard-header">
        <h1>🎯 Target vs Achievement</h1>
        <p>Track daily and weekly targets — visualize your progress with live progress bars</p>
    </div>""", unsafe_allow_html=True)

    targets = load_targets()
    tab_d, tab_w, tab_s = st.tabs(["📅 Daily", "📊 Weekly", "⚙️ Set Targets"])

    with tab_d:
        if "date" in filtered.columns:
            avail_dates = sorted(filtered["date"].dt.date.unique(), reverse=True)
            sel_date = st.selectbox("Select Date", avail_dates, index=0)
            da = daily_achievement(filtered, sel_date, targets)
            if not da.empty:
                st.markdown(f"### Performance for {sel_date}")
                st.markdown(target_progress_html(da), unsafe_allow_html=True)
            else:
                st.info("No data for this date.")

    with tab_w:
        if "week_no" in filtered.columns:
            avail_weeks = sorted(filtered["week_no"].unique())
            sel_week = st.selectbox("Select Week", avail_weeks, index=len(avail_weeks)-1)
            wa = weekly_achievement(filtered, sel_week, targets)
            if not wa.empty:
                st.markdown(f"### Week {int(sel_week)} Achievement")
                st.markdown(target_progress_html(wa), unsafe_allow_html=True)
            else:
                st.info("No data for this week.")

    with tab_s:
        st.markdown("### Configure Targets")
        st.markdown("Set your daily and weekly targets. Changes are saved immediately.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Daily Targets**")
            d = targets.get("daily", {})
            d_visits = st.number_input("Outlet Visits / Day", value=d.get("outlet_visits", 8), min_value=1, key="dt_v")
            d_pitch = st.number_input("Pitches / Day", value=d.get("total_pitches", 25), min_value=1, key="dt_p")
            d_orders = st.number_input("Orders / Day", value=d.get("orders_booked", 10), min_value=1, key="dt_o")
            d_pieces = st.number_input("Pieces / Day", value=d.get("pieces_ordered", 50), min_value=1, key="dt_pc")
            d_strike = st.number_input("Strike Rate % / Day", value=d.get("strike_rate_pct", 40), min_value=1, key="dt_s")

        with c2:
            st.markdown("**Weekly Targets**")
            w = targets.get("weekly", {})
            w_visits = st.number_input("Outlet Visits / Week", value=w.get("outlet_visits", 40), min_value=1, key="wt_v")
            w_pitch = st.number_input("Pitches / Week", value=w.get("total_pitches", 125), min_value=1, key="wt_p")
            w_orders = st.number_input("Orders / Week", value=w.get("orders_booked", 50), min_value=1, key="wt_o")
            w_pieces = st.number_input("Pieces / Week", value=w.get("pieces_ordered", 250), min_value=1, key="wt_pc")
            w_outlets = st.number_input("Unique Outlets / Week", value=w.get("unique_outlets", 20), min_value=1, key="wt_u")
            w_strike = st.number_input("Strike Rate % / Week", value=w.get("strike_rate_pct", 45), min_value=1, key="wt_s")

        if st.button("💾 Save Targets", type="primary", use_container_width=True):
            new_targets = {
                "daily": {"outlet_visits": d_visits, "total_pitches": d_pitch, "orders_booked": d_orders, "pieces_ordered": d_pieces, "strike_rate_pct": d_strike},
                "weekly": {"outlet_visits": w_visits, "total_pitches": w_pitch, "orders_booked": w_orders, "pieces_ordered": w_pieces, "unique_outlets": w_outlets, "strike_rate_pct": w_strike},
            }
            save_targets(new_targets)
            st.success("✅ Targets saved successfully!")
            st.rerun()


# ═══════════════════════════════════════════════
# PAGE 8: BEAT ANALYSIS (Improvement #4)
# ═══════════════════════════════════════════════
elif page == "🗺️ Beat Analysis":
    st.markdown("""<div class="dashboard-header">
        <h1>🗺️ Beat / Route Analysis</h1>
        <p>Compare productivity across beats — find your most efficient routes</p>
    </div>""", unsafe_allow_html=True)

    beat_perf = beat_performance_table(filtered)
    beat_rank = beat_ranking(filtered)

    if beat_perf.empty:
        st.info("No beat data available. Ensure 'beat_name' column exists in your data.")
    else:
        best_beat = beat_rank.iloc[0] if not beat_rank.empty else beat_perf.iloc[0]
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi_card_html("Total Beats", len(beat_perf), ""), unsafe_allow_html=True)
        with k2: st.markdown(kpi_card_html("Best Beat", best_beat["beat_name"], f"{best_beat['conversion_pct']}% conv", color="#10B981"), unsafe_allow_html=True)
        with k3: st.markdown(kpi_card_html("Avg Conv", f"{beat_perf['conversion_pct'].mean():.1f}%", "Across beats"), unsafe_allow_html=True)
        with k4: st.markdown(kpi_card_html("Total Pieces", int(beat_perf["pieces"].sum()), ""), unsafe_allow_html=True)

        st.markdown("")
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(beat_conversion_bar(beat_perf), use_container_width=True)
        with c2: st.plotly_chart(beat_productivity_scatter(beat_perf), use_container_width=True)

        # Beat-Product Matrix
        bpm = beat_product_matrix(filtered)
        if not bpm.empty:
            st.markdown('<div class="section-header">🔥 Beat × Product Conversion Matrix</div>', unsafe_allow_html=True)
            st.plotly_chart(product_outlet_matrix_heatmap(bpm), use_container_width=True)

        st.markdown('<div class="section-header">📊 Beat Performance Table</div>', unsafe_allow_html=True)
        bcols = ["beat_name","visit_days","unique_outlets","pitches","orders","pieces","conversion_pct","pitches_per_day","orders_per_day","scheme_pct","competitor_pct"]
        bcols = [c for c in bcols if c in beat_perf.columns]
        st.dataframe(beat_perf[bcols].rename(columns={"beat_name":"Beat","visit_days":"Days","unique_outlets":"Outlets","pitches":"Pitches","orders":"Orders","pieces":"Pieces","conversion_pct":"Conv %","pitches_per_day":"Pitches/Day","orders_per_day":"Orders/Day","scheme_pct":"Scheme %","competitor_pct":"Comp %"}), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 9: COMPETITOR INTELLIGENCE (Improvement #6)
# ═══════════════════════════════════════════════
elif page == "⚔️ Competitor Intel":
    st.markdown("""<div class="dashboard-header">
        <h1>⚔️ Competitor Intelligence</h1>
        <p>Which competitors block which products, in which outlets — and how to win</p>
    </div>""", unsafe_allow_html=True)

    comp_ov = competitor_overview(filtered)
    comp_brands = competitor_brand_analysis(filtered)
    comp_products = competitor_by_product(filtered)
    comp_outlets = competitor_by_outlet_type(filtered)

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(kpi_card_html("Competitor Presence", f"{comp_ov.get('competitor_present_pct',0)}%", f"{comp_ov.get('competitor_present_count',0)} encounters"), unsafe_allow_html=True)
    with k2: st.markdown(kpi_card_html("Conv WITH Comp", f"{comp_ov.get('conversion_with_competitor',0)}%", "", color="#EF4444"), unsafe_allow_html=True)
    with k3: st.markdown(kpi_card_html("Conv WITHOUT", f"{comp_ov.get('conversion_without_competitor',0)}%", "", color="#10B981"), unsafe_allow_html=True)
    with k4: st.markdown(kpi_card_html("Conversion Gap", f"{comp_ov.get('conversion_gap',0):+.1f}pp", f"{comp_ov.get('unique_competitors',0)} competitors", color="#F59E0B"), unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(competitor_brand_bar(comp_brands), use_container_width=True)
    with c2: st.plotly_chart(competitor_exposure_bar(comp_products), use_container_width=True)

    # Competitor-Product matrix
    cpm = competitor_product_matrix(filtered)
    if not cpm.empty:
        st.markdown('<div class="section-header">🔥 Amul Product × Competitor Brand Matrix</div>', unsafe_allow_html=True)
        st.plotly_chart(product_objection_heatmap(cpm), use_container_width=True)

    if not comp_products.empty:
        st.markdown('<div class="section-header">📊 Product-Level Competitor Analysis</div>', unsafe_allow_html=True)
        pcols = ["product_name","total_pitches","comp_present","competitor_exposure_pct","top_competitor"]
        pcols = [c for c in pcols if c in comp_products.columns]
        st.dataframe(comp_products[pcols].rename(columns={"product_name":"Product","total_pitches":"Pitches","comp_present":"Comp Present","competitor_exposure_pct":"Exposure %","top_competitor":"Top Competitor"}), use_container_width=True, hide_index=True)

    if not comp_outlets.empty:
        st.markdown('<div class="section-header">🏪 Competitor Presence by Outlet Type</div>', unsafe_allow_html=True)
        ocols = ["outlet_type","pitches","comp_present","competitor_pct","top_brands"]
        ocols = [c for c in ocols if c in comp_outlets.columns]
        st.dataframe(comp_outlets[ocols].rename(columns={"outlet_type":"Type","pitches":"Pitches","comp_present":"Comp Present","competitor_pct":"Comp %","top_brands":"Top Brands"}), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# PAGE 10: AI SUMMARY
# ═══════════════════════════════════════════════
elif page == "🤖 AI Summary":
    st.markdown("""<div class="dashboard-header">
        <h1>🤖 AI-Powered Summary</h1>
        <p>Generate a manager-ready weekly performance summary</p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([0.6, 0.4])
    with c1: api_key = st.text_input("🔑 Gemini API Key (optional)", type="password", help="Leave empty for template summary.")
    with c2:
        st.markdown(""); st.markdown("")
        use_ai = st.checkbox("Use AI Summary", value=bool(api_key))

    if st.button("📊 Generate Summary", use_container_width=True, type="primary"):
        with st.spinner("Generating summary..."):
            if use_ai and api_key:
                summary = generate_ai_summary(api_key, cov, conv, exec_k, prod_k, objection_dist)
                if "⚠️" in summary:
                    st.warning("AI failed, showing template instead.")
                    summary = generate_template_summary(cov, conv, exec_k, prod_k, objection_dist)
            else:
                summary = generate_template_summary(cov, conv, exec_k, prod_k, objection_dist)
        st.markdown("---")
        st.markdown(summary)
        st.download_button("📥 Download Summary", data=summary.encode("utf-8"), file_name="weekly_summary.md", mime="text/markdown")
    else:
        st.info("Click **Generate Summary** to create your weekly report.")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Total Pitches", cov.get("total_pitches", 0))
        with c2: st.metric("Conversion Rate", f"{conv.get('conversion_rate', 0)}%")
        with c3: st.metric("Pieces Ordered", conv.get("total_pieces_ordered", 0))
        with c4: st.metric("Follow-up Cases", exec_k.get("high_interest_no_order_count", 0))


# ═══════════════════════════════════════════════
# PAGE 11: DATA ENTRY (Improvement #1 + #10)
# ═══════════════════════════════════════════════
elif page == "📝 Data Entry":
    st.markdown("""<div class="dashboard-header">
        <h1>📝 Data Entry</h1>
        <p>Add field visit data via form or upload CSV — supports Google Sheets export too</p>
    </div>""", unsafe_allow_html=True)

    tab_form, tab_upload = st.tabs(["📋 Manual Entry Form", "📤 CSV Upload"])

    with tab_form:
        st.markdown("### Log a Field Visit")
        st.markdown("Fill in one product pitch per submission. Submit multiple times for multiple products at one outlet.")

        products_master = load_products_master()
        outlets_master = load_outlets_master()

        product_names = products_master["product_name"].tolist() if not products_master.empty else [
            "More Tin Paneer","Amul Aata","Amul Cookies","Amul Chocolates",
            "Organic Kabuli Chana","Organic Toor Dal","Organic Masoor Dal","Organic Rajma"
        ]
        outlet_types = ["Kirana","Supermarket","Dairy Shop","Bakery","General Store","Departmental Store","Wholesaler","Others"]
        objection_cats = ["","No demand","Low margin","Already have competitor","No shelf space","Slow moving","High price","No customer asking","Stock not available","Not relevant for outlet","Retailer unconvinced","Cash or credit issue"]

        with st.form("field_entry", clear_on_submit=True):
            st.markdown("**📅 Visit Details**")
            c1, c2, c3 = st.columns(3)
            with c1: f_date = st.date_input("Date", value=date.today())
            with c2: f_beat = st.text_input("Beat / Route", value="Beat A - East")
            with c3: f_area = st.text_input("Area", value="Main Market")

            st.markdown("**🏪 Outlet Details**")
            c1, c2, c3, c4 = st.columns(4)
            with c1: f_outlet_name = st.text_input("Outlet Name *")
            with c2: f_outlet_type = st.selectbox("Outlet Type", outlet_types)
            with c3: f_outlet_size = st.selectbox("Outlet Size", ["Small","Medium","Large"])
            with c4: f_locality = st.selectbox("Locality", ["Residential","Market","Mixed","Institutional"])

            c1, c2 = st.columns(2)
            with c1: f_cold = st.selectbox("Cold Storage?", ["No","Yes"])
            with c2: f_footfall = st.selectbox("High Footfall?", ["No","Yes"])

            st.markdown("**📦 Product & Pitch**")
            c1, c2, c3, c4 = st.columns(4)
            with c1: f_product = st.selectbox("Product *", product_names)
            with c2: f_avail = st.selectbox("Availability Before Pitch", ["No","Yes"])
            with c3: f_visibility = st.selectbox("Display Visibility", ["Low","Medium","High"])
            with c4: f_scheme = st.selectbox("Scheme Explained", ["No","Yes"])

            c1, c2, c3 = st.columns(3)
            with c1: f_interest = st.selectbox("Retailer Interest", ["Low","Medium","High"])
            with c2: f_order = st.selectbox("Order Booked? *", ["No","Yes"])
            with c3: f_pieces = st.number_input("Pieces Ordered", min_value=0, value=0)

            c1, c2 = st.columns(2)
            with c1: f_bill = st.selectbox("Bill Cut?", ["No","Yes"])
            with c2: f_comp = st.selectbox("Competitor Present?", ["No","Yes"])

            c1, c2 = st.columns(2)
            with c1: f_comp_brand = st.text_input("Competitor Brand (if any)")
            with c2: f_objection = st.selectbox("Objection Category", objection_cats)

            f_objection_raw = st.text_input("Objection (raw notes)")
            c1, c2, c3 = st.columns(3)
            with c1: f_followup = st.selectbox("Follow-up Needed?", ["No","Yes"])
            with c2: f_followup_p = st.selectbox("Follow-up Priority", ["","High","Medium","Low"])
            with c3: f_followup_r = st.text_input("Follow-up Reason")
            f_obs = st.text_area("My Observation", height=68)

            submitted = st.form_submit_button("✅ Submit Entry", type="primary", use_container_width=True)

            if submitted:
                if not f_outlet_name.strip():
                    st.error("Outlet Name is required!")
                else:
                    # Build product group mapping
                    pg_map = {"More Tin Paneer":"Dairy","Amul Aata":"Staples","Amul Cookies":"Snacks","Amul Chocolates":"Confectionery","Organic Kabuli Chana":"Organics","Organic Toor Dal":"Organics","Organic Masoor Dal":"Organics","Organic Rajma":"Organics"}
                    ps_map = {"More Tin Paneer":"Paneer","Amul Aata":"Flour","Amul Cookies":"Cookies","Amul Chocolates":"Chocolate","Organic Kabuli Chana":"Pulses","Organic Toor Dal":"Pulses","Organic Masoor Dal":"Pulses","Organic Rajma":"Pulses"}

                    outlet_id = f"OUT{abs(hash(f_outlet_name)) % 10000:04d}"

                    new_row = {
                        "date": f_date.strftime("%Y-%m-%d"),
                        "day": f_date.strftime("%A"),
                        "week_no": "",
                        "month": f_date.strftime("%B"),
                        "distributor_name": "Amul Distributor - City Hub",
                        "salesman_name": "Saurav",
                        "beat_name": f_beat,
                        "area": f_area,
                        "outlet_id": outlet_id,
                        "outlet_name": f_outlet_name.strip(),
                        "outlet_type": f_outlet_type,
                        "outlet_size": f_outlet_size,
                        "locality_type": f_locality,
                        "cold_storage_available": f_cold,
                        "high_footfall": f_footfall,
                        "visited": "Yes",
                        "product_name": f_product,
                        "product_group": pg_map.get(f_product, "Other"),
                        "product_subgroup": ps_map.get(f_product, ""),
                        "pitched": "Yes",
                        "availability_before_pitch": f_avail,
                        "display_visibility": f_visibility,
                        "scheme_explained": f_scheme,
                        "retailer_interest_level": f_interest,
                        "order_booked": f_order,
                        "bill_cut": f_bill,
                        "pieces_ordered": f_pieces,
                        "pieces_sold_if_known": 0,
                        "order_value_if_known": "",
                        "competitor_present": f_comp,
                        "competitor_brand": f_comp_brand,
                        "retailer_objection_raw": f_objection_raw,
                        "retailer_objection_category": f_objection,
                        "follow_up_needed": f_followup,
                        "follow_up_priority": f_followup_p,
                        "follow_up_reason": f_followup_r,
                        "my_observation": f_obs,
                    }

                    new_df = pd.DataFrame([new_row])
                    if os.path.exists(RAW_CSV):
                        new_df.to_csv(RAW_CSV, mode="a", header=False, index=False)
                    else:
                        os.makedirs(os.path.dirname(RAW_CSV), exist_ok=True)
                        new_df.to_csv(RAW_CSV, index=False)

                    st.success(f"✅ Entry saved! {f_product} at {f_outlet_name} on {f_date}")
                    st.cache_data.clear()

    with tab_upload:
        st.markdown("### Upload CSV / Google Sheets Export")
        st.markdown("Upload a CSV file to **append** to your existing data. The file should match the field_sales_log column format.")
        st.markdown("**💡 Tip:** Export your Google Sheet as CSV and upload it here.")

        uploaded = st.file_uploader("Choose CSV file", type=["csv"])
        if uploaded:
            try:
                upload_df = pd.read_csv(uploaded)
                st.success(f"Loaded {len(upload_df)} rows from upload")
                st.dataframe(upload_df.head(10), use_container_width=True, hide_index=True)

                if st.button("✅ Append to Field Log", type="primary"):
                    if os.path.exists(RAW_CSV):
                        upload_df.to_csv(RAW_CSV, mode="a", header=False, index=False)
                    else:
                        os.makedirs(os.path.dirname(RAW_CSV), exist_ok=True)
                        upload_df.to_csv(RAW_CSV, index=False)
                    st.success(f"✅ {len(upload_df)} rows appended successfully!")
                    st.cache_data.clear()
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

        st.markdown("---")
        st.markdown("### 📋 Expected Column Format")
        st.markdown("Your CSV should contain these key columns (other columns are optional):")
        st.code("date, outlet_name, outlet_type, product_name, pitched, order_booked, pieces_ordered", language="text")


# ═══════════════════════════════════════════════
# PAGE 12: EXPORT REPORT (Improvement #8)
# ═══════════════════════════════════════════════
elif page == "📄 Export Report":
    st.markdown("""<div class="dashboard-header">
        <h1>📄 Export Report</h1>
        <p>Generate a downloadable, print-ready HTML report for your manager</p>
    </div>""", unsafe_allow_html=True)

    if not filtered.empty:
        st.markdown("### Report Preview")
        st.markdown("This generates a styled HTML report with KPIs, product performance, alerts, and recommendations.")

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Total Pitches", cov.get("total_pitches", 0))
        with c2: st.metric("Strike Rate", f"{conv.get('strike_rate', 0)}%")
        with c3: st.metric("Total Pieces", conv.get("total_pieces_ordered", 0))

        if st.button("📄 Generate HTML Report", type="primary", use_container_width=True):
            with st.spinner("Generating report..."):
                alerts = generate_alerts(filtered)
                recs = generate_recommendations(filtered)
                by_rule, _ = recommendation_summary(recs)
                prod_perf = product_performance_table(filtered)

                html_report = generate_html_report(
                    cov, conv, exec_k, prod_perf, objection_dist, alerts, by_rule
                )

            st.success("✅ Report generated!")
            st.download_button(
                "📥 Download HTML Report",
                data=html_report.encode("utf-8"),
                file_name=f"amul_sales_report_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True,
            )

            with st.expander("🔍 Preview Report"):
                st.components.v1.html(html_report, height=800, scrolling=True)
    else:
        st.info("Add field data first to generate a report.")
