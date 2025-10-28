import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from utils import load_data, train_traffic_model, find_optimal_routes

# --- Page Configuration ---
st.set_page_config(
    page_title="NexGen EcoRoute Optimizer",
    page_icon="🚚",
    layout="wide"
)

# --- Load Data and Train Model (cached for performance) ---
@st.cache_data
def load_and_prepare_data():
    df, df_traffic = load_data()
    return df, df_traffic

@st.cache_resource
def get_traffic_model(_df_traffic):
    model = train_traffic_model(_df_traffic)
    return model

df, df_traffic = load_and_prepare_data()
traffic_model = get_traffic_model(df_traffic)

# --- App Header ---
st.title("🚚 NexGen EcoRoute Optimizer")
st.markdown("An intelligent routing system to optimize for cost, time, and environmental impact.")

# --- Sidebar for User Inputs ---
st.sidebar.header("Route Selection")
origin_list = df['origin'].unique()
destination_list = df['destination'].unique()

selected_origin = st.sidebar.selectbox("Select Origin Warehouse", origin_list)
selected_destination = st.sidebar.selectbox("Select Destination Warehouse", destination_list)

st.sidebar.header("Optimization Preference")
st.sidebar.markdown("Define what matters most for this route.")
cost_weight = st.sidebar.slider("Cost Importance", 0.0, 1.0, 0.5, 0.05)
time_weight = st.sidebar.slider("Time Importance (Speed)", 0.0, 1.0, 0.3, 0.05)
env_weight = st.sidebar.slider("Environmental Importance", 0.0, 1.0, 0.2, 0.05)

# --- Main Logic ---
if st.sidebar.button("Find Optimal Route", type="primary"):
    if selected_origin == selected_destination:
        st.error("Origin and destination cannot be the same.")
    else:
        weights = {'cost': cost_weight, 'time': time_weight, 'env': env_weight}
        
        # Call the optimization function from utils.py
        optimal_routes_df = find_optimal_routes(df, selected_origin, selected_destination, weights, traffic_model)

        if optimal_routes_df.empty:
            st.warning("No direct routes found between the selected locations.")
        else:
            st.header("🏆 Recommended Routes")
            
            # --- Display Key Metrics for the TOP Route ---
            top_route = optimal_routes_df.iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Top Route", top_route['route_name'])
            col2.metric("Estimated Cost", f"₹{top_route['total_cost']:.2f}")
            col3.metric("Estimated Time", f"{top_route['travel_time_hours']:.2f} hrs")
            col4.metric("CO2 Emissions", f"{top_route['total_co2_kg']:.2f} kg")

            # --- Display Comparison Table (Data Analysis) ---
            st.subheader("Route Comparison")
            display_cols = [
                'route_name', 'distance_km', 'total_cost', 
                'travel_time_hours', 'total_co2_kg', 'optimization_score'
            ]
            st.dataframe(optimal_routes_df[display_cols].round(2), use_container_width=True)

            # --- Interactive Visualizations ---
            col_viz1, col_viz2 = st.columns(2)

            with col_viz1:
                # Bar Chart for Cost Comparison (Visualization 1)
                st.subheader("Cost Breakdown")
                cost_fig = px.bar(
                    optimal_routes_df, 
                    x='route_name', 
                    y=['fuel_cost', 'toll_cost'],
                    title="Fuel vs. Toll Costs",
                    labels={'value': 'Cost (INR)', 'variable': 'Cost Type'}
                )
                st.plotly_chart(cost_fig, use_container_width=True)
            
            with col_viz2:
                # Bar chart for CO2 Emissions (Visualization 2)
                 st.subheader("Environmental Impact")
                 env_fig = px.bar(
                    optimal_routes_df, 
                    x='route_name', 
                    y='total_co2_kg',
                    title="CO2 Emissions per Route",
                    labels={'total_co2_kg': 'CO2 (kg)'}
                 )
                 st.plotly_chart(env_fig, use_container_width=True)

            # Interactive Map (Visualization 3) - Needs lat/lon data
            # For now, we use placeholder coordinates for demonstration.
            st.subheader("Route Map Visualization")
            # In a real dataset, you would have lat/lon for each city.
            city_coords = {
                'Mumbai': [19.0760, 72.8777], 'Delhi': [28.7041, 77.1025],
                'Bangalore': [12.9716, 77.5946], 'Chennai': [13.0827, 80.2707],
                'Kolkata': [22.5726, 88.3639]
            }
            
            map_center = city_coords.get(selected_origin, [20.5937, 78.9629])
            m = folium.Map(location=map_center, zoom_start=5)

            # Add markers
            folium.Marker(city_coords[selected_origin], popup=f"Origin: {selected_origin}", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(city_coords[selected_destination], popup=f"Destination: {selected_destination}", icon=folium.Icon(color='red')).add_to(m)

            # Display the map
            st_folium(m, width=725, height=500)

else:
    st.info("Select your route and optimization preferences from the sidebar and click 'Find Optimal Route'.")