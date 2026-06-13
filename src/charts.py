"""
Plotly chart functions for the Amul Sales Dashboard.
Consistent dark theme with FMCG-appropriate color system.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- Color Palette ---
COLORS = {
    # Airbnb Brand Tokens
    "primary": "#ff385c", # Rausch
    "primary_active": "#e00b41",
    "ink": "#222222",
    "body": "#3f3f3f",
    "muted": "#6a6a6a",
    "hairline": "#dddddd",
    "hairline_soft": "#ebebeb",
    "canvas": "#ffffff",
    "surface": "#f7f7f7",
    
    # Legacy fallbacks mapped to new system
    "green": "#10B981", # Kept for positive deltas
    "red": "#c13515",   # Airbnb Error Red
    "orange": "#ffb200",
    "blue": "#428bff",  # Airbnb Legal Blue
    "purple": "#ff385c",# Map to primary
    "indigo": "#ff385c",# Map to primary
    "slate": "#6a6a6a",
    
    # Layout mappings
    "bg": "#ffffff",
    "card_bg": "#ffffff",
    "text": "#222222",
    "text_muted": "#6a6a6a",
    "grid": "#ebebeb",
}

PRODUCT_COLORS = [
    "#ff385c", "#222222", "#428bff", "#10B981",
    "#ffb200", "#c13515", "#6a6a6a", "#e00b41",
]

# --- Common layout ---
def _base_layout(title="", height=400, margin=None):
    """Base layout for all charts."""
    if margin is None:
        margin = dict(l=20, r=20, t=50, b=20)
    
    return dict(
        title=dict(text=title, font=dict(size=16, color=COLORS["ink"], family="'Airbnb Cereal App', 'Airbnb Cereal VF', 'Circular', -apple-system, sans-serif", weight="bold"), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="'Airbnb Cereal App', 'Airbnb Cereal VF', 'Circular', -apple-system, sans-serif", size=14),
        height=height,
        margin=margin,
        xaxis=dict(
            gridcolor=COLORS["grid"],
            gridwidth=1,
            zerolinecolor=COLORS["grid"],
            showline=False,
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            gridwidth=1,
            zerolinecolor=COLORS["grid"],
            showline=False,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["muted"]),
        ),
        hoverlabel=dict(
            bgcolor=COLORS["card_bg"],
            font=dict(color=COLORS["ink"]),
            bordercolor=COLORS["hairline"],
        ),
    )


# --- KPI Card (returns HTML) ---
def kpi_card_html(label, value, subtitle="", delta=None, color=None):
    """Generate HTML for a styled KPI card matching Airbnb aesthetics."""
    if color is None:
        color = COLORS["primary"]
    
    delta_html = ""
    if delta is not None:
        delta_color = COLORS["green"] if delta >= 0 else COLORS["red"]
        delta_icon = "↑" if delta >= 0 else "↓"
        delta_html = f'<span style="color:{delta_color}; font-size:14px; font-weight:600; margin-left:6px;">{delta_icon} {abs(delta):.1f}%</span>'
    
    return f"""<div style="background: {COLORS['canvas']}; border: 1px solid {COLORS['hairline']}; border-radius: 14px; padding: 24px; box-shadow: rgba(0, 0, 0, 0.02) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 6px 0; display: flex; flex-direction: column; justify-content: center; min-height: 120px; width: 100%;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
