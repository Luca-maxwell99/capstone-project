import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

# Ensure project root is in sys.path for clean imports
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from etl_process.src.transform.load_summary import (
    load_latest_summary,
    load_national_trends,
    load_trust_12hr_summary
)

def show_home():
    st.set_page_config(page_title="NHS Dashboard Overview", layout="wide")

    # --- Header ---
    st.markdown("Explore A&E performance across NHS trusts — from breach rates to extreme delays and geospatial hotspots.")

    # --- Load Data ---
    summary_df = load_latest_summary()
    trend_df = load_national_trends()
    trust_df = load_trust_12hr_summary()

    if summary_df.empty or trend_df.empty or trust_df.empty:
        st.warning("No data available for the selected period.")
        st.stop()

    latest_month = summary_df['month'].max()

    # --- Trend Chart ---
    st.subheader("📈 National Performance Over Time")
    fig = px.line(
        trend_df,
        x="month",
        y="pct_seen_within_4hrs",
        title="National % Seen Within 4 Hours",
        markers=True,
        labels={"pct_seen_within_4hrs": "% Seen Within 4 Hours", "month": "Month"},
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # --- Trusts to Watch ---
    st.subheader("Trusts to Watch — 12-Hour Breaches")

    if "org_name" in trust_df.columns and "patients_12hr_wait" in trust_df.columns:
        top_trusts = trust_df.sort_values("patients_12hr_wait", ascending=False).head(5)

        st.markdown("These trusts reported the highest number of patients waiting over 12 hours in the latest period:")

        cols = st.columns(len(top_trusts))

        for col, (_, row) in zip(cols, top_trusts.iterrows()):
            col.metric(
                label=f"{row['org_name']}",
                value=f"{row['patients_12hr_wait']:,}"
            )
    else:
        st.error("Trust-level data is missing required columns. Please check your SQL query or data source.")
