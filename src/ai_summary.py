"""
AI-powered summary generation for the Amul Sales Dashboard.
Uses Google Gemini API with fallback to template-based summary.
"""


def generate_template_summary(coverage, conversion, exec_kpis, product_stats, objection_dist):
    """Generate a structured template-based summary when no API key is available."""
    lines = []
    lines.append("## 📊 Weekly Field Sales Summary")
    lines.append("")
    
    # --- Overall Performance ---
    lines.append("### Overall Performance")
    lines.append(f"- **{coverage.get('total_visit_days', 0)}** outlet-visit days across **{coverage.get('unique_outlets', 0)}** unique outlets")
    lines.append(f"- **{coverage.get('total_pitches', 0)}** total product pitches made")
    lines.append(f"- **{conversion.get('total_orders', 0)}** orders booked ({conversion.get('conversion_rate', 0)}% conversion rate)")
    lines.append(f"- **Strike Rate**: {conversion.get('strike_rate', 0)}%")
    lines.append(f"- **{conversion.get('total_pieces_ordered', 0)}** total pieces ordered")
    lines.append(f"- **Avg pieces per order**: {conversion.get('avg_pieces_per_order', 0)}")
    if conversion.get('estimated_total_value', 0) > 0:
        lines.append(f"- **Estimated sales value**: ₹{conversion.get('estimated_total_value', 0):,.0f}")
    lines.append("")
    
    # --- Top Products ---
    if product_stats is not None and not product_stats.empty:
        lines.append("### 🏆 Top Performing Products")
        top = product_stats.nlargest(3, "conversion_pct")
        for _, row in top.iterrows():
            lines.append(f"- **{row['product_name']}**: {row['conversion_pct']}% conversion, {int(row['pieces'])} pieces, avg order {row['avg_order_size']} pcs")
        lines.append("")
        
        lines.append("### ⚠️ Products Needing Attention")
        bottom = product_stats.nsmallest(3, "conversion_pct")
        for _, row in bottom.iterrows():
            obj_text = f" (Top objection: {row['top_objection']})" if row.get('top_objection') else ""
            lines.append(f"- **{row['product_name']}**: {row['conversion_pct']}% conversion{obj_text}")
        lines.append("")
    
    # --- Execution Quality ---
    lines.append("### 🔧 Execution Quality")
    lines.append(f"- Product availability before pitch: **{exec_kpis.get('availability_pct', 0)}%**")
    lines.append(f"- Scheme explained: **{exec_kpis.get('scheme_explained_pct', 0)}%**")
    lines.append(f"- Competitor presence: **{exec_kpis.get('competitor_presence_pct', 0)}%**")
    lines.append(f"- High-interest no-order cases: **{exec_kpis.get('high_interest_no_order_count', 0)}**")
    lines.append(f"- Pitches without prior stock: **{exec_kpis.get('pitch_without_stock_count', 0)}**")
    lines.append("")
    
    # --- Top Objections ---
    if objection_dist is not None and not objection_dist.empty:
        lines.append("### 🚫 Top Objection Categories")
        top_obj = objection_dist.head(5)
        for _, row in top_obj.iterrows():
            lines.append(f"- {row['objection']}: **{int(row['count'])}** occurrences ({row['pct']}%)")
        lines.append("")
    
    # --- Recommendations ---
    lines.append("### 💡 Recommended Next Actions")
    lines.append("1. **Revisit high-interest outlets** that didn't convert — they represent the strongest near-term opportunity")
    lines.append("2. **Coordinate stock availability** with distributor for products with interest but no stock")
    lines.append("3. **Improve display visibility** for impulse products (cookies, chocolates) in high-footfall outlets")
    if exec_kpis.get('scheme_explained_pct', 100) < 70:
        lines.append("4. **Increase scheme communication** — only {:.0f}% of pitches included scheme explanation".format(exec_kpis.get('scheme_explained_pct', 0)))
    if exec_kpis.get('competitor_presence_pct', 0) > 40:
        lines.append("5. **Strengthen competitive positioning** — competitor presence is high at {:.0f}%".format(exec_kpis.get('competitor_presence_pct', 0)))
    lines.append("")
    
    return "\n".join(lines)


def generate_ai_summary(api_key, coverage, conversion, exec_kpis, product_stats, objection_dist):
    """Generate an AI-powered summary using Gemini API."""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Build context
        context_parts = [
            f"Total outlet-visit days: {coverage.get('total_visit_days', 0)}",
            f"Unique outlets covered: {coverage.get('unique_outlets', 0)}",
            f"Total pitches: {coverage.get('total_pitches', 0)}",
            f"Orders booked: {conversion.get('total_orders', 0)}",
            f"Strike rate: {conversion.get('strike_rate', 0)}%",
            f"Conversion rate: {conversion.get('conversion_rate', 0)}%",
            f"Total pieces ordered: {conversion.get('total_pieces_ordered', 0)}",
            f"Avg pieces per order: {conversion.get('avg_pieces_per_order', 0)}",
            f"Availability before pitch: {exec_kpis.get('availability_pct', 0)}%",
            f"Scheme explained: {exec_kpis.get('scheme_explained_pct', 0)}%",
            f"Competitor presence: {exec_kpis.get('competitor_presence_pct', 0)}%",
            f"High-interest no-order count: {exec_kpis.get('high_interest_no_order_count', 0)}",
        ]
        
        if product_stats is not None and not product_stats.empty:
            top_3 = product_stats.nlargest(3, "conversion_pct")
            bottom_3 = product_stats.nsmallest(3, "conversion_pct")
            context_parts.append(f"Top 3 products by conversion: {', '.join(top_3['product_name'].tolist())}")
            context_parts.append(f"Bottom 3 products by conversion: {', '.join(bottom_3['product_name'].tolist())}")
        
        if objection_dist is not None and not objection_dist.empty:
            top_obj = objection_dist.head(3)
            context_parts.append(f"Top objections: {', '.join(top_obj['objection'].tolist())}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are preparing a concise weekly field sales performance summary for an Amul territory manager.

Here is the field data summary:
{context}

The focus products are: More Tin Paneer, Amul Aata, Amul Cookies, Amul Chocolates, Organic Kabuli Chana, Organic Toor Dal, Organic Masoor Dal, Organic Rajma.

Write a structured summary covering:
1. Overall field productivity (2-3 sentences)
2. Best performing products and why (2-3 bullet points)
3. Weakest products and likely causes (2-3 bullet points)
4. Outlet type insights (1-2 sentences)
5. Major objection patterns (2-3 bullet points)
6. Top 5 specific, actionable recommendations for next week

Keep it factual, practical, and specific. Use bullet points. Don't repeat raw numbers — interpret them into insights.
Format in clean markdown."""
        
        response = model.generate_content(prompt)
        return response.text
        
    except ImportError:
        return "⚠️ `google-generativeai` package not installed. Install it with: `pip install google-generativeai`"
    except Exception as e:
        return f"⚠️ AI summary generation failed: {str(e)}\n\nFalling back to template summary..."


def get_objection_distribution(df):
    """Get objection category distribution for summary input."""
    import pandas as pd
    
    no_order = df[(df["order_booked"] == "No") & (df["retailer_objection_category"] != "")]
    
    if no_order.empty:
        return pd.DataFrame(columns=["objection", "count", "pct"])
    
    dist = no_order["retailer_objection_category"].value_counts().reset_index()
    dist.columns = ["objection", "count"]
    dist["pct"] = round(dist["count"] / dist["count"].sum() * 100, 1)
    
    return dist