<div style="color:{COLORS['ink']}; font-size:16px; font-weight:600; font-family: 'Airbnb Cereal App', 'Airbnb Cereal VF', 'Circular', -apple-system, sans-serif;">{label}</div>
<div style="color: {color}; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: {COLORS['surface']};"><div style="background-color: {color}; width: 8px; height: 8px; border-radius: 50%;"></div></div>
</div>
<div style="color:{COLORS['ink']}; font-size:28px; font-weight:700; line-height:1.2; font-family: 'Airbnb Cereal App', 'Airbnb Cereal VF', 'Circular', -apple-system, sans-serif; margin-bottom:4px;">{value}</div>
<div style="color:{COLORS['muted']}; font-size:14px; font-weight:400; font-family: 'Airbnb Cereal App', 'Airbnb Cereal VF', 'Circular', -apple-system, sans-serif;">{subtitle} {delta_html}</div>
</div>"""


# --- Line Charts ---
def daily_pitches_vs_orders(daily_df):
    """Dual-line chart: daily pitches vs orders with area fill."""
    if daily_df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_df["date"], y=daily_df["pitches"],
        name="Pitches", mode="lines+markers",
        line=dict(color=COLORS["blue"], width=2),
        marker=dict(size=6, color=COLORS["blue"]),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.1)",
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_df["date"], y=daily_df["orders"],
        name="Orders", mode="lines+markers",
        line=dict(color=COLORS["green"], width=2),
        marker=dict(size=6, color=COLORS["green"]),
        fill="tozeroy", fillcolor="rgba(16,185,129,0.1)",
    ))
    
    fig.update_layout(**_base_layout("Daily Pitches vs Orders", height=350))
    fig.update_xaxes(tickformat="%b %d")
    
    return fig


def daily_conversion_trend(daily_df):
    """Line chart of daily conversion rate."""
    if daily_df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_df["date"], y=daily_df["conversion_rate"],
        mode="lines+markers",
        line=dict(color=COLORS["purple"], width=2.5),
        marker=dict(size=7, color=COLORS["purple"]),
        fill="tozeroy", fillcolor="rgba(139,92,246,0.1)",
        name="Conversion %",
    ))
    
    fig.update_layout(**_base_layout("Daily Conversion Rate (%)", height=300))
    fig.update_xaxes(tickformat="%b %d")
    fig.update_yaxes(ticksuffix="%")
    
    return fig


# --- Bar Charts ---
def product_conversion_bar(product_df, metric="conversion_pct"):
    """Horizontal bar chart: product conversion rates."""
    if product_df.empty:
        return go.Figure()
    
    df = product_df.sort_values(metric, ascending=True)
    
    colors = [COLORS["green"] if v >= 40 else COLORS["orange"] if v >= 25 else COLORS["red"]
              for v in df[metric]]
    
    fig = go.Figure(go.Bar(
        y=df["product_name"],
        x=df[metric],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=4,
        ),
        text=[f"{v:.1f}%" for v in df[metric]],
        textposition="auto",
        textfont=dict(color="white", size=12, family="Inter"),
    ))
    
    layout = _base_layout("Conversion Rate by Product (%)", height=max(300, len(df) * 50))
    layout["yaxis"]["categoryorder"] = "total ascending"
    fig.update_layout(**layout)
    
    return fig


def pitches_vs_orders_stacked(product_df):
    """Stacked bar: pitches vs successful orders by product."""
    if product_df.empty:
        return go.Figure()
    
    df = product_df.sort_values("pitches", ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df["product_name"],
        x=df["orders"],
        orientation="h",
        name="Orders",
        marker=dict(color=COLORS["green"], cornerradius=4),
    ))
    
    fig.add_trace(go.Bar(
        y=df["product_name"],
        x=df["pitches"] - df["orders"],
        orientation="h",
        name="No Order",
        marker=dict(color=COLORS["red"], opacity=0.4, cornerradius=4),
    ))
    
    layout = _base_layout("Pitches vs Orders by Product", height=max(300, len(df) * 50))
    layout["barmode"] = "stack"
    fig.update_layout(**layout)
    
    return fig


def outlet_type_conversion_bar(otype_df):
    """Horizontal bar: conversion by outlet type."""
    if otype_df.empty:
        return go.Figure()
    
    df = otype_df.sort_values("conversion_pct", ascending=True)
    
    colors = [COLORS["green"] if v >= 40 else COLORS["orange"] if v >= 25 else COLORS["red"]
              for v in df["conversion_pct"]]
    
    fig = go.Figure(go.Bar(
        y=df["outlet_type"],
        x=df["conversion_pct"],
        orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:.1f}%" for v in df["conversion_pct"]],
        textposition="auto",
        textfont=dict(color="white", size=12),
    ))
    
    layout = _base_layout("Conversion by Outlet Type (%)", height=max(280, len(df) * 50))
    fig.update_layout(**layout)
    
    return fig


def objection_distribution_bar(objection_df):
    """Horizontal bar chart of objection categories."""
    if objection_df.empty:
        return go.Figure()
    
    df = objection_df.sort_values("count", ascending=True).tail(10)
    
    fig = go.Figure(go.Bar(
        y=df["objection"],
        x=df["count"],
        orientation="h",
        marker=dict(
            color=COLORS["orange"],
            opacity=0.85,
            cornerradius=4,
        ),
        text=[f"{int(v)}" for v in df["count"]],
        textposition="auto",
        textfont=dict(color="white", size=12),
    ))
    
    layout = _base_layout("Top Objection Categories", height=max(300, len(df) * 45))
    fig.update_layout(**layout)
    
    return fig


# --- Heatmaps ---
def product_objection_heatmap(matrix_df):
    """Annotated heatmap: product × objection category."""
    if matrix_df.empty:
        return go.Figure()
    
    fig = go.Figure(go.Heatmap(
        z=matrix_df.values,
        x=matrix_df.columns.tolist(),
        y=matrix_df.index.tolist(),
        colorscale=[
            [0, "rgba(99,102,241,0.05)"],
            [0.25, "rgba(245,158,11,0.3)"],
            [0.5, "rgba(245,158,11,0.5)"],
            [0.75, "rgba(239,68,68,0.6)"],
            [1, "rgba(239,68,68,0.9)"],
        ],
        text=matrix_df.values,
        texttemplate="%{text}",
        textfont=dict(size=11, color=COLORS["text"]),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(title="Count", tickfont=dict(color=COLORS["text_muted"])),
    ))
    
    layout = _base_layout(
        "Product × Objection Heatmap",
        height=max(350, len(matrix_df) * 50),
        margin=dict(l=20, r=20, t=50, b=100),
    )
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    
    return fig


def product_outlet_matrix_heatmap(matrix_df):
    """Heatmap: product × outlet type conversion rate."""
    if matrix_df.empty:
        return go.Figure()
    
    fig = go.Figure(go.Heatmap(
        z=matrix_df.values,
        x=matrix_df.columns.tolist(),
        y=matrix_df.index.tolist(),
        colorscale=[
            [0, "rgba(239,68,68,0.2)"],
            [0.3, "rgba(245,158,11,0.4)"],
            [0.6, "rgba(16,185,129,0.5)"],
            [1, "rgba(16,185,129,0.9)"],
        ],
        text=[[f"{v:.0f}%" for v in row] for row in matrix_df.values],
        texttemplate="%{text}",
        textfont=dict(size=11, color=COLORS["text"]),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(title="Conv %", tickfont=dict(color=COLORS["text_muted"])),
    ))
    
    layout = _base_layout(
        "Product-Outlet Fit Matrix (Conversion %)",
        height=max(350, len(matrix_df) * 50),
        margin=dict(l=20, r=20, t=50, b=100),
    )
    layout["xaxis"]["tickangle"] = -45
    fig.update_layout(**layout)
    
    return fig


# --- Scatter Plots ---
def outlet_scatter(outlet_df):
    """Scatter plot: pitches vs orders by outlet."""
    if outlet_df.empty:
        return go.Figure()
    
    fig = px.scatter(
        outlet_df,
        x="pitches",
        y="orders",
        size="pieces",
        color="outlet_type",
        hover_name="outlet_name",
        hover_data=["conversion_pct", "avg_interest"],
        color_discrete_sequence=PRODUCT_COLORS,
        size_max=25,
    )
    
    fig.update_layout(**_base_layout("Outlet Pitches vs Orders", height=400))
    
    return fig


# --- Funnel Chart ---
def execution_funnel(funnel_dict):
    """Funnel chart: visited → pitched → interested → ordered."""
    if not funnel_dict:
        return go.Figure()
    
    stages = list(funnel_dict.keys())
    values = list(funnel_dict.values())
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        textfont=dict(color="white", size=13),
        marker=dict(
            color=[COLORS["blue"], COLORS["purple"], COLORS["orange"], COLORS["green"], COLORS["green_light"]],
            line=dict(width=1, color=COLORS["grid"]),
        ),
        connector=dict(line=dict(color=COLORS["grid"], width=1)),
    ))
    
    layout = _base_layout("Sales Funnel: Visit → Order", height=380)
    layout["funnelmode"] = "stack"
    fig.update_layout(**layout)
    
    return fig


# --- Grouped Bar for Factors ---
def conversion_by_factor(df, factor_col, title=""):
    """Grouped bar: conversion rate by a categorical factor (visibility, scheme, etc.)."""
    if df.empty or factor_col not in df.columns:
        return go.Figure()
    
    pitched = df[df["pitched"] == "Yes"]
    
    stats = pitched.groupby(factor_col).agg(
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
    ).reset_index()
    
    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"] * 100, 1)
    
    # Order levels
    level_order = {"No": 0, "Yes": 1, "Low": 0, "Medium": 1, "High": 2}
    stats["sort_key"] = stats[factor_col].map(level_order).fillna(0)
    stats = stats.sort_values("sort_key")
    
    colors = [COLORS["red"] if v < 25 else COLORS["orange"] if v < 40 else COLORS["green"]
              for v in stats["conversion_pct"]]
    
    fig = go.Figure(go.Bar(
        x=stats[factor_col],
        y=stats["conversion_pct"],
        marker=dict(color=colors, cornerradius=6),
        text=[f"{v:.1f}%" for v in stats["conversion_pct"]],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=12),
    ))
    
    layout = _base_layout(title or f"Conversion by {factor_col}", height=320)
    fig.update_layout(**layout)
    fig.update_yaxes(ticksuffix="%")
    
    return fig


# --- Recommendation Priority Donut ---
def recommendation_priority_donut(by_priority_df):
    """Donut chart for recommendation priority distribution."""
    if by_priority_df.empty:
        return go.Figure()
    
    color_map = {"High": COLORS["red"], "Medium": COLORS["orange"], "Low": COLORS["green"]}
    colors = [color_map.get(p, COLORS["slate"]) for p in by_priority_df["priority"]]
    
    fig = go.Figure(go.Pie(
        labels=by_priority_df["priority"],
        values=by_priority_df["count"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=COLORS["card_bg"], width=2)),
        textinfo="label+value",
        textfont=dict(color="white", size=13),
    ))
    
    layout = _base_layout("Recommendations by Priority", height=320)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)
    fig.update_layout(**layout)
    
    return fig


# ──────────────────────────────────────────────────
# V2 Charts — Improvements
# ──────────────────────────────────────────────────

def weekly_comparison_bar(weekly_df):
    """Grouped bar chart comparing metrics across weeks."""
    if weekly_df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[f"Week {int(w)}" for w in weekly_df["week_no"]],
        y=weekly_df["pitches"],
        name="Pitches",
        marker=dict(color=COLORS["blue"], cornerradius=4),
    ))
    fig.add_trace(go.Bar(
        x=[f"Week {int(w)}" for w in weekly_df["week_no"]],
        y=weekly_df["orders"],
        name="Orders",
        marker=dict(color=COLORS["green"], cornerradius=4),
    ))

    layout = _base_layout("Week-over-Week: Pitches vs Orders", height=350)
    layout["barmode"] = "group"
    fig.update_layout(**layout)

    return fig


def weekly_conversion_line(weekly_df):
    """Line chart of weekly conversion rate trend."""
    if weekly_df.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[f"Week {int(w)}" for w in weekly_df["week_no"]],
        y=weekly_df["conversion_pct"],
        mode="lines+markers+text",
        line=dict(color=COLORS["purple"], width=3),
        marker=dict(size=10, color=COLORS["purple"]),
        text=[f"{v:.1f}%" for v in weekly_df["conversion_pct"]],
        textposition="top center",
        textfont=dict(color=COLORS["text"], size=12),
        fill="tozeroy",
        fillcolor="rgba(139,92,246,0.08)",
        name="Conversion %",
    ))

    layout = _base_layout("Weekly Conversion Rate Trend", height=320)
    fig.update_layout(**layout)
    fig.update_yaxes(ticksuffix="%")

    return fig


def weekly_pieces_bar(weekly_df):
    """Bar chart of weekly pieces ordered."""
    if weekly_df.empty:
        return go.Figure()

    colors = [COLORS["green"] if v >= weekly_df["pieces"].mean() else COLORS["orange"]
              for v in weekly_df["pieces"]]

    fig = go.Figure(go.Bar(
        x=[f"Week {int(w)}" for w in weekly_df["week_no"]],
        y=weekly_df["pieces"],
        marker=dict(color=colors, cornerradius=6),
        text=[f"{int(v)}" for v in weekly_df["pieces"]],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=13, weight="bold"),
    ))

    layout = _base_layout("Weekly Pieces Ordered", height=320)
    fig.update_layout(**layout)

    return fig


def beat_conversion_bar(beat_df):
    """Horizontal bar: conversion by beat/route."""
    if beat_df.empty:
        return go.Figure()

    df = beat_df.sort_values("conversion_pct", ascending=True)

    colors = [COLORS["green"] if v >= 45 else COLORS["orange"] if v >= 30 else COLORS["red"]
              for v in df["conversion_pct"]]

    fig = go.Figure(go.Bar(
        y=df["beat_name"],
        x=df["conversion_pct"],
        orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:.1f}%" for v in df["conversion_pct"]],
        textposition="auto",
        textfont=dict(color="white", size=12),
    ))

    layout = _base_layout("Conversion Rate by Beat/Route (%)", height=max(250, len(df) * 60))
    fig.update_layout(**layout)

    return fig


def beat_productivity_scatter(beat_df):
    """Scatter: beat productivity — pitches/day vs conversion."""
    if beat_df.empty:
        return go.Figure()

    fig = go.Figure(go.Scatter(
        x=beat_df["pitches_per_day"],
        y=beat_df["conversion_pct"],
        mode="markers+text",
        marker=dict(
            size=beat_df["pieces"].clip(lower=1) / beat_df["pieces"].max() * 40 + 10,
            color=PRODUCT_COLORS[:len(beat_df)],
            line=dict(width=1, color=COLORS["grid"]),
        ),
        text=beat_df["beat_name"],
        textposition="top center",
        textfont=dict(color=COLORS["text"], size=11),
    ))

    layout = _base_layout("Beat Productivity: Activity vs Conversion", height=380)
    layout["xaxis"]["title"] = "Pitches per Day"
    layout["yaxis"]["title"] = "Conversion %"
    fig.update_layout(**layout)

    return fig


def retailer_health_donut(health_dist_df):
    """Donut chart: retailer health distribution."""
    if health_dist_df.empty:
        return go.Figure()

    color_map = {
        "🟢 Strong": COLORS["green"],
        "🟡 Growing": COLORS["orange"],
        "🔴 At Risk": COLORS["red"],
    }
    colors = [color_map.get(s, COLORS["slate"]) for s in health_dist_df["status"]]

    fig = go.Figure(go.Pie(
        labels=health_dist_df["status"],
        values=health_dist_df["count"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=COLORS["card_bg"], width=2)),
        textinfo="label+value",
        textfont=dict(color="white", size=13),
    ))

    layout = _base_layout("Retailer Health Distribution", height=320)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)
    fig.update_layout(**layout)

    return fig


def retailer_score_bar(scores_df, top_n=15):
    """Horizontal bar: retailer relationship scores."""
    if scores_df.empty:
        return go.Figure()

    df = scores_df.head(top_n).sort_values("relationship_score", ascending=True)

    colors = [COLORS["green"] if v >= 60 else COLORS["orange"] if v >= 35 else COLORS["red"]
              for v in df["relationship_score"]]

    fig = go.Figure(go.Bar(
        y=df["outlet_name"],
        x=df["relationship_score"],
        orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:.0f}" for v in df["relationship_score"]],
        textposition="auto",
        textfont=dict(color="white", size=11),
    ))

    layout = _base_layout("Retailer Relationship Scores", height=max(350, len(df) * 38))
    fig.update_layout(**layout)

    return fig


def competitor_brand_bar(comp_df):
    """Horizontal bar: competitor brand frequency."""
    if comp_df.empty:
        return go.Figure()

    df = comp_df.sort_values("occurrences", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["competitor_brand"],
        x=df["won_orders"],
        orientation="h",
        name="Amul Won",
        marker=dict(color=COLORS["green"], cornerradius=4),
    ))
    fig.add_trace(go.Bar(
        y=df["competitor_brand"],
        x=df["blocked_orders"],
        orientation="h",
        name="Amul Lost",
        marker=dict(color=COLORS["red"], opacity=0.6, cornerradius=4),
    ))

    layout = _base_layout("Competitor Impact: Orders Won vs Lost", height=max(300, len(df) * 50))
    layout["barmode"] = "stack"
    fig.update_layout(**layout)

    return fig


def competitor_exposure_bar(comp_product_df):
    """Bar chart: competitor exposure by Amul product."""
    if comp_product_df.empty:
        return go.Figure()

    df = comp_product_df.sort_values("competitor_exposure_pct", ascending=True)

    fig = go.Figure(go.Bar(
        y=df["product_name"],
        x=df["competitor_exposure_pct"],
        orientation="h",
        marker=dict(color=COLORS["red"], opacity=0.7, cornerradius=4),
        text=[f"{v:.0f}%" for v in df["competitor_exposure_pct"]],
        textposition="auto",
        textfont=dict(color="white", size=12),
    ))

    layout = _base_layout("Competitor Exposure by Amul Product (%)", height=max(300, len(df) * 50))
    fig.update_layout(**layout)

    return fig


def target_progress_html(achievement_df):
    """Generate HTML progress bars for target vs achievement."""
    if achievement_df.empty:
        return "<p style='color:#94a3b8;'>No data for this period.</p>"

    html = ""
    for _, row in achievement_df.iterrows():
        pct = min(row["achievement_pct"], 100)
        bar_color = COLORS["green"] if pct >= 100 else COLORS["orange"] if pct >= 70 else COLORS["red"]
        overflow = f" ({row['achievement_pct']:.0f}%)" if row["achievement_pct"] > 100 else ""

        html += f"""
        <div style="margin-bottom: 14px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:{COLORS['text']}; font-size:0.85rem; font-weight:600;">
                    {row['status']} {row['metric']}
                </span>
                <span style="color:{COLORS['text_muted']}; font-size:0.8rem;">
                    {row['actual']} / {row['target']}{overflow}
                </span>
            </div>
            <div style="
                background: {COLORS['grid']};
                border-radius: 6px;
                height: 10px;
                overflow: hidden;
            ">
                <div style="
                    background: {bar_color};
                    width: {pct}%;
                    height: 100%;
                    border-radius: 6px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """

    return html


def scheme_effectiveness_chart(df):
    """Side-by-side bar: conversion with vs without scheme explained, by product."""
    if df.empty:
        return go.Figure()

    pitched = df[df["pitched"] == "Yes"]

    with_scheme = pitched[pitched["scheme_explained"] == "Yes"].groupby("product_name").agg(
        pitches=("pitched", "count"), orders=("productive_call", "sum"),
    ).reset_index()
    with_scheme["conv"] = round(with_scheme["orders"] / with_scheme["pitches"] * 100, 1)

    without_scheme = pitched[pitched["scheme_explained"] == "No"].groupby("product_name").agg(
        pitches=("pitched", "count"), orders=("productive_call", "sum"),
    ).reset_index()
    without_scheme["conv"] = round(without_scheme["orders"] / without_scheme["pitches"] * 100, 1)

    merged = with_scheme[["product_name", "conv"]].rename(columns={"conv": "with_scheme"}).merge(
        without_scheme[["product_name", "conv"]].rename(columns={"conv": "without_scheme"}),
        on="product_name", how="outer"
    ).fillna(0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=merged["product_name"], y=merged["with_scheme"],
        name="Scheme Explained", marker=dict(color=COLORS["green"], cornerradius=4),
    ))
    fig.add_trace(go.Bar(
        x=merged["product_name"], y=merged["without_scheme"],
        name="No Scheme", marker=dict(color=COLORS["red"], opacity=0.5, cornerradius=4),
    ))

    layout = _base_layout("Scheme Effectiveness: Conversion With vs Without (%)", height=380)
    layout["barmode"] = "group"
    layout["xaxis"]["tickangle"] = -30
    fig.update_layout(**layout)
    fig.update_yaxes(ticksuffix="%")

    return fig
