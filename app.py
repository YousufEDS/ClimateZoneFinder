import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Climate Zone Finder",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    .header-line {
        width: 100px;
        height: 4px;
        background-color: #ff6b35;
        margin: 0 auto 30px auto;
    }
    .description {
        text-align: center;
        color: #666;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 40px;
        padding: 0 20px;
    }
    .label-text {
        font-size: 18px;
        color: #555;
        font-weight: 500;
        margin-bottom: 0;
        display: flex;
        align-items: center;
        height: 48px;
    }
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #ddd;
    }
    .stButton > button {
        background-color: #dc3545;
        color: white;
        border-radius: 6px;
        padding: 8px 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">CLIMATE ZONE FINDER</div>', unsafe_allow_html=True)
st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

# Description
st.markdown("""
    <div class="description">
    Identify the climate zone of any location across the world using data from
    ASHRAE Standard 169. Select the country, pick the location, and click 'REPORT'.
    </div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("US&InternationStations-ClimateZones.xlsx")

df = load_data()

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)

# Centered form layout
col_left, col_center, col_right = st.columns([0.5, 3, 0.5])

with col_center:
    # Country
    r1_label, r1_input = st.columns([1, 2.5])
    with r1_label:
        st.markdown('<div class="label-text">Country</div>', unsafe_allow_html=True)
    with r1_input:
        countries = sorted(df["Country"].unique())
        selected_country = st.selectbox("Country", countries, key="country", label_visibility="collapsed")

    # Location
    r2_label, r2_input = st.columns([1, 2.5])
    with r2_label:
        st.markdown('<div class="label-text">Location</div>', unsafe_allow_html=True)
    with r2_input:
        locations = sorted(df[df["Country"] == selected_country]["Location"].unique())
        selected_location = st.selectbox("Location", locations, key="location", label_visibility="collapsed")

    # Fetch result row
    result = df[(df["Country"] == selected_country) & (df["Location"] == selected_location)]

    # Climate Zone numeric
    r3_label, r3_input = st.columns([1, 2.5])
    with r3_label:
        st.markdown('<div class="label-text">Climate Zone</div>', unsafe_allow_html=True)
    with r3_input:
        if not result.empty:
            climate_zone = result.iloc[0]["Climate Zone"]
            st.markdown(
                f'<p style="font-size: 24px; font-weight: bold; color: #dc3545;">{climate_zone}</p>',
                unsafe_allow_html=True,
            )
        else:
            climate_zone = None
            st.markdown('<p style="font-size: 24px; font-weight: bold; color: #dc3545;">-</p>',
                        unsafe_allow_html=True)

    # Climate Zone Name
    r4_label, r4_input = st.columns([1, 2.5])
    with r4_label:
        st.markdown('<div class="label-text">Climate Zone Name</div>', unsafe_allow_html=True)
    with r4_input:
        if not result.empty:
            climate_zone_name = result.iloc[0]["Climate Zone Name"]
            st.markdown(
                f'<p style="font-size: 18px; font-weight: 500; color: #555;">{climate_zone_name}</p>',
                unsafe_allow_html=True,
            )
        else:
            climate_zone_name = None
            st.markdown('<p style="font-size: 18px; font-weight: 500; color: #555;">-</p>',
                        unsafe_allow_html=True)

    # Report button
    r5_label, r5_input = st.columns([1, 2.5])
    with r5_label:
        st.markdown('<div class="label-text">Click to generate report</div>', unsafe_allow_html=True)
    with r5_input:
        report_clicked = st.button("REPORT", type="primary")

# -------------------------
# REPORT SECTION
# -------------------------
if report_clicked and not result.empty:

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Large Climate Zone Highlight
    st.markdown(
        f'<div style="text-align:center;"><p style="font-size:56px; font-weight:300; color:#dc3545;">{climate_zone}</p></div>',
        unsafe_allow_html=True,
    )

    # Info Box
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.markdown(f"""
            <div style="background-color:#f8f9fa; padding:30px; border-radius:10px; border-left:5px solid #ff6b35;">
                <h3 style="color:#333;">Climate Zone Details</h3>
                <p style="font-size:18px;"><strong>Country:</strong> {selected_country}</p>
                <p style="font-size:18px;"><strong>Location:</strong> {selected_location}</p>
                <p style="font-size:18px;"><strong>Climate Zone:</strong> 
                    <span style="color:#dc3545; font-weight:bold;">{climate_zone}</span></p>
                <p style="font-size:18px;"><strong>Climate Zone Name:</strong> {climate_zone_name}</p>
            </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # WORLD MAP
    # -------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🌍 Climate Zone on World Map")

    lat_selected = result.iloc[0]["Latitude"]
    lon_selected = result.iloc[0]["Longitude"]

    # Plot ALL locations with climate zones
    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location",
        hover_data={"Climate Zone": True, "Country": True},
        color="Climate Zone",
        projection="natural earth",
        size=[8] * len(df),
    )

    # Highlight selected location with red star
    fig.add_scattergeo(
        lat=[lat_selected],
        lon=[lon_selected],
        marker=dict(size=18, color="red", symbol="star"),
        name="Selected Location",
        hovertext=f"{selected_location} ({climate_zone})",
    )

    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#999; padding:20px;">
        Climate Zone Finder Dashboard | Data-driven Climate Analysis
    </div>
""", unsafe_allow_html=True)
