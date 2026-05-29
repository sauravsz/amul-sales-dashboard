"""
KPI calculations for the Amul Sales Dashboard.
All core FMCG field sales metrics.
"""

import pandas as pd


def coverage_kpis(df):
    """Calculate coverage-related KPIs."""
    total_visits = df[df["visited"] == "Yes"]["outlet_id"].nunique() if "visited" in df.columns else 0
    # Total visit-days (unique outlet-date combos)
    if "date" in df.columns:
        total_visit_days = df.drop_duplicates(subset=["outlet_id", "date"]).shape[0]
    else:
        total_visit_days = len(df)
    
    unique_outlets = df["outlet_id"].nunique() if "outlet_id" in df.columns else 0
    total_pitches = df[df["pitched"] == "Yes"].shape[0] if "pitched" in df.columns else 0
    productive_calls = df[df["order_booked"] == "Yes"].shape[0] if "order_booked" in df.columns else 0
    
    return {
        "total_visit_days": total_visit_days,
        "unique_outlets": unique_outlets,
        "total_pitches": total_pitches,
        "productive_calls": productive_calls,
        "outlet_coverage_rate": round(unique_outlets / 25 * 100, 1) if unique_outlets else 0,
    }


def conversion_kpis(df):
    """Calculate conversion-related KPIs."""
    pitched = df[df["pitched"] == "Yes"] if "pitched" in df.columns else df
    total_pitches = len(pitched)
    orders = df[df["order_booked"] == "Yes"] if "order_booked" in df.columns else pd.DataFrame()
    total_orders = len(orders)
    total_pieces = df["pieces_ordered"].sum() if "pieces_ordered" in df.columns else 0
    
    strike_rate = round(total_orders / total_pitches * 100, 1) if total_pitches > 0 else 0
    conversion_rate = round(total_orders / total_pitches * 100, 1) if total_pitches > 0 else 0
    
    bill_cuts = orders[orders["bill_cut"] == "Yes"].shape[0] if "bill_cut" in orders.columns else 0
    bill_cut_rate = round(bill_cuts / total_orders * 100, 1) if total_orders > 0 else 0
    
    avg_pieces = round(total_pieces / total_orders, 1) if total_orders > 0 else 0
    
    # Estimated total sales value
    total_value = df["estimated_sales_value"].sum() if "estimated_sales_value" in df.columns else 0
    
    return {
        "strike_rate": strike_rate,
        "conversion_rate": conversion_rate,
        "bill_cut_rate": bill_cut_rate,
        "avg_pieces_per_order": avg_pieces,
        "total_pieces_ordered": int(total_pieces),
        "total_orders": total_orders,
        "estimated_total_value": round(total_value, 0),
    }


def product_kpis(df):
    """Calculate product-level KPIs."""
    if df.empty:
        return pd.DataFrame()
    
    pitched = df[df["pitched"] == "Yes"] if "pitched" in df.columns else df
    
    product_stats = pitched.groupby("product_name").agg(
        pitches=("pitched", "count"),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        avg_visibility=("visibility_score", "mean"),
        avg_interest=("interest_score", "mean"),
        competitor_count=("competitor_present", lambda x: (x == "Yes").sum()),
    ).reset_index()
    
    product_stats["conversion_pct"] = round(
        product_stats["orders"] / product_stats["pitches"] * 100, 1
    )
    product_stats["avg_order_size"] = round(
        product_stats["pieces"] / product_stats["orders"].replace(0, 1), 1
    )
    product_stats["competitor_pct"] = round(
        product_stats["competitor_count"] / product_stats["pitches"] * 100, 1
    )
    product_stats["avg_visibility"] = round(product_stats["avg_visibility"], 2)
    product_stats["avg_interest"] = round(product_stats["avg_interest"], 2)
    
    # Top objection per product
    no_order = df[df["order_booked"] == "No"]
    if not no_order.empty and "retailer_objection_category" in no_order.columns:
        top_obj = no_order[no_order["retailer_objection_category"] != ""].groupby(
            "product_name"
        )["retailer_objection_category"].agg(
            lambda x: x.value_counts().index[0] if len(x) > 0 else ""
        ).reset_index()
        top_obj.columns = ["product_name", "top_objection"]
        product_stats = product_stats.merge(top_obj, on="product_name", how="left")
    else:
        product_stats["top_objection"] = ""
    
    return product_stats.sort_values("conversion_pct", ascending=False)


