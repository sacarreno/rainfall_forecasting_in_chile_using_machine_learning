import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
import pickle

# Set up the app
st.set_page_config(page_title="Chile Rainfall Forecast", layout="wide")
st.title("🌧️ Chile Rainfall Forecasting Dashboard")

# Sidebar for user inputs
with st.sidebar:
    st.header("Settings")
    selected_station = st.selectbox(
        "Select Weather Station",
        ["Calama", "La Serena", "Santiago", "Valdivia", "Punta Arenas"]
    )
    forecast_year = st.slider("Forecast Year", 2024, 2030, 2026)
    show_details = st.toggle("Show Technical Details")

# Load model and data (in a real app, you'd load your actual model)
@st.cache_data
def load_data():
    # This would be replaced with your actual data loading
    data = pd.DataFrame({
        'Station': ["Calama", "La Serena", "Santiago", "Valdivia", "Punta Arenas"],
        '2024': [0.8, 110.2, 158.3, 1190.5, 160.1],
        '2025': [0.9, 113.5, 161.2, 1208.7, 162.9],
        '2026': [1.0, 116.8, 163.0, 1227.3, 165.6],
        'Risk': ["Extreme Drought", "Moderate", "Moderate", "Low", "Volatile"]
    })
    return data

data = load_data()

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Forecast for {selected_station}")
    
    # Get station data
    station_data = data[data['Station'] == selected_station].iloc[0]
    
    # Display metrics
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric(
            label=f"{forecast_year} Forecast",
            value=f"{station_data[str(forecast_year)]:.1f} mm",
            delta=f"{(station_data[str(forecast_year)] - station_data[str(forecast_year-1)]):.1f} mm from {forecast_year-1}"
        )
    with metric_col2:
        st.metric(
            label="Drought Risk",
            value=station_data['Risk']
        )
    
    # Show historical trend chart
    st.subheader("Historical Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    years = ['2024', '2025', '2026']
    ax.plot(years, [station_data[year] for year in years], marker='o')
    ax.set_xlabel("Year")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title(f"{selected_station} Rainfall Projection")
    st.pyplot(fig)

with col2:
    st.subheader("Regional Comparison")
    
    # Bar chart comparing stations
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data, x='Station', y=str(forecast_year), palette="Blues_d")
    plt.xticks(rotation=45)
    plt.title(f"Projected {forecast_year} Rainfall by Station")
    plt.ylabel("Rainfall (mm)")
    st.pyplot(fig2)
    
    # Data table
    st.dataframe(
        data.set_index('Station')[['2024', '2025', '2026', 'Risk']],
        use_container_width=True
    )

# Technical details section
if show_details:
    st.expander("Technical Details").write("""
    **Model Details:**
    - Algorithm: XGBoost Regressor
    - RMSE: 24.5 mm
    - Features used: Historical rainfall, station location, seasonal patterns
    
    **Data Sources:**
    - Chilean Directorate of Water Resources (DGA)
    - 56 years of historical data (1969-2025)
    """)

# Recommendations section
st.subheader("Recommendations")
if selected_station == "Calama":
    st.warning("🚨 Extreme drought conditions expected. Recommendations:")
    st.write("- Implement strict water rationing")
    st.write("- Prioritize drought-resistant crops")
elif selected_station == "Valdivia":
    st.success("✅ Normal rainfall expected. Recommendations:")
    st.write("- Maintain current water management plans")
    st.write("- Optimal conditions for rainfed agriculture")
else:
    st.info("ℹ️ Moderate rainfall expected. Recommendations:")
    st.write("- Monitor reservoir levels")
    st.write("- Prepare contingency plans for dry spells")

# Footer
st.markdown("---")
st.caption("""
*Data Science Project - Chile Rainfall Forecasting*\n
For official use with Chilean water authorities
""")