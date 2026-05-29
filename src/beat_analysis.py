"""
Beat productivity analysis for the Amul Sales Dashboard.
Compares performance across different beats/routes.
"""

import pandas as pd


def beat_performance_table(df):
    """Calculate performance metrics by beat."""
    if df.empty or "beat_name" not in df.columns:
        return pd.DataFrame()

    pitched = df[df["pitched"] == "Yes"]

    stats = pitched.groupby("beat_name").agg(
        visit_days=("date", "nunique"),
        unique_outlets=("outlet_id", "nunique"),
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        avg_visibility=("visibility_score", "mean"),
        avg_interest=("interest_score", "mean"),
        scheme_yes=("scheme_explained", lambda x: (x == "Yes").sum()),
        competitor_yes=("competitor_present", lambda x: (x == "Yes").sum()),
        follow_ups=("follow_up_needed", lambda x: (x == "Yes").sum()),
    ).reset_index()

    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"] * 100, 1)
    stats["avg_pieces_per_order"] = round(stats["pieces"] / stats["orders"].replace(0, 1), 1)
    stats["pitches_per_day"] = round(stats["pitches"] / stats["visit_days"].replace(0, 1), 1)
    stats["orders_per_day"] = round(stats["orders"] / stats["visit_days"].replace(0, 1), 1)
    stats["scheme_pct"] = round(stats["scheme_yes"] / stats["pitches"] * 100, 1)
    stats["competitor_pct"] = round(stats["competitor_yes"] / stats["pitches"] * 100, 1)
    stats["avg_visibility"] = round(stats["avg_visibility"], 2)
    stats["avg_interest"] = round(stats["avg_interest"], 2)

    return stats.sort_values("conversion_pct", ascending=False)


def beat_product_matrix(df):
    """Product conversion rate by beat — shows which products work best on which routes."""
    if df.empty or "beat_name" not in df.columns:
        return pd.DataFrame()

    pitched = df[df["pitched"] == "Yes"]

    pivot = pitched.groupby(["beat_name", "product_name"]).agg(
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
    ).reset_index()

    pivot["conversion_pct"] = round(pivot["orders"] / pivot["pitches"] * 100, 1)

    matrix = pivot.pivot_table(
        index="beat_name",
        columns="product_name",
        values="conversion_pct",
        fill_value=0,
    )

    return matrix


def beat_daily_trend(df):
    """Daily trend by beat."""
    if df.empty or "beat_name" not in df.columns or "date" not in df.columns:
        return pd.DataFrame()

    daily = df.groupby(["date", "beat_name"]).agg(
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
    ).reset_index()

    daily["conversion_pct"] = round(daily["orders"] / daily["pitches"].replace(0, 1) * 100, 1)

    return daily


def beat_ranking(df):
    """Rank beats by a composite productivity score."""
    perf = beat_performance_table(df)
    if perf.empty:
        return pd.DataFrame()

    # Composite score: weighted combination of conversion, pieces/day, and interest
    perf["productivity_score"] = round(
        perf["conversion_pct"] * 0.4 +
        perf["orders_per_day"] * 3 +
        perf["avg_interest"] * 10 +
        perf["avg_pieces_per_order"] * 0.5,
        1
    )

    return perf.sort_values("productivity_score", ascending=False)
