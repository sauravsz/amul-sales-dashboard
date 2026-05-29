"""
Product-level analysis for the Amul Sales Dashboard.
Product performance, product-outlet fit, product-objection analysis.
"""

import pandas as pd


def product_performance_table(df):
    """Comprehensive product performance table."""
    if df.empty:
        return pd.DataFrame()
    
    pitched = df[df["pitched"] == "Yes"]
    
    stats = pitched.groupby("product_name").agg(
        product_group=("product_group", "first"),
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        avg_visibility=("visibility_score", "mean"),
        avg_interest=("interest_score", "mean"),
        scheme_yes=("scheme_explained", lambda x: (x == "Yes").sum()),
        availability_yes=("availability_before_pitch", lambda x: (x == "Yes").sum()),
        competitor_yes=("competitor_present", lambda x: (x == "Yes").sum()),
        high_interest_no_order=("high_interest_no_order", "sum"),
    ).reset_index()
    
    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"] * 100, 1)
    stats["avg_order_size"] = round(stats["pieces"] / stats["orders"].replace(0, 1), 1)
    stats["scheme_pct"] = round(stats["scheme_yes"] / stats["pitches"] * 100, 1)
    stats["availability_pct"] = round(stats["availability_yes"] / stats["pitches"] * 100, 1)
    stats["competitor_pct"] = round(stats["competitor_yes"] / stats["pitches"] * 100, 1)
    stats["avg_visibility"] = round(stats["avg_visibility"], 2)
    stats["avg_interest"] = round(stats["avg_interest"], 2)
    
    return stats.sort_values("conversion_pct", ascending=False)


def product_objection_matrix(df):
    """Create product × objection category matrix."""
    if df.empty:
        return pd.DataFrame()
    
    no_order = df[(df["order_booked"] == "No") & (df["retailer_objection_category"] != "")]
    
    if no_order.empty:
        return pd.DataFrame()
    
    matrix = pd.crosstab(
        no_order["product_name"],
        no_order["retailer_objection_category"],
        margins=False
    )
    
    return matrix


def product_outlet_fit_matrix(df):
    """Create product × outlet_type conversion rate matrix."""
    if df.empty:
        return pd.DataFrame()
    
    pitched = df[df["pitched"] == "Yes"]
    
    # Calculate conversion rate for each product-outlet combination
    pivot = pitched.groupby(["product_name", "outlet_type"]).agg(
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
    ).reset_index()
    
    pivot["conversion_pct"] = round(pivot["orders"] / pivot["pitches"] * 100, 1)
    
    matrix = pivot.pivot_table(
        index="product_name",
        columns="outlet_type",
        values="conversion_pct",
        fill_value=0,
    )
    
    return matrix


def product_daily_trend(df, product_name=None):
    """Daily trend for a specific product or all products."""
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()
    
    data = df.copy()
    if product_name:
        data = data[data["product_name"] == product_name]
    
    daily = data.groupby(["date", "product_name"]).agg(
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
    ).reset_index()
    
    return daily