def execution_kpis(df):
    """Calculate execution quality KPIs."""
    pitched = df[df["pitched"] == "Yes"] if "pitched" in df.columns else df
    total = len(pitched)
    
    if total == 0:
        return {
            "availability_pct": 0,
            "scheme_explained_pct": 0,
            "avg_visibility_score": 0,
            "competitor_presence_pct": 0,
            "follow_up_needed_pct": 0,
            "high_interest_no_order_count": 0,
            "pitch_without_stock_count": 0,
        }
    
    avail = pitched[pitched["availability_before_pitch"] == "Yes"].shape[0]
    scheme = pitched[pitched["scheme_explained"] == "Yes"].shape[0]
    comp = pitched[pitched["competitor_present"] == "Yes"].shape[0]
    followup = pitched[pitched["follow_up_needed"] == "Yes"].shape[0]
    
    hino = df["high_interest_no_order"].sum() if "high_interest_no_order" in df.columns else 0
    pws = df["pitch_without_stock"].sum() if "pitch_without_stock" in df.columns else 0
    
    avg_vis = round(pitched["visibility_score"].mean(), 2) if "visibility_score" in pitched.columns else 0
    
    return {
        "availability_pct": round(avail / total * 100, 1),
        "scheme_explained_pct": round(scheme / total * 100, 1),
        "avg_visibility_score": avg_vis,
        "competitor_presence_pct": round(comp / total * 100, 1),
        "follow_up_needed_pct": round(followup / total * 100, 1),
        "high_interest_no_order_count": int(hino),
        "pitch_without_stock_count": int(pws),
    }


def funnel_data(df):
    """Calculate sales funnel stages."""
    total_visited = df[df["visited"] == "Yes"].shape[0] if "visited" in df.columns else len(df)
    total_pitched = df[df["pitched"] == "Yes"].shape[0] if "pitched" in df.columns else 0
    
    pitched_df = df[df["pitched"] == "Yes"] if "pitched" in df.columns else df
    interested = pitched_df[pitched_df["retailer_interest_level"].isin(["Medium", "High"])].shape[0]
    ordered = df[df["order_booked"] == "Yes"].shape[0]
    pieces = int(df["pieces_ordered"].sum()) if "pieces_ordered" in df.columns else 0
    
    return {
        "Outlets Visited": total_visited,
        "Products Pitched": total_pitched,
        "Retailer Interested": interested,
        "Orders Booked": ordered,
        "Pieces Ordered": pieces,
    }


def daily_trend(df):
    """Calculate daily trends for pitches and orders."""
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()
    
    daily = df.groupby("date").agg(
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("order_booked", lambda x: (x == "Yes").sum()),
        pieces=("pieces_ordered", "sum"),
    ).reset_index()
    
    daily["conversion_rate"] = round(daily["orders"] / daily["pitches"].replace(0, 1) * 100, 1)
    daily["date"] = pd.to_datetime(daily["date"])
    
    return daily.sort_values("date")


def outlet_type_stats(df):
    """Calculate stats by outlet type."""
    if df.empty:
        return pd.DataFrame()
    
    stats = df.groupby("outlet_type").agg(
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("productive_call", "sum"),
        pieces=("pieces_ordered", "sum"),
        unique_outlets=("outlet_id", "nunique"),
        avg_visibility=("visibility_score", "mean"),
    ).reset_index()
    
    stats["conversion_pct"] = round(stats["orders"] / stats["pitches"].replace(0, 1) * 100, 1)
    stats["avg_pieces_per_order"] = round(stats["pieces"] / stats["orders"].replace(0, 1), 1)
    stats["avg_visibility"] = round(stats["avg_visibility"], 2)
    
    return stats.sort_values("conversion_pct", ascending=False)


def weekly_trend(df):
    """Calculate weekly aggregated trends for week-over-week comparison."""
    if df.empty or "week_no" not in df.columns:
        return pd.DataFrame()

    weekly = df.groupby("week_no").agg(
        days=("date", "nunique"),
        unique_outlets=("outlet_id", "nunique"),
        pitches=("pitched", lambda x: (x == "Yes").sum()),
        orders=("order_booked", lambda x: (x == "Yes").sum()),
        pieces=("pieces_ordered", "sum"),
        avg_visibility=("visibility_score", "mean"),
        avg_interest=("interest_score", "mean"),
        scheme_yes=("scheme_explained", lambda x: (x == "Yes").sum()),
        competitor_yes=("competitor_present", lambda x: (x == "Yes").sum()),
        follow_ups=("follow_up_needed", lambda x: (x == "Yes").sum()),
    ).reset_index()

    weekly["conversion_pct"] = round(weekly["orders"] / weekly["pitches"].replace(0, 1) * 100, 1)
    weekly["avg_pieces_per_order"] = round(weekly["pieces"] / weekly["orders"].replace(0, 1), 1)
    weekly["pitches_per_day"] = round(weekly["pitches"] / weekly["days"].replace(0, 1), 1)
    weekly["orders_per_day"] = round(weekly["orders"] / weekly["days"].replace(0, 1), 1)
    weekly["scheme_pct"] = round(weekly["scheme_yes"] / weekly["pitches"].replace(0, 1) * 100, 1)
    weekly["competitor_pct"] = round(weekly["competitor_yes"] / weekly["pitches"].replace(0, 1) * 100, 1)
    weekly["avg_visibility"] = round(weekly["avg_visibility"], 2)
    weekly["avg_interest"] = round(weekly["avg_interest"], 2)

    return weekly.sort_values("week_no")
