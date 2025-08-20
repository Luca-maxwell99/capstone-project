import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
import pandas as pd

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from etl_process.src.transform.load_operational import load_operational_data

def show_operational():
    st.header("Operational Pressure")

    df = load_operational_data()
    if df is None or df.empty:
        st.error("No data available")
        return

    # Filter out rows with missing performance data
    df_filtered = df.dropna(subset=['pct_seen_within_4hrs'])

    # --- KPI Summary Cards ---
    latest_period = df_filtered['period'].max()
    latest_df = df_filtered[df_filtered['period'] == latest_period]
    latest_df = latest_df[latest_df['attendances_type_1'] > 0]

    total_attendances = latest_df['attendances_type_1'].sum()
    total_breaches = latest_df['over_4hrs_type_1'].sum()
    avg_pct_seen = latest_df['pct_seen_within_4hrs'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Attendances", f"{int(total_attendances):,}")
    col2.metric("Total Breaches", f"{int(total_breaches):,}")
    col3.metric("Avg % Seen Within 4hrs", f"{avg_pct_seen:.1f}%")

    st.markdown("---")

    # --- Top vs Bottom Performing Trusts ---
    st.subheader(f"Top vs Bottom Performing Trusts – {latest_period.strftime('%B %Y')}")

    top5 = latest_df.sort_values('pct_seen_within_4hrs', ascending=False).head(5)
    bottom5 = latest_df.sort_values('pct_seen_within_4hrs').head(5)

    top5['Performance'] = 'Top'
    bottom5['Performance'] = 'Bottom'
    combined = pd.concat([top5, bottom5])
    combined['Color'] = combined['Performance'].map({'Top': 'blue', 'Bottom': 'red'})

    fig_dual = px.bar(
        combined,
        x='pct_seen_within_4hrs',
        y='org_name',
        orientation='h',
        color='Performance',
        color_discrete_map={'Top': 'blue', 'Bottom': 'red'},
        labels={'pct_seen_within_4hrs': '% Seen Within 4hrs', 'org_name': 'Trust'}
    )
    fig_dual.update_layout(xaxis=dict(ticksuffix='%'), yaxis_title='', xaxis_title='Performance')

    st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("---")

    # --- Trust-Level Performance Chart ---
    selected_trust = st.selectbox("Select Trust", df_filtered['org_name'].unique())
    trust_df = df_filtered[df_filtered['org_name'] == selected_trust]

    fig = px.line(
        trust_df,
        x='period',
        y='pct_seen_within_4hrs',
        title=f"{selected_trust} – % Seen Within 4 Hours Over Time",
        markers=True,
        labels={'pct_seen_within_4hrs': '% Seen Within 4hrs', 'period': 'Date'}
    )
    fig.update_layout(yaxis=dict(ticksuffix='%'), xaxis_title='Month', yaxis_title='Performance')

    st.plotly_chart(fig, use_container_width=True)
