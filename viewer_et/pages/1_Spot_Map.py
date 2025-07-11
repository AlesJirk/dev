# pages/1_Spot_Map.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import utils  # Import our shared code

# --- UI and Charting Functions SPECIFIC to this page ---
def setup_sidebar():
    st.sidebar.header("Spot Map Controls")
    if 'date_picker_range' not in st.session_state:
        st.session_state.date_picker_range = (date(2025, 6, 16), date(2025, 6, 16))
    st.sidebar.date_input("Select date range", key="date_picker_range")
    selected_range = st.session_state.date_picker_range
    if len(selected_range) == 2: start_date, end_date = selected_range
    else: start_date = end_date = selected_range[0]
    step_options = {'H': 'Hourly', 'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly'}
    selected_step = st.sidebar.selectbox("Select step", options=list(step_options.keys()), format_func=lambda k: step_options[k])
    selected_countries_a2 = st.sidebar.multiselect("Country", options=list(utils.CODE_A2_TO_A3.keys()), default=utils.DEFAULT_SELECTION_A2,
        format_func=lambda code: f"{utils.COUNTRY_NAMES.get(utils.CODE_A2_TO_A3.get(code, ''), code)} ({code})")
    return start_date, end_date, selected_countries_a2, selected_step

def draw_spot_chart(data, start_date, end_date, selected_step):
    st.subheader("Spot")
    if data.empty:
        st.warning("Please select a valid date range and at least one country.")
        return
    if selected_step == 'H':
        data_to_plot = data
    else:
        data_with_index = data.set_index('timestamp')
        aggregated_data = data_with_index.groupby('country_code').resample(rule=selected_step)['value'].mean()
        data_to_plot = aggregated_data.reset_index()
    fig = px.line(data_to_plot, x="timestamp", y="value", color="country_code",
                  labels={"value": "value", "timestamp": "", "country_code": "variable"}, template="plotly_dark")
    if start_date == end_date: title_text = start_date.strftime('%Y-%m-%d')
    else: title_text = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    fig.update_layout(legend_title_text='variable', xaxis_title=title_text,
                      yaxis_range=[0, max(155, data['value'].max() * 1.05 if not data.empty else 155)],
                      margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

def draw_map_chart(spot_data, geo_data):
    st.subheader("Map")
    if geo_data is None: return
    if spot_data.empty:
        st.warning("No data to display on the map for the selected date range.")
        return
    map_data = spot_data.groupby('country_code')['value'].mean().reset_index(name='base_price')
    merged_data = geo_data.merge(map_data, left_on='iso_a2', right_on='country_code', how='left')
    merged_data['base_price_text'] = merged_data['base_price'].apply(lambda x: f'{x:.2f}' if pd.notna(x) else '')
    rep_points = merged_data.geometry.representative_point()
    merged_data['lon'] = rep_points.x
    merged_data['lat'] = rep_points.y
    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locations=merged_data['id'], z=merged_data['base_price'],
        geojson=merged_data.__geo_interface__, featureidkey="properties.id",
        colorscale="jet", zmin=0, zmax=150,
        colorbar_title_text="base", marker_line_color='darkgray', marker_line_width=0.5,
    ))
    fig.add_trace(go.Scattergeo(
        lon=merged_data['lon'], lat=merged_data['lat'], text=merged_data['base_price_text'],
        mode='text', textfont=dict(color='black', size=10), showlegend=False,
    ))
    fig.update_layout(
        title_text="Map", template="plotly_dark", margin={"r":0, "t":40, "l":0, "b":0},
        geo=dict(scope='europe', bgcolor='rgba(0,0,0,0)', showland=False,
                 lataxis_range=[35, 70], lonaxis_range=[-15, 40]),
        coloraxis_colorbar=dict(title="base", yanchor="middle", y=0.5, len=0.8)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Main Page Logic ---
def main():
    st.title("Spot Price Analysis")
    st.markdown("---")
    
    start_date, end_date, country_selection_codes, selected_step = setup_sidebar()
    # Use the shared functions from utils.py
    all_spot_data = utils.generate_spot_data(start_date, end_date, list(utils.CODE_A2_TO_A3.keys()))
    europe_geodata = utils.get_europe_geodata()
    
    line_chart_data = all_spot_data[all_spot_data['country_code'].isin(country_selection_codes)]
    col1, col2 = st.columns([3, 2]) # Give a bit more space to the line chart
    with col1:
        draw_spot_chart(line_chart_data, start_date, end_date, selected_step)
    with col2:
        draw_map_chart(all_spot_data, europe_geodata)

if __name__ == "__main__":
    main()