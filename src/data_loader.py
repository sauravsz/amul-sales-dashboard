"""
Data loading utilities for the Amul Sales Dashboard.
Handles reading CSV files and validating required columns.
"""

import pandas as pd
import os
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

REQUIRED_COLUMNS = [
    "date", "outlet_id", "outlet_name", "outlet_type", "product_name",
    "pitched", "order_booked", "pieces_ordered"
]


@st.cache_data(ttl=300)
def load_field_log(path=None):
    """Load the raw field sales log CSV."""
    if path is None:
        path = os.path.join(DATA_DIR, "raw", "field_sales_log.csv")
    
    if not os.path.exists(path):
        st.error(f"Field sales log not found at: {path}")
        return pd.DataFrame()
    
    df = pd.read_csv(path, encoding="utf-8")
    
    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.warning(f"Missing columns in field log: {missing}")
    
    return df


@st.cache_data(ttl=600)
def load_products_master(path=None):
    """Load the products master file."""
    if path is None:
        path = os.path.join(DATA_DIR, "master", "products_master.csv")
    
    if not os.path.exists(path):
        return pd.DataFrame()
    
    return pd.read_csv(path, encoding="utf-8")


@st.cache_data(ttl=600)
def load_outlets_master(path=None):
    """Load the outlets master file."""
    if path is None:
        path = os.path.join(DATA_DIR, "master", "outlets_master.csv")
    
    if not os.path.exists(path):
        return pd.DataFrame()
    
    return pd.read_csv(path, encoding="utf-8")


@st.cache_data(ttl=600)
def load_objections_master(path=None):
    """Load the objections master file."""
    if path is None:
        path = os.path.join(DATA_DIR, "master", "objections_master.csv")
    
    if not os.path.exists(path):
        return pd.DataFrame()
    
    return pd.read_csv(path, encoding="utf-8")


def load_all_data():
    """Load all data sources and return as a dictionary."""
    field_log = load_field_log()
    products = load_products_master()
    outlets = load_outlets_master()
    objections = load_objections_master()
    
    return {
        "field_log": field_log,
        "products_master": products,
        "outlets_master": outlets,
        "objections_master": objections,
    }
