import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Climate Zone Finder",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for styling (updated: label centering)
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
        /* vertical center label relative to input */
        display: flex;
        align-items: center;
        height: 48px;
    }
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #ddd;
    }
    /* make the REPORT button style a bit nicer */
    .stButton>button {
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
    The world is home to an incredible range of climatic conditions from dry deserts and cool
    alpine regions to humid coastal belts and temperate landscapes. Different countries 
    categorize their regions into climate zones to support climate-responsive planning and design.
    The Climate Zone Finder Tool helps you identify the climate zone of any Location across multiple 
    countries and provides suitable passive design strategies for buildings planned in that location. 
    Simply select the country, pick the location, and click 'Apply'.
    </div>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    df = pd.read_excel("US&InternationStations-ClimateZones.xlsx")
    return df

# Load the data
df = load_data()

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Create centered container for the form
col_left_spacer, col_form, col_right_spacer = st.columns([0.5, 3, 0.5])

with col_form:
    # Row 1: Country
    r1_label, r1_input = st.columns([1, 2.5])
    with r1_label:
        st.markdown('<div class="label-text">Country</div>', unsafe_allow_html=True)
    with r1_input:
        countries = sorted(df['Country'].unique())
        selected_country = st.selectbox('Country', countries, key='country', label_visibility='collapsed')

    # Row 2: Location (depends on country)
    r2_label, r2_input = st.columns([1, 2.5])
    with r2_label:
        st.markdown('<div class="label-text">Location</div>', unsafe_allow_html=True)
    with r2_input:
        filtered_locations = df[df['Country'] == selected_country]['Location'].unique()
        selected_location = st.selectbox('Location', sorted(filtered_locations), key='location', label_visibility='collapsed')

    # Row 3: Climate Zone (display only)
    r3_label, r3_input = st.columns([1, 2.5])
    with r3_label:
        st.markdown('<div class="label-text">Climate Zone</div>', unsafe_allow_html=True)
    with r3_input:
        result = df[(df['Country'] == selected_country) & (df['Location'] == selected_location)]
        if not result.empty:
            climate_zone = result.iloc[0]['Climate Zone']
            st.markdown(f'<p style="font-size: 24px; font-weight: bold; color: #dc3545; margin-top: 5px; margin-bottom: 8px; line-height: 1.2;">{climate_zone}</p>', unsafe_allow_html=True)
        else:
            climate_zone = None
            st.markdown('<p style="font-size: 24px; font-weight: bold; color: #dc3545; margin-top: 5px; margin-bottom: 8px; line-height: 1.2;">-</p>', unsafe_allow_html=True)

    # Row 4: Climate Zone Name (display only)
    r4_label, r4_input = st.columns([1, 2.5])
    with r4_label:
        st.markdown('<div class="label-text">Climate Zone Name</div>', unsafe_allow_html=True)
    with r4_input:
        if not result.empty:
            climate_zone_name = result.iloc[0]['Climate Zone Name']
            st.markdown(f'<p style="font-size: 18px; font-weight: 500; color: #555; margin-top: 5px; margin-bottom: 8px; line-height: 1.2;">{climate_zone_name}</p>', unsafe_allow_html=True)
        else:
            climate_zone_name = None
            st.markdown('<p style="font-size: 18px; font-weight: 500; color: #555; margin-top: 5px; margin-bottom: 8px; line-height: 1.2;">-</p>', unsafe_allow_html=True)

    # Row 5: Report button
    r5_label, r5_input = st.columns([1, 2.5])
    with r5_label:
        st.markdown('<div class="label-text">Click to generate report</div>', unsafe_allow_html=True)
    with r5_input:
        report_clicked = st.button('REPORT', type='primary', use_container_width=False)


# Display report below if button clicked
if 'report_clicked' in locals() and report_clicked and result is not None and not result.empty:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;"><p style="font-size: 56px; font-weight: 300; color: #dc3545; margin: 20px 0;">{climate_zone}</p></div>', unsafe_allow_html=True)
    
    # Display detailed information
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_report_left, col_report_center, col_report_right = st.columns([1, 2, 1])
    with col_report_center:
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 10px; border-left: 5px solid #ff6b35;">
                <h3 style="color: #333; margin-bottom: 20px;">Climate Zone Details</h3>
                <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Country:</strong> {selected_country}</p>
                <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Location:</strong> {selected_location}</p>
                <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Climate Zone (by ASHRAE Standard 169):</strong> <span style="color: #dc3545; font-weight: bold;">{climate_zone}</span></p>
                <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Climate Zone Name:</strong> {climate_zone_name}</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #999; padding: 20px;">
    Climate Zone Finder Dashboard | Data-driven Climate Analysis
    </div>
""", unsafe_allow_html=True)
