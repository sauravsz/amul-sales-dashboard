"""
Data cleaning pipeline for the Amul Sales Dashboard.
Standardizes text, fills defaults, validates data quality.
"""

import pandas as pd


# --- Standard mappings for text normalization ---
OUTLET_TYPE_MAP = {
    "kirana": "Kirana",
    "supermarket": "Supermarket",
    "dairy shop": "Dairy Shop",
    "dairy": "Dairy Shop",
    "bakery": "Bakery",
    "general store": "General Store",
    "general": "General Store",
    "departmental store": "Departmental Store",
    "departmental": "Departmental Store",
    "wholesaler": "Wholesaler",
    "others": "Others",
}

YES_NO_COLUMNS = [
    "visited", "pitched", "availability_before_pitch", "scheme_explained",
    "order_booked", "bill_cut", "competitor_present", "follow_up_needed",
    "cold_storage_available", "high_footfall",
]

LEVEL_COLUMNS = ["display_visibility", "retailer_interest_level"]
VALID_LEVELS = {"Low", "Medium", "High"}


def standardize_text(df):
    """Standardize text columns — strip whitespace, fix case."""
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
    
    # Standardize outlet types
    if "outlet_type" in df.columns:
        df["outlet_type"] = df["outlet_type"].str.lower().map(
            lambda x: OUTLET_TYPE_MAP.get(x, x.title())
        )
    
    # Standardize yes/no columns
    for col in YES_NO_COLUMNS:
        if col in df.columns:
            df[col] = df[col].str.capitalize().apply(
                lambda x: "Yes" if x in ("Yes", "Y", "1", "True") else
                          "No" if x in ("No", "N", "0", "False", "nan", "") else x
            )
    
    # Standardize level columns
    for col in LEVEL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].str.capitalize().apply(
                lambda x: x if x in VALID_LEVELS else "Medium"
            )
    
    return df


def fill_defaults(df):
    """Fill missing values with sensible defaults."""
    numeric_cols = ["pieces_ordered", "pieces_sold_if_known", "order_value_if_known"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    
    # Default yes/no to "No"
    for col in YES_NO_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("No")
    
    # Default levels to "Medium"
    for col in LEVEL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("Medium")
    
    # Fill text blanks
    text_fill = {
        "retailer_objection_raw": "",
        "retailer_objection_category": "",
        "competitor_brand": "",
        "follow_up_priority": "",
        "follow_up_reason": "",
        "my_observation": "",
    }
    for col, default in text_fill.items():
        if col in df.columns:
            df[col] = df[col].fillna(default).replace("nan", default)
    
    return df


def parse_dates(df):
    """Parse and validate date columns."""
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["day"] = df["date"].dt.day_name()
        df["week_no"] = ((df["date"] - df["date"].min()).dt.days // 7) + 1
        df["month"] = df["date"].dt.strftime("%B")
    return df


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        print(f"Removed {removed} duplicate rows")
    return df


def validate_data(df):
    """Validate data quality and return issues list."""
    issues = []
    
    if df.empty:
        issues.append("Dataset is empty")
        return issues
    
    # Check required columns
    required = ["date", "outlet_id", "product_name", "pitched", "order_booked"]
    for col in required:
        if col not in df.columns:
            issues.append(f"Missing required column: {col}")
    
    # Check for rows with order but no pieces
    if "order_booked" in df.columns and "pieces_ordered" in df.columns:
        bad = df[(df["order_booked"] == "Yes") & (df["pieces_ordered"] == 0)]
        if len(bad) > 0:
            issues.append(f"{len(bad)} rows have order_booked=Yes but pieces_ordered=0")
    
    return issues


def clean_pipeline(df):
    """Run the full cleaning pipeline."""
    df = df.copy()
    df = standardize_text(df)
    df = fill_defaults(df)
    df = parse_dates(df)
    df = remove_duplicates(df)
    return df
