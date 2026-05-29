"""
Outlet-level analysis for the Amul Sales Dashboard.
Outlet performance, opportunity identification, follow-up prioritization.
"""

import pandas as pd


def outlet_performance_table(df):
    """Comprehensive outlet performance table."""
    if df.empty:
        return pd.DataFrame()
    
    pitched = df[df["pitched"] == "Yes"]
    
    stats = pitched.groupby(["outlet_id", "outlet_name"]).agg(
        outlet_type=("outlet_type", "first"),
        outlet_size=("outlet_size", "first"),
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        unique_products_pitched=("product_name", "nunique"),
        unique_products_ordered=("successful_pitch", lambda x: x.sum()),
        avg_interest=("interest_score", "mean"),
        high_interest_no_order=("high_interest_no_order", "sum"),
        visit_days=("date", "nunique"),
    ).reset_index()
    
    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"] * 100, 1)
    stats["avg_pieces_per_order"] = round(stats["pieces"] / stats["orders"].replace(0, 1), 1)
    stats["avg_interest"] = round(stats["avg_interest"], 2)
    
    # Range selling: products ordered / products pitched
    stats["range_selling_pct"] = round(
        stats["unique_products_ordered"] / stats["unique_products_pitched"] * 100, 1
    )
    
    return stats.sort_values("pieces", ascending=False)


def outlet_type_comparison(df):
    """Compare conversion and performance by outlet type."""
    if df.empty:
        return pd.DataFrame()
    
    pitched = df[df["pitched"] == "Yes"]
    
    stats = pitched.groupby("outlet_type").agg(
        unique_outlets=("outlet_id", "nunique"),
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        avg_visibility=("visibility_score", "mean"),
        avg_interest=("interest_score", "mean"),
        competitor_count=("competitor_present", lambda x: (x == "Yes").sum()),
    ).reset_index()
    
    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"] * 100, 1)
    stats["avg_pieces_per_order"] = round(stats["pieces"] / stats["orders"].replace(0, 1), 1)
    stats["avg_visibility"] = round(stats["avg_visibility"], 2)
    stats["avg_interest"] = round(stats["avg_interest"], 2)
    stats["competitor_pct"] = round(stats["competitor_count"] / stats["pitches"] * 100, 1)
    
    return stats.sort_values("conversion_pct", ascending=False)


def opportunity_outlets(df, min_interest=2, max_orders=2):
    """Find outlets with high interest but low orders — key opportunity signal."""
    if df.empty:
        return pd.DataFrame()
    
    outlet_stats = df.groupby(["outlet_id", "outlet_name"]).agg(
        outlet_type=("outlet_type", "first"),
        outlet_size=("outlet_size", "first"),
        total_pitches=("pitched", lambda x: (x == "Yes").sum()),
        total_orders=("productive_call", "sum"),
        avg_interest=("interest_score", "mean"),
        high_interest_no_order=("high_interest_no_order", "sum"),
        top_product=("product_name", lambda x: x.value_counts().index[0]),
    ).reset_index()
    
    # Filter: high average interest but few orders
    opportunities = outlet_stats[
        (outlet_stats["avg_interest"] >= min_interest) &
        (outlet_stats["total_orders"] <= max_orders) &
        (outlet_stats["high_interest_no_order"] > 0)
    ].sort_values("high_interest_no_order", ascending=False)
    
    opportunities["avg_interest"] = round(opportunities["avg_interest"], 2)
    
    return opportunities


def follow_up_priority_table(df):
    """Generate a prioritized follow-up table."""
    if df.empty:
        return pd.DataFrame()
    
    followup = df[df["follow_up_needed"] == "Yes"].copy()
    
    if followup.empty:
        return pd.DataFrame()
    
    result = followup.groupby(["outlet_id", "outlet_name", "product_name"]).agg(
        outlet_type=("outlet_type", "first"),
        interest_level=("retailer_interest_level", "first"),
        objection=("retailer_objection_category", "first"),
        priority=("follow_up_priority", "first"),
        reason=("follow_up_reason", "first"),
        observation=("my_observation", "first"),
        last_visit=("date", "max"),
    ).reset_index()
    
    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2, "": 3}
    result["priority_rank"] = result["priority"].map(priority_order).fillna(3)
    result = result.sort_values("priority_rank").drop(columns=["priority_rank"])
    
    return result
