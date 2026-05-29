"""
Generate synthetic field sales log data for the Amul Sales Dashboard demo.
Run this script once to create data/raw/field_sales_log.csv
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# --- Master Data ---
PRODUCTS = [
    ("More Tin Paneer", "Dairy", "Paneer"),
    ("Amul Aata", "Staples", "Flour"),
    ("Amul Cookies", "Snacks", "Cookies"),
    ("Amul Chocolates", "Confectionery", "Chocolate"),
    ("Organic Kabuli Chana", "Organics", "Pulses"),
    ("Organic Toor Dal", "Organics", "Pulses"),
    ("Organic Masoor Dal", "Organics", "Pulses"),
    ("Organic Rajma", "Organics", "Pulses"),
]

OUTLETS = [
    ("OUT001", "Sharma General Store", "Kirana", "Small", "Residential", "No", "No"),
    ("OUT002", "Patel Dairy & Sweets", "Dairy Shop", "Medium", "Market", "Yes", "Yes"),
    ("OUT003", "Raj Supermart", "Supermarket", "Large", "Market", "Yes", "Yes"),
    ("OUT004", "Gupta Provision Store", "Kirana", "Medium", "Residential", "No", "No"),
    ("OUT005", "Fresh Daily Mart", "General Store", "Medium", "Mixed", "Yes", "No"),
    ("OUT006", "City Bakery & Confectionery", "Bakery", "Small", "Market", "Yes", "No"),
    ("OUT007", "Annapurna Grocers", "Kirana", "Large", "Residential", "No", "No"),
    ("OUT008", "Metro Fresh Supermarket", "Supermarket", "Large", "Market", "Yes", "Yes"),
    ("OUT009", "Lakshmi Dairy Booth", "Dairy Shop", "Small", "Residential", "No", "Yes"),
    ("OUT010", "Balaji General Store", "General Store", "Small", "Mixed", "No", "No"),
    ("OUT011", "Singh Departmental Store", "Departmental Store", "Large", "Market", "Yes", "Yes"),
    ("OUT012", "Mahavir Kirana", "Kirana", "Small", "Residential", "No", "No"),
    ("OUT013", "Royal Bakers", "Bakery", "Medium", "Market", "Yes", "No"),
    ("OUT014", "Sai Provision & General", "Kirana", "Medium", "Mixed", "No", "No"),
    ("OUT015", "Green Valley Organics", "Supermarket", "Medium", "Market", "Yes", "Yes"),
    ("OUT016", "Mahalaxmi Dairy", "Dairy Shop", "Medium", "Residential", "Yes", "Yes"),
    ("OUT017", "Jai Bhavani Store", "Kirana", "Small", "Residential", "No", "No"),
    ("OUT018", "Big Basket Express", "Supermarket", "Large", "Market", "Yes", "Yes"),
    ("OUT019", "Nandini General Store", "General Store", "Medium", "Mixed", "Yes", "No"),
    ("OUT020", "Quick Stop Convenience", "General Store", "Small", "Market", "Yes", "No"),
    ("OUT021", "Ganesh Wholesalers", "Wholesaler", "Large", "Market", "No", "Yes"),
    ("OUT022", "Shree Ram Kirana", "Kirana", "Medium", "Residential", "No", "No"),
    ("OUT023", "Taste & Treat Bakery", "Bakery", "Small", "Market", "Yes", "No"),
    ("OUT024", "Apna Bazaar", "Departmental Store", "Medium", "Mixed", "Yes", "Yes"),
    ("OUT025", "Kisaan Organics Hub", "Supermarket", "Medium", "Market", "Yes", "Yes"),
]

OBJECTION_CATEGORIES = [
    "No demand", "Low margin", "Already have competitor", "No shelf space",
    "Slow moving", "High price", "No customer asking", "Stock not available",
    "Not relevant for outlet", "Retailer unconvinced", "Cash or credit issue",
]

OBJECTION_RAW_MAP = {
    "No demand": ["Nobody asks for this", "No demand here", "Customers don't want it"],
    "Low margin": ["Margin is too low", "Not enough profit", "Competitor gives better margin"],
    "Already have competitor": ["Already selling Mother Dairy", "Have Patanjali", "Competitor brand runs well"],
    "No shelf space": ["No space left", "Shelf is full", "Where do I keep it"],
    "Slow moving": ["It sits on the shelf", "Tried before, didn't sell", "Very slow rotation"],
    "High price": ["Too expensive", "Price is high", "Customers complain about price"],
    "No customer asking": ["Nobody has asked", "No enquiry", "Customers don't know about it"],
    "Stock not available": ["Distributor didn't send", "Out of stock", "Not available right now"],
    "Not relevant for outlet": ["Not our type of product", "Doesn't match our store", "Wrong category for us"],
    "Retailer unconvinced": ["Not sure about quality", "Don't trust organic claims", "Need more info"],
    "Cash or credit issue": ["Cash flow problem", "Need credit terms", "Payment pending with distributor"],
}

COMPETITOR_BRANDS = [
    "Mother Dairy", "Patanjali", "Britannia", "Cadbury", "Parle",
    "Fortune", "Tata Sampann", "24 Mantra", "Aashirvaad", "Nestle"
]

BEATS = ["Beat A - East", "Beat B - West", "Beat C - North", "Beat D - South"]
AREAS = ["Sector 12", "Main Market", "Civil Lines", "Station Road", "Gandhi Nagar"]

OBSERVATIONS = [
    "Good display location available",
    "Retailer seems open to trial",
    "Competitor running promo scheme",
    "High customer traffic today",
    "Store recently renovated",
    "Retailer asked about return policy",
    "Adjacent store carries Amul butter already",
    "Small counter space only",
    "Retailer was busy, brief conversation only",
    "Positive response to taste sample",
    "Need to revisit with scheme details",
    "Store has prime shelf location potential",
    "Retailer mentioned past Amul experience was good",
    "Price comparison sheet needed",
    "Competitor out of stock, opportunity to fill gap",
]

FOLLOW_UP_REASONS = [
    "Retailer asked for more info",
    "Interested but wants to clear current stock first",
    "Wants to see scheme details",
    "Positive but needs manager approval",
    "Will try if stock availability improves",
    "Wanted smaller trial quantity",
    "Needs credit terms discussion",
]

# --- Conversion probability logic ---
def get_conversion_probability(product, outlet_type, outlet_size, cold_storage, high_footfall, visibility, scheme, availability, interest):
    """Realistic conversion probability based on product-outlet fit."""
    base = 0.30

    # Product-outlet fit
    if product[0] == "More Tin Paneer":
        if cold_storage == "Yes": base += 0.15
        else: base -= 0.20
        if outlet_type in ("Dairy Shop",): base += 0.15
    elif product[0] in ("Amul Cookies", "Amul Chocolates"):
        if high_footfall == "Yes": base += 0.15
        if outlet_type in ("Bakery", "General Store", "Supermarket"): base += 0.10
    elif product[0] == "Amul Aata":
        if outlet_type in ("Kirana", "General Store", "Supermarket"): base += 0.10
        if outlet_size == "Large": base += 0.05
    elif "Organic" in product[0]:
        if outlet_type in ("Supermarket", "Departmental Store"): base += 0.15
        elif outlet_type == "Kirana" and outlet_size == "Small": base -= 0.15
        if outlet_type == "Bakery": base -= 0.10

    # Size & type
    if outlet_size == "Large": base += 0.10
    elif outlet_size == "Small": base -= 0.05

    # Execution factors
    if visibility == "High": base += 0.10
    elif visibility == "Low": base -= 0.10
    if scheme == "Yes": base += 0.10
    if availability == "Yes": base += 0.05
    if interest == "High": base += 0.20
    elif interest == "Low": base -= 0.15

    return max(0.05, min(0.85, base))


def get_objection_weights(product, outlet_type):
    """Weighted objection probabilities based on product-outlet combination."""
    weights = {cat: 1.0 for cat in OBJECTION_CATEGORIES}

    if "Organic" in product[0]:
        weights["No demand"] = 3.0
        weights["High price"] = 3.0
        weights["Slow moving"] = 2.5
        weights["No customer asking"] = 2.0
        weights["Retailer unconvinced"] = 2.0
    if product[0] == "More Tin Paneer":
        weights["Not relevant for outlet"] = 2.0
        weights["Slow moving"] = 1.5
    if product[0] in ("Amul Cookies", "Amul Chocolates"):
        weights["Already have competitor"] = 3.0
        weights["No shelf space"] = 2.0
        weights["Low margin"] = 2.0
    if product[0] == "Amul Aata":
        weights["Already have competitor"] = 3.0
        weights["Low margin"] = 2.5

    if outlet_type == "Kirana":
        weights["No shelf space"] = 2.0
        weights["Cash or credit issue"] = 1.5
    elif outlet_type == "Supermarket":
        weights["Low margin"] = 2.0
    elif outlet_type == "Wholesaler":
        weights["Low margin"] = 2.5
        weights["Cash or credit issue"] = 2.0

    return weights


def weighted_choice(items, weights):
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for item, w in zip(items, weights):
        cumulative += w
        if r <= cumulative:
            return item
    return items[-1]


def generate_data():
    """Generate ~250 rows of realistic field sales data."""
    rows = []
    start_date = datetime(2025, 6, 2)  # Start from a Monday
    num_days = 18  # ~3 weeks, weekdays only

    current_date = start_date
    day_count = 0

    while day_count < num_days:
        if current_date.weekday() >= 6:  # Skip Sunday
            current_date += timedelta(days=1)
            continue

        day_name = current_date.strftime("%A")
        week_no = ((current_date - start_date).days // 7) + 1
        month = current_date.strftime("%B")

        # Visit 6-10 outlets per day
        num_outlets_today = random.randint(6, 10)
        outlets_today = random.sample(OUTLETS, min(num_outlets_today, len(OUTLETS)))

        beat = random.choice(BEATS)
        area = random.choice(AREAS)

        for outlet in outlets_today:
            oid, oname, otype, osize, locality, hf, cold = outlet

            # Pitch 2-5 products per outlet
            num_products = random.randint(2, 5)
            products_pitched = random.sample(PRODUCTS, min(num_products, len(PRODUCTS)))

            for product in products_pitched:
                pitched = "Yes"
                availability = random.choices(["Yes", "No"], weights=[0.55, 0.45])[0]
                visibility = random.choices(["Low", "Medium", "High"], weights=[0.30, 0.45, 0.25])[0]
                scheme = random.choices(["Yes", "No"], weights=[0.60, 0.40])[0]
                interest = random.choices(["Low", "Medium", "High"], weights=[0.25, 0.45, 0.30])[0]

                conv_prob = get_conversion_probability(
                    product, otype, osize, cold, hf, visibility, scheme, availability, interest
                )

                order_booked = "Yes" if random.random() < conv_prob else "No"
                bill_cut = "No"
                pieces = 0

                if order_booked == "Yes":
                    bill_cut = random.choices(["Yes", "No"], weights=[0.80, 0.20])[0]
                    if osize == "Large":
                        pieces = random.randint(5, 30)
                    elif osize == "Medium":
                        pieces = random.randint(3, 15)
                    else:
                        pieces = random.randint(1, 8)

                pieces_sold = 0
                if pieces > 0 and random.random() < 0.3:
                    pieces_sold = random.randint(1, max(1, pieces // 2))

                # Competitor
                comp_present = random.choices(["Yes", "No"], weights=[0.45, 0.55])[0]
                comp_brand = ""
                if comp_present == "Yes":
                    if "Organic" in product[0]:
                        comp_brand = random.choice(["Patanjali", "Tata Sampann", "24 Mantra"])
                    elif product[0] in ("Amul Cookies", "Amul Chocolates"):
                        comp_brand = random.choice(["Britannia", "Cadbury", "Parle", "Nestle"])
                    elif product[0] == "Amul Aata":
                        comp_brand = random.choice(["Aashirvaad", "Patanjali", "Fortune"])
                    elif product[0] == "More Tin Paneer":
                        comp_brand = random.choice(["Mother Dairy", "Parag"])
                    else:
                        comp_brand = random.choice(COMPETITOR_BRANDS)

                # Objection
                objection_raw = ""
                objection_cat = ""
                if order_booked == "No":
                    obj_weights = get_objection_weights(product, otype)
                    cats = list(obj_weights.keys())
                    ws = [obj_weights[c] for c in cats]
                    objection_cat = weighted_choice(cats, ws)
                    objection_raw = random.choice(OBJECTION_RAW_MAP[objection_cat])

                # Follow-up
                follow_up = "No"
                follow_priority = ""
                follow_reason = ""
                if order_booked == "No":
                    if interest == "High":
                        follow_up = "Yes"
                        follow_priority = "High"
                        follow_reason = random.choice(FOLLOW_UP_REASONS)
                    elif interest == "Medium" and random.random() < 0.40:
                        follow_up = "Yes"
                        follow_priority = "Medium"
                        follow_reason = random.choice(FOLLOW_UP_REASONS)
                    elif random.random() < 0.10:
                        follow_up = "Yes"
                        follow_priority = "Low"
                        follow_reason = random.choice(FOLLOW_UP_REASONS)

                observation = ""
                if random.random() < 0.35:
                    observation = random.choice(OBSERVATIONS)

                rows.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "week_no": week_no,
                    "month": month,
                    "distributor_name": "Amul Distributor - City Hub",
                    "salesman_name": "Saurav",
                    "beat_name": beat,
                    "area": area,
                    "outlet_id": oid,
                    "outlet_name": oname,
                    "outlet_type": otype,
                    "outlet_size": osize,
                    "locality_type": locality,
                    "cold_storage_available": cold,
                    "high_footfall": hf,
                    "visited": "Yes",
                    "product_name": product[0],
                    "product_group": product[1],
                    "product_subgroup": product[2],
                    "pitched": pitched,
                    "availability_before_pitch": availability,
                    "display_visibility": visibility,
                    "scheme_explained": scheme,
                    "retailer_interest_level": interest,
                    "order_booked": order_booked,
                    "bill_cut": bill_cut,
                    "pieces_ordered": pieces,
                    "pieces_sold_if_known": pieces_sold,
                    "order_value_if_known": "",
                    "competitor_present": comp_present,
                    "competitor_brand": comp_brand,
                    "retailer_objection_raw": objection_raw,
                    "retailer_objection_category": objection_cat,
                    "follow_up_needed": follow_up,
                    "follow_up_priority": follow_priority,
                    "follow_up_reason": follow_reason,
                    "my_observation": observation,
                })

        current_date += timedelta(days=1)
        day_count += 1

    return rows


if __name__ == "__main__":
    import os
    rows = generate_data()
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "field_sales_log.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows → {output_path}")
