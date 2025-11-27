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

# Climate zone strategy mapping
def get_climate_strategies(zone_name):
    """Returns passive design strategies based on climate zone name"""
    strategies = {
        "Hot Dry": {
            "title": "Hot-Dry",
            "color": "#dc3545",
            "strategies": [
                {
                    "name": "Surface area to volume ratio",
                    "image": "images/surface_ratio.png",
                    "description": "In hot & dry regions, building's shape needs to be compact to reduce heat gain and losses, respectively. The surface to volume(S/V) ratio of the building should be as low as possible to minimize heat gain."
                },
                {
                    "name": "Evaporative Cooling",
                    "image": "images/evaporative_cooling.png",
                    "description": "Evaporative cooling is mostly effective in hot and dry climate where the humidity is low. Water in pools and fountains can be used as a cooling element along with cross-ventilating arrangement of openings."
                },
                {
                    "name": "Cool Roof",
                    "image": "images/cool_roof.png",
                    "description": "Cool roofs reflect most of the solar radiation and efficiently emit some of the absorbed radiation back into the atmosphere, instead of conducting it to the building below."
                }
            ]
        },
        "Hot Humid": {
            "title": "Hot-Humid",
            "color": "#ff6b35",
            "strategies": [
                {
                    "name": "Natural Ventilation",
                    "image": "images/natural_ventilation.png",
                    "description": "In hot-humid climates, maximizing natural ventilation is crucial. Cross-ventilation and stack ventilation help remove excess humidity and heat from indoor spaces."
                },
                {
                    "name": "Shading Devices",
                    "image": "images/shading_devices.png",
                    "description": "External shading devices like overhangs, louvers, and vegetation prevent direct solar radiation while allowing natural light and ventilation."
                },
                {
                    "name": "Elevated Buildings",
                    "image": "images/elevated_buildings.png",
                    "description": "Elevating buildings on stilts or pillars improves air circulation underneath, reduces ground moisture impact, and enhances cooling through natural ventilation."
                }
            ]
        },
        "Warm Humid": {
            "title": "Warm-Humid",
            "color": "#ffa500",
            "strategies": [
                {
                    "name": "Orientation and Layout",
                    "image": "images/orientation_layout.png",
                    "description": "Building orientation should maximize exposure to prevailing breezes while minimizing direct solar exposure. Open floor plans facilitate air movement."
                },
                {
                    "name": "Thermal Mass Control",
                    "image": "images/thermal_mass_control.png",
                    "description": "Use lightweight construction with low thermal mass to prevent heat storage. Materials should cool quickly during night hours."
                },
                {
                    "name": "Moisture Management",
                    "image": "images/moisture_management.png",
                    "description": "Design details should prevent moisture accumulation through proper drainage, vapor barriers, and moisture-resistant materials."
                }
            ]
        },
        "Mixed Dry": {
            "title": "Mixed-Dry",
            "color": "#28a745",
            "strategies": [
                {
                    "name": "Thermal Mass",
                    "image": "images/thermal_mass.png",
                    "description": "Use high thermal mass materials like concrete or masonry to store heat during day and release at night, moderating temperature swings."
                },
                {
                    "name": "Passive Solar Design",
                    "image": "images/passive_solar.png",
                    "description": "South-facing windows with proper overhangs capture winter sun for heating while blocking summer sun to reduce cooling needs."
                },
                {
                    "name": "Night Ventilation",
                    "image": "images/night_ventilation.png",
                    "description": "Open windows during cool nights to flush out daytime heat and cool thermal mass for the next day."
                }
            ]
        },
        "Mixed Humid": {
            "title": "Mixed-Humid",
            "color": "#17a2b8",
            "strategies": [
                {
                    "name": "Dehumidification",
                    "image": "images/dehumidification.png",
                    "description": "Incorporate passive dehumidification through proper ventilation design and moisture control strategies to maintain comfort."
                },
                {
                    "name": "Insulation Balance",
                    "image": "images/insulation_balance.png",
                    "description": "Moderate insulation levels balance heating and cooling needs while preventing condensation issues in varying humidity conditions."
                },
                {
                    "name": "Rainwater Management",
                    "image": "images/rainwater_management.png",
                    "description": "Effective gutters, downspouts, and drainage systems prevent water intrusion and manage high precipitation levels."
                }
            ]
        },
        "Cool Dry": {
            "title": "Cool",
            "color": "#6610f2",
            "strategies": [
                {
                    "name": "Solar Heat Gain",
                    "image": "images/solar_heat_gain.png",
                    "description": "Maximize south-facing glazing to capture solar heat. Use thermal storage walls or floors to store and redistribute heat."
                },
                {
                    "name": "Insulation",
                    "image": "images/insulation.png",
                    "description": "High levels of insulation in walls, roof, and foundation minimize heat loss and reduce heating demands significantly."
                },
                {
                    "name": "Windbreaks",
                    "image": "images/windbreaks.png",
                    "description": "Strategic placement of vegetation or structures on north and west sides reduce cold wind impact and heat loss."
                }
            ]
        },
        "Cold Dry": {
            "title": "Cold",
            "color": "#0d6efd",
            "strategies": [
                {
                    "name": "Compact Design",
                    "image": "images/compact_design.png",
                    "description": "Minimize surface area to volume ratio to reduce heat loss. Compact, clustered designs with minimal exposed surfaces work best."
                },
                {
                    "name": "Vestibules & Airlocks",
                    "image": "images/vestibules_airlocks.png",
                    "description": "Entry vestibules create buffer zones that prevent direct cold air infiltration and reduce heat loss through doorways."
                },
                {
                    "name": "Super Insulation",
                    "image": "images/super_insulation.png",
                    "description": "Extra-thick insulation (R-40+ walls, R-60+ roof) combined with triple-glazed windows minimizes heat loss in extreme cold."
                }
            ]
        },
        "Cool Marine": {
            "title": "Marine",
            "color": "#20c997",
            "strategies": [
                {
                    "name": "Moisture Protection",
                    "image": "images/moisture_protection.png",
                    "description": "Advanced water-resistant barriers and proper flashing details protect against persistent moisture and salt spray in marine climates."
                },
                {
                    "name": "Moderate Insulation",
                    "image": "images/moderate_insulation.png",
                    "description": "Balanced insulation addresses mild winters and cool summers while managing high humidity levels typical of marine climates."
                },
                {
                    "name": "Daylighting",
                    "image": "images/daylighting.png",
                    "description": "Maximize natural light through windows and skylights to compensate for frequently overcast conditions in marine climates."
                }
            ]
        }
    }
    
    
    # Match zone name to strategy (flexible matching)
    zone_name_lower = zone_name.lower().strip()
    
    for key in strategies.keys():
        key_lower = key.lower().strip()
        if key_lower == zone_name_lower or key_lower in zone_name_lower or zone_name_lower in key_lower:
            return strategies[key]
    
    # Default return if no match
    return None

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
    # st.markdown("<br><br>", unsafe_allow_html=True)
    # st.markdown(f'<div style="text-align: center;"><p style="font-size: 56px; font-weight: 300; color: #dc3545; margin: 20px 0;">{climate_zone}</p></div>', unsafe_allow_html=True)
    
    # # Display detailed information
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # col_report_left, col_report_center, col_report_right = st.columns([1, 2, 1])
    # with col_report_center:
    #     st.markdown(f"""
    #         <div style="background-color: #f8f9fa; padding: 30px; border-radius: 10px; border-left: 5px solid #ff6b35;">
    #             <h3 style="color: #333; margin-bottom: 20px;">Climate Zone Details</h3>
    #             <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Country:</strong> {selected_country}</p>
    #             <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Location:</strong> {selected_location}</p>
    #             <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Climate Zone (by ASHRAE Standard 169):</strong> <span style="color: #dc3545; font-weight: bold;">{climate_zone}</span></p>
    #             <p style="font-size: 18px; color: #666; margin-bottom: 10px;"><strong>Climate Zone Name:</strong> {climate_zone_name}</p>
    #         </div>
    #     """, unsafe_allow_html=True)
    
    # Get and display passive design strategies
    strategies_data = get_climate_strategies(climate_zone_name)
    
    
    if strategies_data:
        # st.markdown("<br><br>", unsafe_allow_html=True)
        # st.markdown(f"""
        #     <div style="text-align: center;">
        # st.markdown(f"""<h2 style="color: {strategies_data['color']}; font-size: 36px; margin-bottom: 10px;">{strategies_data['title']}"""</h2>)
        #         <p style="color: #666; font-size: 18px; margin-bottom: 40px;">Passive Design Strategies</p>
        #     </div>
        # """, unsafe_allow_html=True)
        
        # Display strategies in a horizontal three-column layout
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for idx, strategy in enumerate(strategies_data['strategies']):
            with cols[idx]:
                # Strategy title
                st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 15px;">
                        <h3 style="color: #333; font-size: 20px; font-weight: 600;">{strategy['name']}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # Try to load actual image if image key exists
                if 'image' in strategy:
                    try:
                        st.image(strategy['image'], use_container_width=True)
                    except Exception as e:
                        # Image placeholder if file doesn't exist
                        st.markdown(f"""
                            <div style="background-color: #f0f0f0; padding: 40px 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 2px dashed #ccc;">
                                <p style="color: #999; font-size: 14px; margin: 0;">📷 Image Placeholder</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    # No image specified
                    st.markdown("""
                        <div style="background-color: #f0f0f0; padding: 40px 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 2px dashed #ccc;">
                            <p style="color: #999; font-size: 14px; margin: 0;">📷 Image will be added</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Description below image
                st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {strategies_data['color']}; min-height: 150px;">
                        <p style="color: #555; font-size: 14px; line-height: 1.5; margin: 0; text-align: justify;">{strategy['description']}</p>
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