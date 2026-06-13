import os
import re
import csv
from datetime import datetime
import pandas as pd

DOCS_DIR = "/Users/sauravsz/The-Hub/amul-sales-dashboard/2026-06-13 Intern Data/Created Docs"
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "field_sales_log.csv")

def parse_markdown_reports_regex():
    all_visits = []
    
    if not os.path.exists(DOCS_DIR):
        print(f"Error: Directory {DOCS_DIR} not found.")
        return []

    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split by '## Report'
        reports = content.split("## Report ")
        
        for report in reports[1:]:
            lines = [line.strip() for line in report.split('\n') if line.strip()]
            if not lines: continue
            
            # Parse Date
            date_formatted = "2026-06-01"
            date_match = re.search(r"(\d{2}/\d{2}/\d{2,4})", report)
            if date_match:
                date_str = date_match.group(1)
                try:
                    # WhatsApp dates might be 13/06/26 or 13/06/2026
                    fmt = "%d/%m/%Y" if len(date_str.split('/')[-1]) == 4 else "%d/%m/%y"
                    date_obj = datetime.strptime(date_str, fmt)
                    date_formatted = date_obj.strftime("%Y-%m-%d")
                except:
                    pass
                
            distributor_name = "Unknown"
            beat_name = "Unknown"
            salesman_name = "Unknown"
            intern_name = "Unknown"
            
            # Parse metadata
            idx = 1
            while idx < len(lines):
                line = lines[idx]
                if re.search(r'Distributor Name\s*[-:]\s*(.*)', line, re.IGNORECASE):
                    distributor_name = re.search(r'Distributor Name\s*[-:]\s*(.*)', line, re.IGNORECASE).group(1).replace("*", "").strip()
                elif re.search(r'Beat Name\s*[-:]\s*(.*)', line, re.IGNORECASE):
                    beat_name = re.search(r'Beat Name\s*[-:]\s*(.*)', line, re.IGNORECASE).group(1).replace("*", "").strip()
                elif re.search(r'Intern Name\s*[-:]\s*(.*)', line, re.IGNORECASE):
                    intern_name = re.search(r'Intern Name\s*[-:]\s*(.*)', line, re.IGNORECASE).group(1).replace("*", "").strip()
                elif re.search(r'Salesman Name\s*[-:]\s*(.*)', line, re.IGNORECASE):
                    salesman_name = re.search(r'Salesman Name\s*[-:]\s*(.*)', line, re.IGNORECASE).group(1).replace("*", "").strip()
                elif "observation" in line.lower():
                    break
                elif "no. of outlets" in line.lower() or "**distributor:**" in line.lower():
                    pass
                else:
                    break
                idx += 1
                
            # Parse outlets and products
            current_outlet = None
            observations = ""
            
            while idx < len(lines):
                line = lines[idx]
                if "observation" in line.lower() or "n.b." in line.lower():
                    observations = "\n".join(lines[idx+1:]).replace("---", "").strip()
                    break
                
                # If line is "Value = ..."
                if "Value =" in line or "Value :" in line or "Total =" in line or "Value -" in line:
                    current_outlet = None
                elif " pcs" in line.lower() or " tin" in line.lower() or " carton" in line.lower() or " box" in line.lower() or " jar" in line.lower() or " bag" in line.lower() or " ta" in line.lower():
                    # Product line
                    match = re.match(r"(.*?)\s+(\d+)\s*(pcs|tins?|cartons?|boxes|box|jars?|bags?|ta|piece|pieces)", line, re.IGNORECASE)
                    if match and current_outlet:
                        raw_product_name = match.group(1).strip()
                        # Clean leading/trailing dashes, colons, multiplier signs
                        product_name = re.sub(r'^[-\–\—\:\*\×\=xX\.]\s*', '', raw_product_name)
                        product_name = re.sub(r'[-\–\—\:\*\×\=xX\.]\s*$', '', product_name).strip().replace("*", "")
                        
                        if len(product_name) > 60:
                            idx += 1
                            continue
                            
                        qty = int(match.group(2))
                        multiplier = 1
                        if "carton" in match.group(3).lower(): multiplier = 24
                        elif "box" in match.group(3).lower(): multiplier = 10
                        
                        price_match = re.search(r'(?:₹|Rs\.?)\s*([\d,]+)', line, re.IGNORECASE)
                        estimated_value = 0
                        if price_match:
                            try:
                                estimated_value = int(price_match.group(1).replace(',', ''))
                            except:
                                pass
                                
                        all_visits.append({
                            "date": date_formatted,
                            "distributor_name": distributor_name,
                            "salesman_name": salesman_name,
                            "intern_name": intern_name,
                            "beat_name": beat_name,
                            "outlet_name": current_outlet,
                            "product_name": product_name,
                            "pieces_ordered": qty * multiplier,
                            "estimated_value": estimated_value,
                            "order_booked": "Yes",
                            "my_observation": ""
                        })
                elif "already present" in line.lower() or "out of stock" in line.lower() or "rejected" in line.lower():
                    if current_outlet and len(line) < 60:
                        all_visits.append({
                            "date": date_formatted,
                            "distributor_name": distributor_name,
                            "salesman_name": salesman_name,
                            "intern_name": intern_name,
                            "beat_name": beat_name,
                            "outlet_name": current_outlet,
                            "product_name": line.strip().replace("*", ""),
                            "pieces_ordered": 0,
                            "estimated_value": 0,
                            "order_booked": "No",
                            "my_observation": line
                        })
                else:
                    # Treat as outlet name if it doesn't match above and we don't have a current outlet
                    if current_outlet is None and line and not line.startswith("---") and not line.isdigit():
                        # Exclude lines that are just numbers (like "1.")
                        clean_name = re.sub(r'^\d+\.\s*', '', line)
                        current_outlet = clean_name
                
                idx += 1
                
            # Assign observations to the first visit of this report
            if observations and all_visits:
                # Find the last added visits for this report and append observation
                all_visits[-1]["my_observation"] = observations

    return all_visits

