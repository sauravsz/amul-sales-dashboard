"""
Target vs Achievement tracking for the Amul Sales Dashboard.
Loads configurable targets and compares against actual KPIs.
"""

import json
import os
import pandas as pd

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "config", "targets.json"
)

DEFAULT_TARGETS = {
    "daily": {
        "outlet_visits": 8,
        "total_pitches": 25,
        "orders_booked": 10,
        "pieces_ordered": 50,
        "strike_rate_pct": 40,
    },
    "weekly": {
        "outlet_visits": 40,
        "total_pitches": 125,
        "orders_booked": 50,
        "pieces_ordered": 250,
        "unique_outlets": 20,
        "strike_rate_pct": 45,
    },
}


def load_targets():
    """Load targets from config file, or return defaults."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_TARGETS
    return DEFAULT_TARGETS


def save_targets(targets):
    """Save targets to config file."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(targets, f, indent=4)


def daily_achievement(df, target_date, targets=None):
    """Calculate daily achievement vs target for a specific date."""
    if targets is None:
        targets = load_targets()

    daily_targets = targets.get("daily", DEFAULT_TARGETS["daily"])
    day_df = df[df["date"] == pd.Timestamp(target_date)]

    if day_df.empty:
        return pd.DataFrame()

    pitched = day_df[day_df["pitched"] == "Yes"]
    orders = day_df[day_df["order_booked"] == "Yes"]

    actuals = {
        "outlet_visits": day_df.drop_duplicates(subset=["outlet_id"]).shape[0],
        "total_pitches": len(pitched),
        "orders_booked": len(orders),
        "pieces_ordered": int(day_df["pieces_ordered"].sum()),
        "strike_rate_pct": round(len(orders) / max(len(pitched), 1) * 100, 1),
    }

    rows = []
    for metric, target_val in daily_targets.items():
        actual_val = actuals.get(metric, 0)
        pct = round(actual_val / max(target_val, 1) * 100, 1)
        rows.append({
            "metric": metric.replace("_", " ").title(),
            "target": target_val,
            "actual": actual_val,
            "achievement_pct": min(pct, 200),  # cap at 200%
            "status": "✅" if actual_val >= target_val else "⚠️" if actual_val >= target_val * 0.7 else "❌",
        })

    return pd.DataFrame(rows)


def weekly_achievement(df, week_no, targets=None):
    """Calculate weekly achievement vs target for a given week."""
    if targets is None:
        targets = load_targets()

    weekly_targets = targets.get("weekly", DEFAULT_TARGETS["weekly"])
    week_df = df[df["week_no"] == week_no]

    if week_df.empty:
        return pd.DataFrame()

    pitched = week_df[week_df["pitched"] == "Yes"]
    orders = week_df[week_df["order_booked"] == "Yes"]

    actuals = {
        "outlet_visits": week_df.drop_duplicates(subset=["outlet_id", "date"]).shape[0],
        "total_pitches": len(pitched),
        "orders_booked": len(orders),
        "pieces_ordered": int(week_df["pieces_ordered"].sum()),
        "unique_outlets": week_df["outlet_id"].nunique(),
        "strike_rate_pct": round(len(orders) / max(len(pitched), 1) * 100, 1),
    }

    rows = []
    for metric, target_val in weekly_targets.items():
        actual_val = actuals.get(metric, 0)
        pct = round(actual_val / max(target_val, 1) * 100, 1)
        rows.append({
            "metric": metric.replace("_", " ").title(),
            "target": target_val,
            "actual": actual_val,
            "achievement_pct": min(pct, 200),
            "status": "✅" if actual_val >= target_val else "⚠️" if actual_val >= target_val * 0.7 else "❌",
        })

    return pd.DataFrame(rows)


def overall_achievement_summary(df, targets=None):
    """Overall achievement across the entire dataset period."""
    if targets is None:
        targets = load_targets()

    if df.empty:
        return {}

    num_days = df["date"].nunique()
    num_weeks = df["week_no"].nunique() if "week_no" in df.columns else 1

    daily_t = targets.get("daily", DEFAULT_TARGETS["daily"])
    pitched = df[df["pitched"] == "Yes"]
    orders = df[df["order_booked"] == "Yes"]

    expected_pitches = daily_t.get("total_pitches", 25) * num_days
    expected_orders = daily_t.get("orders_booked", 10) * num_days
    expected_pieces = daily_t.get("pieces_ordered", 50) * num_days

    return {
        "days_worked": num_days,
        "weeks_worked": num_weeks,
        "pitch_achievement": round(len(pitched) / max(expected_pitches, 1) * 100, 1),
        "order_achievement": round(len(orders) / max(expected_orders, 1) * 100, 1),
        "pieces_achievement": round(df["pieces_ordered"].sum() / max(expected_pieces, 1) * 100, 1),
    }
