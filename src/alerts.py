"""
Alert and anomaly detection for the Amul Sales Dashboard.
Identifies significant changes, opportunities, and risks.
"""

import pandas as pd


def generate_alerts(df):
    """
    Generate contextual alerts based on the dataset.
    Returns a list of alert dicts with type, severity, message.
    """
    if df.empty:
        return []

    alerts = []
    pitched = df[df["pitched"] == "Yes"]
    total_pitches = len(pitched)
    orders = df[df["order_booked"] == "Yes"]

    if total_pitches == 0:
        return [{"type": "info", "severity": "low", "icon": "ℹ️", "message": "No pitch data available yet."}]

    overall_conv = len(orders) / total_pitches * 100

    # --- Product-level alerts ---
    prod_stats = pitched.groupby("product_name").agg(
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
    ).reset_index()
    prod_stats["conv"] = round(prod_stats["orders"] / prod_stats["pitches"] * 100, 1)

    # Best product alert
    best = prod_stats.loc[prod_stats["conv"].idxmax()]
    alerts.append({
        "type": "success",
        "severity": "info",
        "icon": "🏆",
        "message": f"**{best['product_name']}** is your top converter at **{best['conv']}%** — focus more effort here",
    })

    # Worst product alert
    worst = prod_stats.loc[prod_stats["conv"].idxmin()]
    if worst["conv"] < 30:
        alerts.append({
            "type": "warning",
            "severity": "medium",
            "icon": "⚠️",
            "message": f"**{worst['product_name']}** has low conversion ({worst['conv']}%) — review pitch strategy or outlet targeting",
        })

    # --- Week-over-week alerts (if multiple weeks) ---
    if "week_no" in df.columns and df["week_no"].nunique() >= 2:
        weeks = sorted(df["week_no"].unique())
        latest = weeks[-1]
        previous = weeks[-2]

        latest_df = pitched[pitched["week_no"] == latest]
        prev_df = pitched[pitched["week_no"] == previous]

        if len(latest_df) > 0 and len(prev_df) > 0:
            latest_conv = latest_df["productive_call"].sum() / len(latest_df) * 100
            prev_conv = prev_df["productive_call"].sum() / len(prev_df) * 100
            change = latest_conv - prev_conv

            if change >= 5:
                alerts.append({
                    "type": "success",
                    "severity": "info",
                    "icon": "📈",
                    "message": f"Conversion **improved +{change:.1f}pp** from Week {previous} to Week {latest} — keep this momentum!",
                })
            elif change <= -5:
                alerts.append({
                    "type": "danger",
                    "severity": "high",
                    "icon": "📉",
                    "message": f"Conversion **dropped {change:.1f}pp** from Week {previous} to Week {latest} — investigate what changed",
                })

            # Pieces trend
            latest_pcs = latest_df["pieces_ordered"].sum()
            prev_pcs = prev_df["pieces_ordered"].sum()
            if prev_pcs > 0:
                pcs_change = (latest_pcs - prev_pcs) / prev_pcs * 100
                if pcs_change >= 20:
                    alerts.append({
                        "type": "success",
                        "severity": "info",
                        "icon": "📦",
                        "message": f"Pieces ordered **up {pcs_change:.0f}%** week-over-week ({int(prev_pcs)} → {int(latest_pcs)})",
                    })
                elif pcs_change <= -20:
                    alerts.append({
                        "type": "warning",
                        "severity": "medium",
                        "icon": "📦",
                        "message": f"Pieces ordered **down {abs(pcs_change):.0f}%** week-over-week ({int(prev_pcs)} → {int(latest_pcs)})",
                    })

    # --- Execution gap alerts ---
    if "availability_before_pitch" in df.columns:
        avail_pct = (pitched["availability_before_pitch"] == "Yes").sum() / total_pitches * 100
        if avail_pct < 50:
            alerts.append({
                "type": "danger",
                "severity": "high",
                "icon": "🚨",
                "message": f"Product availability before pitch is only **{avail_pct:.0f}%** — major distribution gap, coordinate with distributor",
            })

    if "scheme_explained" in df.columns:
        scheme_pct = (pitched["scheme_explained"] == "Yes").sum() / total_pitches * 100
        if scheme_pct < 50:
            alerts.append({
                "type": "warning",
                "severity": "medium",
                "icon": "💬",
                "message": f"Scheme explained in only **{scheme_pct:.0f}%** of pitches — opportunity to improve by explaining schemes consistently",
            })

    # --- Competitor surge alert ---
    if "competitor_present" in df.columns:
        comp_pct = (pitched["competitor_present"] == "Yes").sum() / total_pitches * 100
        if comp_pct > 50:
            alerts.append({
                "type": "warning",
                "severity": "medium",
                "icon": "⚔️",
                "message": f"Competitor presence is high at **{comp_pct:.0f}%** — strengthen competitive positioning",
            })

    # --- High interest no order alert ---
    if "high_interest_no_order" in df.columns:
        hino = df["high_interest_no_order"].sum()
        if hino > 10:
            alerts.append({
                "type": "warning",
                "severity": "high",
                "icon": "🎯",
                "message": f"**{int(hino)} cases** of high retailer interest but no order — this is your biggest near-term opportunity",
            })

    # --- Product with high pitch but low conversion ---
    for _, row in prod_stats.iterrows():
        if row["pitches"] >= 20 and row["conv"] < 25:
            alerts.append({
                "type": "warning",
                "severity": "medium",
                "icon": "🔄",
                "message": f"**{row['product_name']}** has {int(row['pitches'])} pitches but only {row['conv']}% conversion — reconsider pitch script or outlet mix",
            })

    return alerts


def format_alert_html(alert):
    """Format a single alert as styled HTML."""
    colors = {
        "success": {"bg": "rgba(16,185,129,0.1)", "border": "#10B981", "text": "#34D399"},
        "warning": {"bg": "rgba(245,158,11,0.1)", "border": "#F59E0B", "text": "#FBBF24"},
        "danger": {"bg": "rgba(239,68,68,0.1)", "border": "#EF4444", "text": "#F87171"},
        "info": {"bg": "rgba(99,102,241,0.1)", "border": "#6366F1", "text": "#A5B4FC"},
    }
    c = colors.get(alert["type"], colors["info"])

    return f"""
    <div style="
        background: {c['bg']};
        border-left: 4px solid {c['border']};
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        color: {c['text']};
    ">
        {alert['icon']} {alert['message']}
    </div>
    """
