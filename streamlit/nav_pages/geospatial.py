import streamlit as st
import pandas as pd
import plotly.express as px
from etl_process.src.transform.load_operational import load_geospatial_data

def show_geospatial():
    st.set_page_config(page_title="Geospatial Mapping", layout="wide")
    st.title("🗺️ NHS A&E Pressure: Geospatial View")

    df = load_geospatial_data()

    if df.empty:
        st.warning("No data available to display.")
        st.stop()

    latest_period = df["period"].max()
    latest_df = df[df["period"] == latest_period]

    st.markdown(f"Showing trusts with 12-hour waits in **{latest_period.strftime('%B %Y')}**")

    fig = px.scatter_mapbox(
        latest_df,
        lat="latitude",
        lon="longitude",
        hover_name="org_name",
        hover_data=["patients_12hr_wait", "ae_attendances_type_1"],
        color="patients_12hr_wait",
        size="patients_12hr_wait",
        zoom=5,
        height=600
    )

    fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
