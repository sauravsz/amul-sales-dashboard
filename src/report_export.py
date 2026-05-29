"""
Report export for the Amul Sales Dashboard.
Generates downloadable HTML and Markdown reports.
"""

import pandas as pd
from datetime import datetime


def generate_html_report(cov, conv, exec_k, prod_stats, objection_dist, alerts, recs_summary):
    """Generate a styled HTML report for download/printing."""

    date_str = datetime.now().strftime("%B %d, %Y")

    # Build product table rows
    prod_rows = ""
    if prod_stats is not None and not prod_stats.empty:
        for _, r in prod_stats.iterrows():
            conv_color = "#10B981" if r.get("conversion_pct", 0) >= 40 else "#F59E0B" if r.get("conversion_pct", 0) >= 25 else "#EF4444"
            prod_rows += f"""
            <tr>
                <td>{r.get('product_name', '')}</td>
                <td>{r.get('product_group', '')}</td>
                <td>{int(r.get('pitches', 0))}</td>
                <td>{int(r.get('orders', 0))}</td>
                <td>{int(r.get('pieces', 0))}</td>
                <td style="color:{conv_color}; font-weight:600;">{r.get('conversion_pct', 0)}%</td>
                <td>{r.get('avg_order_size', 0)}</td>
                <td>{r.get('top_objection', '')}</td>
            </tr>
            """

    # Build alert rows
    alert_html = ""
    for a in alerts[:8]:
        alert_html += f"<li>{a['icon']} {a['message']}</li>"

    # Build recommendations
    rec_html = ""
    if recs_summary is not None and not recs_summary.empty:
        for _, r in recs_summary.head(8).iterrows():
            rec_html += f"<li><strong>{r.get('rule_name', '')}</strong> — {int(r.get('count', 0))} cases ({r.get('priority', '')})</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Amul Sales Report — {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: #fff; color: #1e293b;
            padding: 40px; max-width: 900px; margin: 0 auto;
            line-height: 1.6;
        }}
        h1 {{ font-size: 1.8rem; color: #312e81; margin-bottom: 4px; }}
        h2 {{ font-size: 1.2rem; color: #4338ca; margin: 24px 0 12px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }}
        .subtitle {{ color: #64748b; font-size: 0.9rem; margin-bottom: 20px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }}
        .kpi {{
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
            padding: 14px; text-align: center;
        }}
        .kpi-label {{ font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }}
        .kpi-value {{ font-size: 1.4rem; font-weight: 700; color: #312e81; }}
        table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.85rem; }}
        th {{ background: #f1f5f9; padding: 8px 12px; text-align: left; font-weight: 600; color: #475569; border-bottom: 2px solid #e2e8f0; }}
        td {{ padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }}
        tr:hover {{ background: #f8fafc; }}
        ul {{ margin: 8px 0 8px 20px; }}
        li {{ margin-bottom: 6px; font-size: 0.9rem; }}
        .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.75rem; text-align: center; }}
        @media print {{
            body {{ padding: 20px; }}
            .kpi-grid {{ break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <h1>🥛 Amul Focus Product Sales Report</h1>
    <p class="subtitle">Field Sales Performance Summary — Generated {date_str}</p>

    <h2>📊 Key Performance Indicators</h2>
    <div class="kpi-grid">
        <div class="kpi">
            <div class="kpi-label">Visit Days</div>
            <div class="kpi-value">{cov.get('total_visit_days', 0)}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Total Pitches</div>
            <div class="kpi-value">{cov.get('total_pitches', 0)}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Strike Rate</div>
            <div class="kpi-value">{conv.get('strike_rate', 0)}%</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Pieces Ordered</div>
            <div class="kpi-value">{conv.get('total_pieces_ordered', 0)}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Outlets Covered</div>
            <div class="kpi-value">{cov.get('unique_outlets', 0)}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Bill Cut Rate</div>
            <div class="kpi-value">{conv.get('bill_cut_rate', 0)}%</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Availability %</div>
            <div class="kpi-value">{exec_k.get('availability_pct', 0)}%</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">Est. Value</div>
            <div class="kpi-value">₹{conv.get('estimated_total_value', 0):,.0f}</div>
        </div>
    </div>

    <h2>📦 Product Performance</h2>
    <table>
        <thead>
            <tr><th>Product</th><th>Group</th><th>Pitches</th><th>Orders</th><th>Pieces</th><th>Conv %</th><th>Avg Order</th><th>Top Objection</th></tr>
        </thead>
        <tbody>{prod_rows}</tbody>
    </table>

    <h2>🔔 Key Alerts</h2>
    <ul>{alert_html if alert_html else "<li>No alerts at this time.</li>"}</ul>

    <h2>💡 Top Recommendations</h2>
    <ul>{rec_html if rec_html else "<li>No recommendations generated.</li>"}</ul>

    <h2>🔧 Execution Quality</h2>
    <ul>
        <li>Product availability before pitch: <strong>{exec_k.get('availability_pct', 0)}%</strong></li>
        <li>Scheme explained: <strong>{exec_k.get('scheme_explained_pct', 0)}%</strong></li>
        <li>Competitor presence: <strong>{exec_k.get('competitor_presence_pct', 0)}%</strong></li>
        <li>High-interest no-order cases: <strong>{exec_k.get('high_interest_no_order_count', 0)}</strong></li>
    </ul>

    <div class="footer">
        Amul Focus Product Sales Conversion Dashboard • Generated by Amul Sales Intel v2.0
    </div>
</body>
</html>"""

    return html
