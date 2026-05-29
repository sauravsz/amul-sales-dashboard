"""
Rule-based recommendation engine for the Amul Sales Dashboard.
Generates actionable follow-up suggestions based on field data patterns.
"""

import pandas as pd


# --- Recommendation Rules ---
RULES = [
    {
        "id": "R01",
        "name": "High Interest No Order",
        "condition": lambda row: row.get("retailer_interest_level") == "High" and row.get("order_booked") == "No",
        "action": "High opportunity outlet — revisit within 2-3 days with focused pitch",
        "priority": "High",
    },
    {
        "id": "R02",
        "name": "Stock Availability Gap",
        "condition": lambda row: row.get("availability_before_pitch") == "No" and row.get("retailer_interest_level") in ("Medium", "High"),
        "action": "Stock availability issue — coordinate with distributor to ensure product is available",
        "priority": "High",
    },
    {
        "id": "R03",
        "name": "Low Visibility Impulse",
        "condition": lambda row: row.get("display_visibility") == "Low" and row.get("product_group") in ("Snacks", "Confectionery"),
        "action": "Improve counter/display visibility for impulse product",
        "priority": "Medium",
    },
    {
        "id": "R04",
        "name": "Price Objection",
        "condition": lambda row: row.get("retailer_objection_category") == "High price",
        "action": "Reframe value proposition — compare pack size and price vs competitor",
        "priority": "Medium",
    },
    {
        "id": "R05",
        "name": "Slow Moving Objection",
        "condition": lambda row: row.get("retailer_objection_category") == "Slow moving",
        "action": "Suggest small trial quantity to build confidence; offer scheme if available",
        "priority": "Medium",
    },
    {
        "id": "R06",
        "name": "No Cold Storage for Paneer",
        "condition": lambda row: row.get("product_name") == "More Tin Paneer" and row.get("cold_storage_available") == "No",
        "action": "Paneer not ideal without refrigeration — deprioritize or discuss storage options",
        "priority": "Low",
    },
    {
        "id": "R07",
        "name": "Organic in Supermarket",
        "condition": lambda row: row.get("product_group") == "Organics" and row.get("outlet_type") in ("Supermarket", "Departmental Store") and row.get("order_booked") == "No",
        "action": "Premium outlet for organics — strengthen assortment pitch with health and quality focus",
        "priority": "High",
    },
    {
        "id": "R08",
        "name": "Competitor Dominance",
        "condition": lambda row: row.get("competitor_present") == "Yes" and row.get("order_booked") == "No",
        "action": "Competitor present — highlight Amul brand trust, margin, and scheme advantages",
        "priority": "Medium",
    },
    {
        "id": "R09",
        "name": "No Demand Perception",
        "condition": lambda row: row.get("retailer_objection_category") == "No demand",
        "action": "Educate retailer on product demand trends; offer display support or sampling",
        "priority": "Medium",
    },
    {
        "id": "R10",
        "name": "Scheme Not Explained",
        "condition": lambda row: row.get("scheme_explained") == "No" and row.get("order_booked") == "No" and row.get("retailer_interest_level") in ("Medium", "High"),
        "action": "Scheme was not explained to interested retailer — revisit with scheme details",
        "priority": "High",
    },
    {
        "id": "R11",
        "name": "Retailer Unconvinced",
        "condition": lambda row: row.get("retailer_objection_category") == "Retailer unconvinced",
        "action": "Provide product literature, taste samples, or testimonials from nearby outlets",
        "priority": "Medium",
    },
    {
        "id": "R12",
        "name": "High Footfall Missed",
        "condition": lambda row: row.get("high_footfall") == "Yes" and row.get("order_booked") == "No" and row.get("product_group") in ("Snacks", "Confectionery"),
        "action": "High-footfall outlet ideal for impulse products — revisit with display plan",
        "priority": "High",
    },
]


def generate_recommendations(df):
    """Apply all rules to the dataset and return a recommendations DataFrame."""
    if df.empty:
        return pd.DataFrame()
    
    recommendations = []
    
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        
        for rule in RULES:
            try:
                if rule["condition"](row_dict):
                    recommendations.append({
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "outlet_id": row_dict.get("outlet_id", ""),
                        "outlet_name": row_dict.get("outlet_name", ""),
                        "outlet_type": row_dict.get("outlet_type", ""),
                        "product_name": row_dict.get("product_name", ""),
                        "product_group": row_dict.get("product_group", ""),
                        "interest_level": row_dict.get("retailer_interest_level", ""),
                        "objection": row_dict.get("retailer_objection_category", ""),
                        "suggested_action": rule["action"],
                        "priority": rule["priority"],
                        "date": row_dict.get("date", ""),
                    })
            except Exception:
                continue
    
    if not recommendations:
        return pd.DataFrame()
    
    rec_df = pd.DataFrame(recommendations)
    
    # Deduplicate — keep one recommendation per outlet-product-rule combo
    rec_df = rec_df.drop_duplicates(
        subset=["outlet_id", "product_name", "rule_id"],
        keep="last"
    )
    
    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    rec_df["priority_rank"] = rec_df["priority"].map(priority_order)
    rec_df = rec_df.sort_values("priority_rank").drop(columns=["priority_rank"])
    
    return rec_df


def recommendation_summary(rec_df):
    """Summarize recommendations by rule and priority."""
    if rec_df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    by_rule = rec_df.groupby(["rule_id", "rule_name"]).agg(
        count=("outlet_id", "count"),
        priority=("priority", "first"),
    ).reset_index().sort_values("count", ascending=False)
    
    by_priority = rec_df.groupby("priority").agg(
        count=("outlet_id", "count"),
    ).reset_index()
    
    return by_rule, by_priority
