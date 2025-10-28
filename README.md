# NexGen EcoRoute Optimizer



**A Streamlit web application for intelligent, multi-objective route optimization.**

This project is a functional prototype built in response to the **NexGen Logistics Innovation Challenge**. It is an interactive web application designed to help logistics planners at NexGen move beyond simple distance-based routing. The "EcoRoute Optimizer" finds the truly optimal route by balancing three competing priorities: **Cost**, **Speed (Time)**, and **Environmental Impact**.

---

## Key Features



* Multi-Objective Optimization: Allows users to define what "optimal" means by using sliders to set the importance of cost, time, and sustainability.
* Intelligent Predictions: Uses a `scikit-learn` machine learning model to predict traffic delays based on the time of day, adding a layer of realism to time estimates.
* Detailed Cost Analysis: Calculates a route's total cost by factoring in both fuel consumption (based on vehicle type) and specific toll charges.
* Sustainability Tracking: Estimates the total CO2 emissions (in kg) for each potential route, enabling green logistics decisions.
* Rich, Interactive UI: Built with Streamlit, the dashboard provides a clean user interface, interactive `Plotly` charts for comparison, and an interactive `Folium` map to visualize locations.

---

## The "Innovation": How It Works



The core of this tool is a multi-objective optimization model that runs in real-time.

1. **Metric Calculation:** For every possible route between the selected origin and destination, the app calculates three key metrics:

   * Total Cost: `(Fuel Cost based on vehicle fuel\\\_efficiency) + (Toll Charges)`
   * Total Time: `(Base Travel Time @ avg. speed) + (ML-Predicted Traffic Delay in minutes)`
   * Environmental Impact: `(Distance\\\_km \\\* CO2\\\_emissions\\\_g\\\_km) / 1000`

2. **Normalization:** Since these metrics are in different units (INR, Hours, and kg), they are normalized to a common 0-1 scale so they can be fairly compared.
3. **Weighted Scoring:** The user's slider inputs (e.g., 50% Cost, 20% Time, 30% Environment) are applied as weights to these normalized scores. This creates a single **Optimization Score** for each route.
4. **Recommendation:** The app ranks the routes by this "Optimization Score" and recommends the top 3 options, with the lowest score being the best.

---



## Tech Stack



* **Core:** Python
* **Web Framework:** Streamlit
* **Data Analysis:** Pandas
* **Machine Learning:** Scikit-learn
* **Data Visualization:** Plotly
* **Mapping:** Folium \& `streamlit-folium`

---



## 📂 Project Structure



---

Follow these instructions to get a local copy up and running.

### Prerequisites



* Python 3.8 or newer
* `pip` (Python package installer)

1. **Create a virtual environment (Recommended):**

    `bash python -m venv venv `

*On macOS/Linux:*

    `bash source venv/bin/activate `

*On Windows:*

    `bash .\\\\venv\\\\Scripts\\\\activate `

2. **Install the required dependencies:**

       `bash pip install -r requirements.txt `

3. **Place your data:**
   Ensure your `routes\\\_distance.csv` file (and any other datasets) are placed in the `data/` folder.
4. **Run the application:**

       `bash streamlit run app.py `

5. Open your browser and navigate to the local URL provided (usually `http://localhost:8501`).

   ---

   ## 🏃‍♀️ How to Use the App

   

1. Use the sidebar to select an **Origin Warehouse**.
2. Select a **Destination Warehouse**.
3. Adjust the three sliders to reflect your **Optimization Preference** (e.g., prioritize Cost over Time).
4. Click the **"Find Optimal Route"** button.
5. Analyze the results in the main panel, which shows key metrics, a comparison table, and interactive charts.

   ---

