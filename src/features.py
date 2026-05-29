"""
Feature engineering for the Amul Sales Dashboard.
Creates derived fields from cleaned field sales data.
"""

import pandas as pd


VISIBILITY_MAP = {"Low": 1, "Medium": 2, "High": 3}
INTEREST_MAP = {"Low": 1, "Medium": 2, "High": 3}

PRODUCT_GROUP_MAP = {
    "More Tin Paneer": "Dairy",
    "Amul Aata": "Staples",
    "Amul Cookies": "Snacks",
    "Amul Chocolates": "Confectionery",
    "Organic Kabuli Chana": "Organics",
    "Organic Toor Dal": "Organics",
    "Organic Masoor Dal": "Organics",
    "Organic Rajma": "Organics",
}

# Unit prices for sales value estimation
UNIT_PRICES = {
    "More Tin Paneer": 45,
    "Amul Aata": 38,
    "Amul Cookies": 20,
    "Amul Chocolates": 15,
    "Organic Kabuli Chana": 120,
    "Organic Toor Dal": 95,
    "Organic Masoor Dal": 85,
    "Organic Rajma": 110,
}


def create_features(df):
    """Create all derived fields."""
    df = df.copy()
    
    # --- Binary flags ---
    df["productive_call"] = (df["order_booked"] == "Yes").astype(int)
    df["conversion_flag"] = (df["pieces_ordered"] > 0).astype(int)
    df["successful_pitch"] = (
        (df["pitched"] == "Yes") & (df["order_booked"] == "Yes")
    ).astype(int)
    
    # High interest but no order — key opportunity signal
    df["high_interest_no_order"] = (
        (df["retailer_interest_level"] == "High") & (df["order_booked"] == "No")
    ).astype(int)
    
    # Pitched without prior stock — distribution gap signal
    df["pitch_without_stock"] = (
        (df["pitched"] == "Yes") & (df["availability_before_pitch"] == "No")
    ).astype(int)
    
    # --- Numeric scores ---
    df["visibility_score"] = df["display_visibility"].map(VISIBILITY_MAP).fillna(2)
    df["interest_score"] = df["retailer_interest_level"].map(INTEREST_MAP).fillna(2)
    
    # --- Product group mapping ---
    if "product_group" not in df.columns or df["product_group"].isna().all():
        df["product_group"] = df["product_name"].map(PRODUCT_GROUP_MAP).fillna("Other")
    
    # --- Estimated sales value ---
    df["estimated_unit_price"] = df["product_name"].map(UNIT_PRICES).fillna(0)
    df["estimated_sales_value"] = df["pieces_ordered"] * df["estimated_unit_price"]
    
    # --- Time features ---
    if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["day_of_week"] = df["date"].dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    
    return df
