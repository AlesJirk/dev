# main_app.py
import streamlit as st

# Set the page configuration for the entire app
st.set_page_config(
    page_title="Energy Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main welcome page content
st.title("Welcome to the Energy Trading Dashboard")
st.markdown("---")
st.header("Please select a tool from the sidebar to begin.")
st.info("This application provides tools for analyzing energy market data, including spot prices and spreads.")

st.markdown("""
### Available Tools:
- **Spot Map**: Visualize historical spot prices across Europe on a map and a time-series chart.
- **Data Browser**: (Under Construction) Browse and filter raw market data.
- **Spread Tool**: (Under Construction) Analyze and visualize price spreads between different markets.
""")