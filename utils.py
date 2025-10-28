import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

# --- Data Loading and Preparation ---
def load_data():
    """
    Loads and merges all necessary data files.
    In a real scenario, you'd load multiple CSVs. Here we simulate.
    """
    # Load the base routes
    routes = pd.read_csv('data/routes_distance.csv')

    # --- SIMULATE ADDITIONAL DATA for a complete solution ---
    # Simulate vehicle data
    vehicles = pd.DataFrame({
        'vehicle_type': ['Van', 'Truck', 'Refrigerated Unit'],
        'fuel_efficiency_kmpl': [12, 7, 5],
        'co2_emissions_g_km': [200, 350, 450]
    })
    
    # Simulate route-specific costs (Tolls) and assign a random vehicle
    routes['toll_cost'] = (routes['distance_km'] * 0.5).round(2) # Example toll calculation
    routes['vehicle_type'] = 'Truck' # Assign a default for simplicity

    # Merge data
    df = pd.merge(routes, vehicles, on='vehicle_type', how='left')
    
    # Simulate traffic data for the ML model
    # This creates a dummy dataset for predicting traffic delays
    df_traffic = df.sample(n=500, replace=True).reset_index(drop=True)
    df_traffic['hour_of_day'] = pd.np.random.randint(0, 24, size=len(df_traffic))
    # Simple logic: more traffic during peak hours
    df_traffic['traffic_delay_minutes'] = (df_traffic['hour_of_day'] - 12).abs() * pd.np.random.uniform(0.5, 2.5, size=len(df_traffic))
    df_traffic['traffic_delay_minutes'] = df_traffic['traffic_delay_minutes'].round()

    return df, df_traffic

# --- Machine Learning Model (For Advanced Features Bonus) ---
def train_traffic_model(df_traffic):
    """
    Trains a simple model to predict traffic delays.
    """
    if 'traffic_delay_minutes' not in df_traffic.columns:
        return None
        
    X = df_traffic[['distance_km', 'hour_of_day']]
    y = df_traffic['traffic_delay_minutes']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Model trained with score: {model.score(X_test, y_test):.2f}")
    return model

# --- Core Optimization Logic ---
def find_optimal_routes(df, origin, destination, weights, traffic_model):
    """
    Calculates route scores based on user-defined weights.
    """
    # Filter for possible routes
    possible_routes = df[(df['origin'] == origin) & (df['destination'] == destination)].copy()
    if possible_routes.empty:
        return pd.DataFrame()

    # --- 1. Calculate Core Metrics ---
    # Cost Metric
    fuel_price_per_litre = 95 # INR
    possible_routes['fuel_cost'] = (possible_routes['distance_km'] / possible_routes['fuel_efficiency_kmpl']) * fuel_price_per_litre
    possible_routes['total_cost'] = possible_routes['fuel_cost'] + possible_routes['toll_cost']

    # Time Metric (with ML prediction)
    avg_speed_kmph = 50
    current_hour = 14 # Assume it's 2 PM for prediction
    
    # Predict traffic delay for each route
    predicted_delays = traffic_model.predict(possible_routes[['distance_km']].assign(hour_of_day=current_hour))
    possible_routes['predicted_traffic_delay_minutes'] = predicted_delays.round()

    possible_routes['travel_time_hours'] = (possible_routes['distance_km'] / avg_speed_kmph) + (possible_routes['predicted_traffic_delay_minutes'] / 60)

    # Environmental Metric
    possible_routes['total_co2_kg'] = (possible_routes['distance_km'] * possible_routes['co2_emissions_g_km']) / 1000

    # --- 2. Normalize Metrics (scale 0 to 1) ---
    # So we can compare apples to oranges
    for col in ['total_cost', 'travel_time_hours', 'total_co2_kg']:
        min_val = possible_routes[col].min()
        max_val = possible_routes[col].max()
        if (max_val - min_val) > 0:
            possible_routes[f'{col}_norm'] = (possible_routes[col] - min_val) / (max_val - min_val)
        else:
            possible_routes[f'{col}_norm'] = 0


    # --- 3. Calculate Weighted Score ---
    possible_routes['optimization_score'] = (
        weights['cost'] * possible_routes['total_cost_norm'] +
        weights['time'] * possible_routes['travel_time_hours_norm'] +
        weights['env'] * possible_routes['total_co2_kg_norm']
    )

    # Return top 3 routes, sorted by the lowest score
    return possible_routes.sort_values('optimization_score').head(3)