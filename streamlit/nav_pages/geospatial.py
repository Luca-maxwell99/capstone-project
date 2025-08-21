import streamlit as st
import pandas as pd
import plotly.express as px
from etl_process.src.transform.load_operational import load_geospatial_data

def show_geospatial():
    """
    Streamlit page displaying a geospatial map of NHS A&E pressure.

    Features:
    - KPI showing total 12-hour waits for the latest period.
    - Scatter map showing NHS trusts with 12-hour breaches.
    - Interactive hover showing trust name, patients waiting, and type 1 attendances.
    """
    # Configure Streamlit page
    st.set_page_config(page_title="Geospatial Mapping", layout="wide")
    st.title("🗺️ NHS A&E Pressure: Geospatial View")

    # Load data
    df = load_geospatial_data()

    # Stop early if no data
    if df.empty:
        st.warning("No data available to display.")
        st.stop()

    # Filter for latest period
    latest_period = df["period"].max()
    latest_df = df[df["period"] == latest_period]

    st.markdown(f"Showing trusts with 12-hour waits in **{latest_period.strftime('%B %Y')}**")

    # KPI: Total 12-hour waits for latest month
    total_12hr_waits = int(latest_df["patients_12hr_wait"].sum())
    st.metric(
        label=f"Total 12-Hour Waits ({latest_period.strftime('%B %Y')})",
        value=f"{total_12hr_waits:,}"
    )

    # Map Visualization
    fig = px.scatter_mapbox(
        latest_df,
        lat="latitude",
        lon="longitude",
        hover_name="org_name",
        hover_data=["patients_12hr_wait", "ae_attendances_type_1"],
        color="patients_12hr_wait",
        size="patients_12hr_wait",
        color_continuous_scale="Reds",  # Red for high 12-hour waits
        size_max=30,
        zoom=5,
        height=600
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(title="12-Hour Waits")
    )

    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Show full trust-level table"):
        st.dataframe(latest_df.sort_values("patients_12hr_wait", ascending=False).reset_index(drop=True))
