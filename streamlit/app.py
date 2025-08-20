import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from nav_pages.home import show_home
from nav_pages.operational import show_operational


def main():
    st.set_page_config(
        page_title="NHS A&E Dashboard",
        page_icon="🏥",
        layout="wide"
    )

    st.title("🏥 NHS A&E Performance Dashboard")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        [
            "Overview",
            "Operational Pressure",
            "Geospatial Mapping",
            "Breach Analysis"
        ]
    )

    if page == "Overview":
        show_home()
    elif page == "Operational Pressure":
        show_operational()
    elif page == "Geospatial Mapping":
        show_geospatial()
    

if __name__ == "__main__":
    main()



