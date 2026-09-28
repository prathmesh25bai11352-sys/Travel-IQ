import streamlit as st
import pandas as pd
import random

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="TravelIQ | AI Budget Optimizer", page_icon="✈️", layout="wide")

# ==========================================
# MOCK DATA DICTIONARIES (To simulate backend)
# ==========================================
CITY_BASE_RATES = {
    "Goa, India": 2300,
    "New Delhi, India": 2100,
    "Mumbai, India": 2800,
    "Manali, Himachal": 1900,
    "Paris, France": 9500
}

WEATHER_DATABASE = {
    "Goa, India": {"Winter": "28°C ☀️ Perfect beach weather", "Summer": "35°C 🥵 Hot & Humid", "Monsoon": "26°C 🌧️ Heavy Rains"},
    "New Delhi, India": {"Winter": "15°C 🌫️ Cool & Foggy", "Summer": "42°C 🏜️ Extreme Heat", "Monsoon": "30°C ⛈️ Humid showers"},
    "Mumbai, India": {"Winter": "25°C 🌤️ Pleasant", "Summer": "34°C 💦 Highly Humid", "Monsoon": "27°C 🌊 Flooding risks"},
    "Manali, Himachal": {"Winter": "2°C ❄️ Snowfall expected", "Summer": "20°C 🏔️ Cool & Clear", "Monsoon": "15°C ⚠️ Landslide warnings"},
    "Paris, France": {"Winter": "5°C 🧥 Chilly & Overcast", "Summer": "25°C 🌻 Sunny & Warm", "Monsoon": "12°C ☔ Light drizzling"}
}

# ==========================================
# SIDEBAR: TRIP PARAMETERS (Inputs)
# ==========================================
st.sidebar.title("⚙️ Trip Parameters")
st.sidebar.markdown("Configure your travel details below:")

city_selection = st.sidebar.selectbox("🌆 Select Destination City", list(CITY_BASE_RATES.keys()))
duration = st.sidebar.number_input("📅 Duration (Days)", min_value=1, max_value=30, value=4)
no_of_persons = st.sidebar.number_input("👥 No. of Persons", min_value=1, max_value=20, value=2)
season = st.sidebar.selectbox("🌦️ Season", ["Winter", "Summer", "Monsoon"])
travel_style = st.sidebar.select_slider("🧳 Travel Style", options=["Budget", "Comfort", "Luxury"], value="Comfort")

# ==========================================
# AI PREDICTION LOGIC (Simulating ML Core)
# ==========================================
base_rate = CITY_BASE_RATES[city_selection]

# Style Multiplier
style_mult = 0.65 if travel_style == "Budget" else (2.4 if travel_style == "Luxury" else 1.0)
# Season Multiplier
season_mult = 1.2 if season == "Winter" else (0.8 if season == "Monsoon" else 1.0)

# Calculate Totals
total_budget = int(base_rate * duration * no_of_persons * style_mult * season_mult)
stay_cost = int(total_budget * 0.41)
transport_cost = int(total_budget * 0.34)
food_cost = int(total_budget * 0.20)
activities_cost = total_budget - (stay_cost + transport_cost + food_cost)

# ==========================================
# MAIN DASHBOARD UI
# ==========================================
st.title("✈️ TravelIQ: AI-Powered Travel Planner")
st.markdown("Predict travel expenses, optimize your budget, and track real-time spending.")

# Create Tabs for different features
tab1, tab2, tab3 = st.tabs(["🔮 AI Budget Optimizer", "⛅ Weather Insights", "📊 Live Expense Tracker"])

# ------------------------------------------
# TAB 1: BUDGET OPTIMIZATION
# ------------------------------------------
with tab1:
    st.subheader(f"AI Cost Prediction for {city_selection}")
    
    # Highlight Total Budget
    st.metric(label="Total Estimated Budget", value=f"₹ {total_budget:,}")
    
    # Cost Breakdown
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏨 Stay (41%)", f"₹ {stay_cost:,}")
    col2.metric("✈️ Transport (34%)", f"₹ {transport_cost:,}")
    col3.metric("🍔 Food (20%)", f"₹ {food_cost:,}")
    col4.metric("🎟️ Activities (5%)", f"₹ {activities_cost:,}")
    
    st.divider()
    
    # Budget Optimization Engine
    st.subheader("💡 AI Budget Optimization Tips")
    if travel_style == "Luxury":
        st.success(f"**Optimization:** Switching to 4-star boutique hotels can save up to ₹{int(total_budget * 0.25):,} without compromising your experience.")
    elif travel_style == "Comfort":
        st.info(f"**Optimization:** Switch to a highly-rated 3-star property on days 2 and 3 to save ₹{int(stay_cost * 0.27):,}.")
    else:
        st.warning(f"**Optimization:** Booking local transport passes in advance can cut your transit costs by ₹{int(transport_cost * 0.20):,}.")

# ------------------------------------------
# TAB 2: WEATHER FORECAST
# ------------------------------------------
with tab2:
    st.subheader(f"Expected Weather Conditions in {city_selection}")
    weather_info = WEATHER_DATABASE.get(city_selection, {}).get(season, "Weather data unavailable.")
    
    col_w1, col_w2 = st.columns([1, 2])
    with col_w1:
        st.info(f"**Selected Season:** {season}")
    with col_w2:
        st.success(f"**Forecast:** {weather_info}")
        
    st.markdown("### Packing Recommendations")
    if season == "Winter":
        st.write("• Heavy jackets, thermals, lip balm, and warm socks.")
    elif season == "Monsoon":
        st.write("• Waterproof shoes, umbrellas, raincoats, and mosquito repellent.")
    else:
        st.write("• Sunscreen, sunglasses, light cotton clothing, and hydration packs.")

# ------------------------------------------
# TAB 3: EXPENSE TRACKER
# ------------------------------------------
with tab3:
    st.subheader("Interactive Expense Tracker")
    st.markdown("Log your actual expenses on the trip and see if you are staying within the AI's predicted budget.")
    
    # Initialize session state for the tracker dataframe
    if 'tracker_df' not in st.session_state:
        st.session_state.tracker_df = pd.DataFrame({
            "Category": ["Stay", "Transport", "Food", "Activities", "Misc"],
            "Predicted Budget (₹)": [stay_cost, transport_cost, food_cost, activities_cost, 0],
            "Actual Spent (₹)": [0, 0, 0, 0, 0]
        })
    else:
        # Update predicted values dynamically if user changes inputs
        st.session_state.tracker_df["Predicted Budget (₹)"] = [stay_cost, transport_cost, food_cost, activities_cost, 0]

    # Editable Dataframe
    edited_df = st.data_editor(
        st.session_state.tracker_df, 
        use_container_width=True,
        hide_index=True,
        disabled=["Category", "Predicted Budget (₹)"] # Only allow editing the "Actual Spent" column
    )
    
    # Calculate Variance
    total_actual = edited_df["Actual Spent (₹)"].sum()
    variance = total_budget - total_actual
    
    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.metric("Predicted Total", f"₹ {total_budget:,}")
    col_t2.metric("Actual Total", f"₹ {total_actual:,}")
    
    if variance > 0:
        col_t3.metric("Remaining Budget", f"₹ {variance:,}", delta=f"Under budget", delta_color="normal")
    else:
        col_t3.metric("Remaining Budget", f"₹ {variance:,}", delta=f"Over budget", delta_color="inverse")