def transform_to_dataframe(visits):
    rows = []
    
    product_map = {
        "paneer": ("Dairy", "Paneer"),
        "aata": ("Staples", "Flour"),
        "cookies": ("Snacks", "Cookies"),
        "chocolate": ("Confectionery", "Chocolate"),
        "chocomini": ("Confectionery", "Chocolate"),
        "kool": ("Beverages", "Flavoured Milk"),
        "lassi": ("Beverages", "Lassi"),
        "masti": ("Beverages", "Lassi"),
        "tru litchi": ("Beverages", "Juice"),
        "tru mango": ("Beverages", "Juice"),
        "bindaaz": ("Confectionery", "Chocolate"),
        "doodh peda": ("Sweets", "Traditional Sweets"),
        "laal peda": ("Sweets", "Traditional Sweets"),
        "kaju katli": ("Sweets", "Traditional Sweets"),
        "rusk": ("Snacks", "Rusk")
    }

    for v in visits:
        try:
            date_obj = datetime.strptime(v["date"], "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            month = date_obj.strftime("%B")
            week_no = date_obj.isocalendar()[1] 
        except:
            day_name = "Unknown"
            month = "Unknown"
            week_no = 1
            
        p_lower = v["product_name"].lower()
        prod_group, prod_subgroup = ("Other", "Other")
        
        for key, vals in product_map.items():
            if key in p_lower:
                prod_group, prod_subgroup = vals
                break

        row = {
            "date": v["date"],
            "day": day_name,
            "week_no": week_no,
            "month": month,
            "distributor_name": v.get("distributor_name", "Unknown").title(),
            "salesman_name": v.get("salesman_name", "Unknown").title(),
            "intern_name": v.get("intern_name", "Unknown").title(),
            "beat_name": v.get("beat_name", "Unknown").title(),
            "area": "Unknown Area",
            "outlet_id": "OUT_AUTO",
            "outlet_name": v["outlet_name"],
            "outlet_type": "Kirana",
            "outlet_size": "Medium",
            "locality_type": "Mixed",
            "cold_storage_available": "Yes" if prod_group in ("Dairy", "Beverages") else "No",
            "high_footfall": "Medium",
            "visited": "Yes",
            "product_name": v["product_name"].title(),
            "product_group": prod_group,
            "product_subgroup": prod_subgroup,
            "pitched": "Yes",
            "availability_before_pitch": "Unknown",
            "display_visibility": "Medium",
            "scheme_explained": "No",
            "retailer_interest_level": "High" if v["order_booked"] == "Yes" else "Medium",
            "order_booked": v["order_booked"],
            "bill_cut": "No",
            "pieces_ordered": v["pieces_ordered"],
            "pieces_sold_if_known": 0,
            "order_value_if_known": "",
            "competitor_present": "No",
            "competitor_brand": "",
            "retailer_objection_raw": "",
            "retailer_objection_category": "",
            "follow_up_needed": "No",
            "follow_up_priority": "",
            "follow_up_reason": "",
            "my_observation": v.get("my_observation", ""),
        }
        rows.append(row)
        
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Starting extraction using regex parser...")
    visits = parse_markdown_reports_regex()
    
    if visits:
        df = transform_to_dataframe(visits)
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Successfully generated {len(df)} rows and saved to {OUTPUT_CSV}")
    else:
        print("No data extracted.")
