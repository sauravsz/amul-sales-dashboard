"""
Competitor intelligence analysis for the Amul Sales Dashboard.
Dedicated competitor tracking by product, outlet type, and impact on conversion.
"""

import pandas as pd


def competitor_overview(df):
    """Overall competitor presence statistics."""
    if df.empty:
        return {}

    pitched = df[df["pitched"] == "Yes"]
    total = len(pitched)
    comp_present = pitched[pitched["competitor_present"] == "Yes"]

    # Conversion with and without competitor
    with_comp = comp_present[comp_present["order_booked"] == "Yes"].shape[0]
    without_comp_df = pitched[pitched["competitor_present"] == "No"]
    without_comp = without_comp_df[without_comp_df["order_booked"] == "Yes"].shape[0]

    return {
        "total_pitches": total,
        "competitor_present_count": len(comp_present),
        "competitor_present_pct": round(len(comp_present) / max(total, 1) * 100, 1),
        "conversion_with_competitor": round(with_comp / max(len(comp_present), 1) * 100, 1),
        "conversion_without_competitor": round(without_comp / max(len(without_comp_df), 1) * 100, 1),
        "conversion_gap": round(
            without_comp / max(len(without_comp_df), 1) * 100 -
            with_comp / max(len(comp_present), 1) * 100, 1
        ),
        "unique_competitors": comp_present["competitor_brand"].nunique(),
    }


def competitor_brand_analysis(df):
    """Analyze which competitor brands are most frequent and their impact."""
    if df.empty:
        return pd.DataFrame()

    comp = df[(df["competitor_present"] == "Yes") & (df["competitor_brand"] != "")]

    if comp.empty:
        return pd.DataFrame()

    stats = comp.groupby("competitor_brand").agg(
        occurrences=("competitor_brand", "count"),
        products_affected=("product_name", "nunique"),
        outlets_affected=("outlet_id", "nunique"),
        blocked_orders=("order_booked", lambda x: (x == "No").sum()),
        won_orders=("order_booked", lambda x: (x == "Yes").sum()),
    ).reset_index()

    stats["block_rate"] = round(
        stats["blocked_orders"] / stats["occurrences"] * 100, 1
    )
    stats["win_rate"] = round(
        stats["won_orders"] / stats["occurrences"] * 100, 1
    )

    return stats.sort_values("occurrences", ascending=False)


def competitor_by_product(df):
    """Which Amul products face the most competition?"""
    if df.empty:
        return pd.DataFrame()

    pitched = df[df["pitched"] == "Yes"]

    stats = pitched.groupby("product_name").agg(
        total_pitches=("pitched", "count"),
        comp_present=("competitor_present", lambda x: (x == "Yes").sum()),
        orders_with_comp=("order_booked", lambda x: (
            (x == "Yes") & (pitched.loc[x.index, "competitor_present"] == "Yes")
        ).sum()),
        orders_without_comp=("order_booked", lambda x: (
            (x == "Yes") & (pitched.loc[x.index, "competitor_present"] == "No")
        ).sum()),
    ).reset_index()

    stats["competitor_exposure_pct"] = round(
        stats["comp_present"] / stats["total_pitches"] * 100, 1
    )

    # Top competitor per product
    comp_df = df[(df["competitor_present"] == "Yes") & (df["competitor_brand"] != "")]
    if not comp_df.empty:
        top_comp = comp_df.groupby("product_name")["competitor_brand"].agg(
            lambda x: x.value_counts().index[0] if len(x) > 0 else ""
        ).reset_index()
        top_comp.columns = ["product_name", "top_competitor"]
        stats = stats.merge(top_comp, on="product_name", how="left")
    else:
        stats["top_competitor"] = ""

    return stats.sort_values("competitor_exposure_pct", ascending=False)


def competitor_by_outlet_type(df):
    """Competitor presence by outlet type."""
    if df.empty:
        return pd.DataFrame()

    pitched = df[df["pitched"] == "Yes"]

    stats = pitched.groupby("outlet_type").agg(
        pitches=("pitched", "count"),
        comp_present=("competitor_present", lambda x: (x == "Yes").sum()),
        orders_with_comp=("productive_call", "sum"),
    ).reset_index()

    stats["competitor_pct"] = round(
        stats["comp_present"] / stats["pitches"] * 100, 1
    )

    # Top competitor brands per outlet type
    comp_df = df[(df["competitor_present"] == "Yes") & (df["competitor_brand"] != "")]
    if not comp_df.empty:
        top_brands = comp_df.groupby("outlet_type")["competitor_brand"].agg(
            lambda x: ", ".join(x.value_counts().head(2).index.tolist())
        ).reset_index()
        top_brands.columns = ["outlet_type", "top_brands"]
        stats = stats.merge(top_brands, on="outlet_type", how="left")
    else:
        stats["top_brands"] = ""

    return stats.sort_values("competitor_pct", ascending=False)


def competitor_product_matrix(df):
    """Matrix: Amul product × competitor brand frequency."""
    if df.empty:
        return pd.DataFrame()

    comp = df[(df["competitor_present"] == "Yes") & (df["competitor_brand"] != "")]

    if comp.empty:
        return pd.DataFrame()

    matrix = pd.crosstab(
        comp["product_name"],
        comp["competitor_brand"],
        margins=False,
    )

    return matrix
