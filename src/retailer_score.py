"""
Retailer relationship scoring for the Amul Sales Dashboard.
Tracks outlet health over time based on conversion, interest, and order patterns.
"""

import pandas as pd
import numpy as np


def calculate_retailer_scores(df):
    """
    Calculate a relationship health score for each outlet.

    Scoring components (0-100 scale):
    - Order frequency (30%): How often the outlet places orders
    - Conversion rate (25%): Pitch-to-order success rate
    - Interest trend (20%): Average interest level
    - Order volume (15%): Average pieces per visit
    - Engagement (10%): Follow-up responsiveness, scheme acceptance
    """
    if df.empty:
        return pd.DataFrame()

    pitched = df[df["pitched"] == "Yes"]

    outlet_stats = pitched.groupby(["outlet_id", "outlet_name"]).agg(
        outlet_type=("outlet_type", "first"),
        outlet_size=("outlet_size", "first"),
        total_visits=("date", "nunique"),
        total_pitches=("pitched", "count"),
        total_orders=("productive_call", "sum"),
        total_pieces=("pieces_ordered", "sum"),
        avg_interest=("interest_score", "mean"),
        avg_visibility=("visibility_score", "mean"),
        scheme_accepted=("scheme_explained", lambda x: (x == "Yes").sum()),
        high_interest_no_order=("high_interest_no_order", "sum"),
        first_visit=("date", "min"),
        last_visit=("date", "max"),
        unique_products_ordered=("successful_pitch", "sum"),
    ).reset_index()

    # --- Score Components ---

    # 1. Order frequency score (0-100)
    max_orders = outlet_stats["total_orders"].max()
    if max_orders > 0:
        outlet_stats["order_freq_score"] = round(
            outlet_stats["total_orders"] / max_orders * 100, 1
        )
    else:
        outlet_stats["order_freq_score"] = 0

    # 2. Conversion rate score (0-100)
    outlet_stats["conversion_rate"] = round(
        outlet_stats["total_orders"] / outlet_stats["total_pitches"] * 100, 1
    )
    outlet_stats["conversion_score"] = outlet_stats["conversion_rate"].clip(upper=100)

    # 3. Interest score (0-100)
    outlet_stats["interest_score_norm"] = round(
        outlet_stats["avg_interest"] / 3 * 100, 1
    )

    # 4. Volume score (0-100)
    max_pieces = outlet_stats["total_pieces"].max()
    if max_pieces > 0:
        outlet_stats["volume_score"] = round(
            outlet_stats["total_pieces"] / max_pieces * 100, 1
        )
    else:
        outlet_stats["volume_score"] = 0

    # 5. Engagement score (0-100)
    outlet_stats["scheme_rate"] = round(
        outlet_stats["scheme_accepted"] / outlet_stats["total_pitches"] * 100, 1
    )
    outlet_stats["engagement_score"] = round(
        outlet_stats["scheme_rate"] * 0.5 +
        outlet_stats["avg_visibility"] / 3 * 100 * 0.5,
        1
    )

    # --- Composite Score ---
    outlet_stats["relationship_score"] = round(
        outlet_stats["order_freq_score"] * 0.30 +
        outlet_stats["conversion_score"] * 0.25 +
        outlet_stats["interest_score_norm"] * 0.20 +
        outlet_stats["volume_score"] * 0.15 +
        outlet_stats["engagement_score"] * 0.10,
        1
    )

    # --- Health Status ---
    outlet_stats["health_status"] = outlet_stats["relationship_score"].apply(
        lambda x: "🟢 Strong" if x >= 60
        else "🟡 Growing" if x >= 35
        else "🔴 At Risk"
    )

    # --- Trend (based on first half vs second half of visits) ---
    outlet_stats["avg_interest"] = round(outlet_stats["avg_interest"], 2)

    return outlet_stats.sort_values("relationship_score", ascending=False)


def retailer_trend(df, outlet_id):
    """Calculate weekly trend for a specific outlet."""
    if df.empty:
        return pd.DataFrame()

    outlet_df = df[df["outlet_id"] == outlet_id]
    if outlet_df.empty or "week_no" not in outlet_df.columns:
        return pd.DataFrame()

    weekly = outlet_df.groupby("week_no").agg(
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        avg_interest=("interest_score", "mean"),
    ).reset_index()

    weekly["conversion_pct"] = round(weekly["orders"] / weekly["pitches"].replace(0, 1) * 100, 1)
    weekly["avg_interest"] = round(weekly["avg_interest"], 2)

    return weekly


def health_distribution(scores_df):
    """Get distribution of health statuses."""
    if scores_df.empty:
        return pd.DataFrame()

    dist = scores_df["health_status"].value_counts().reset_index()
    dist.columns = ["status", "count"]
    return dist
