import streamlit as st
import pandas as pd

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(
    page_title="Climate Zone Finder",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
    <style>
    /* Remove top padding/margin */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    
    .main-header {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #1f1f1f;
        margin-top: 0px;
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
        margin-bottom: 8px;
    }
    .section-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 20px;
        border-bottom: 3px solid #ff6b35;
        padding-bottom: 10px;
        display: inline-block;
    }
    .report-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .report-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    .report-item {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    .report-label {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .report-value {
        font-size: 20px;
        font-weight: bold;
    }
    
    /* Adjust selectbox width */
    .stSelectbox > div > div {
        max-width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-header">CLIMATE ZONE FINDER</div>', unsafe_allow_html=True)
st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="description">
    Identify the climate zone of any location across the world using data from
    ASHRAE Standard 169. Select the country, pick the location, and view real-time updates on the globe.
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("US&InternationStations-ClimateZones.xlsx")
    st.write(f"Data loaded: {df.shape[0]} records.")
    # st.write(df[df['Country'] == 'Algeria (DZA)'])
    return df


df = load_data()

# st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Two Column Layout
# -----------------------------
left_col, right_col = st.columns([1, 2.5])

# -----------------------------
# LEFT SIDE - Input Form
# -----------------------------
with left_col:
    st.markdown('<div class="section-title">📍 Location Selection</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Country
    st.markdown('<div class="label-text">Country</div>', unsafe_allow_html=True)
    countries = sorted(df["Country"].unique())
    selected_country = st.selectbox("Country", countries, key="country", label_visibility="collapsed")
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # Location
    st.markdown('<div class="label-text">Location</div>', unsafe_allow_html=True)
    locations = sorted(df[df["Country"] == selected_country]["Location"].unique())
    selected_location = st.selectbox("Location", locations, key="location", label_visibility="collapsed")
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch Selected Row
    result = df[(df["Country"] == selected_country) & (df["Location"] == selected_location)]
    
    # Climate Zone
    st.markdown('<div class="label-text">Climate Zone:</div>', unsafe_allow_html=True)
    if not result.empty:
        climate_zone = result.iloc[0]["Climate Zone"]
        st.markdown(
            f'<p style="font-size: 28px; font-weight: bold; color: #dc3545; margin: 10px 0;">{climate_zone}</p>',
            unsafe_allow_html=True,
        )
    else:
        climate_zone = None
        st.markdown('<p style="font-size: 28px; font-weight: bold; color: #dc3545; margin: 10px 0;">-</p>',
                    unsafe_allow_html=True)
    
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # Climate Zone Name
    st.markdown('<div class="label-text">Climate Zone Name:</div>', unsafe_allow_html=True)
    if not result.empty:
        climate_zone_name = result.iloc[0]["Climate Zone Name"]
        st.markdown(
            f'<p style="font-size: 18px; font-weight: 500; color: #dc3545; margin: 10px 0;">{climate_zone_name}</p>',
            unsafe_allow_html=True,
        )
    else:
        climate_zone_name = None
        st.markdown('<p style="font-size: 18px; font-weight: 500; color: #dc3545; margin: 10px 0;">-</p>',
                    unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Report Button
    report_clicked = st.button("GENERATE REPORT", type="primary", use_container_width=True)
    
    # Show Report Card when button is clicked
    if report_clicked and not result.empty:
        st.markdown(f"""
            <div class="report-card">
                <div class="report-title">📋 Climate Zone Report</div>
                <div class="report-item">
                    <div class="report-label">Location</div>
                    <div class="report-value">{selected_location}</div>
                </div>
                <div class="report-item">
                    <div class="report-label">Country</div>
                    <div class="report-value">{selected_country}</div>
                </div>
                <div class="report-item">
                    <div class="report-label">Climate Zone</div>
                    <div class="report-value">{climate_zone}</div>
                </div>
                <div class="report-item">
                    <div class="report-label">Climate Zone Name</div>
                    <div class="report-value">{climate_zone_name}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------
# RIGHT SIDE - Globe Visualization
# -----------------------------
def amcharts_world_globe(df, lat_sel, lon_sel, location_name, climate_zone, climate_zone_name):
    import json

    # Normalize zone values
    df["Climate Zone"] = df["Climate Zone"].astype(str).str.strip()
    climate_zone = str(climate_zone).strip()

    # Generate color map and zone name mapping
    zone_list = sorted(df["Climate Zone"].unique())
    
    # Create a mapping of climate zones to their names
    zone_name_map = {}
    for zone in zone_list:
        zone_data = df[df["Climate Zone"] == zone].iloc[0]
        zone_name_map[zone] = zone_data["Climate Zone Name"]

    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#005f99", "#cc5500", "#009933", "#990000", "#663399",
        "#00b3b3", "#b30047", "#ff66b2", "#66ff66", "#ffd966"
    ]

    while len(palette) < len(zone_list):
        palette = palette + palette

    zone_color_map = {z: palette[i] for i, z in enumerate(zone_list)}
    default_color = "#444444"

    # Build JS dataset
    df_js = json.dumps([
        {
            "lat": float(row["Latitude"]),
            "lon": float(row["Longitude"]),
            "title": row["Location"],
            "country": row["Country"],
            "zone": row["Climate Zone"],
            "zone_name": row["Climate Zone Name"],
            "color": zone_color_map.get(row["Climate Zone"], default_color)
        }
        for _, row in df.iterrows()
    ])

    selected_js = json.dumps({
        "lat": float(lat_sel),
        "lon": float(lon_sel),
        "title": location_name,
        "zone": climate_zone,
        "zone_name": climate_zone_name,
        "color": "#ff0000"
    })
    
    # Calculate proper rotation values
    rotation_x = -float(lon_sel)
    rotation_y = -float(lat_sel)

    # HTML/JS Rendering with legend on the right side
    html_code = f"""
    <style>
        #container {{
            display: flex;
            flex-direction: row;
            height: 100%;
            gap: 20px;
        }}
        #chartdiv {{
            flex: 1;
            height: 700px;
            min-height: 700px;
        }}
        #legend {{
            width: 250px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            max-height: 700px;
            overflow-y: auto;
        }}
        #legend::-webkit-scrollbar {{
            width: 8px;
        }}
        #legend::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        #legend::-webkit-scrollbar-thumb {{
            background: #ff6b35;
            border-radius: 10px;
        }}
        #legend::-webkit-scrollbar-thumb:hover {{
            background: #e55a25;
        }}
        #legend h4 {{
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #333;
            font-weight: bold;
        }}
        .legend-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .legend-item {{
            display: flex;
            flex-direction: column;
            font-size: 13px;
            padding: 10px;
            background: white;
            border-radius: 5px;
            transition: transform 0.2s;
        }}
        .legend-item:hover {{
            transform: translateX(5px);
            background: #fff5f0;
        }}
        .legend-item-header {{
            display: flex;
            align-items: center;
            margin-bottom: 4px;
        }}
        .legend-zone-name {{
            font-size: 11px;
            color: #666;
            padding-left: 26px;
            font-style: italic;
        }}
        .legend-color {{
            width: 18px;
            height: 18px;
            margin-right: 8px;
            border-radius: 3px;
            border: 1px solid #ccc;
            flex-shrink: 0;
        }}
        .legend-zone {{
            font-weight: 600;
            color: #333;
        }}
    </style>

    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>

    <div id="container">
        <div id="chartdiv"></div>
        <div id="legend">
            <h4>🎨 Climate Zone Legend</h4>
            <div class="legend-grid">
                {''.join([
                    f'<div class="legend-item">'
                    f'<div class="legend-color" style="background:{zone_color_map.get(z, default_color)};"></div>'
                    f'<span class="legend-text"><span class="legend-zone">{z}</span> - {zone_name_map.get(z, "")}</span>'
                    f'</div>'
                    for z in zone_list
                ])}
            </div>
        </div>
    </div>

    <script>
    (function() {{
        // Check if globe already exists
        if (window.globeChart && window.globeRoot) {{
            // Update existing globe with animation
            var selectedData = [{selected_js}];
            window.selectedSeries.data.setAll(selectedData);
            
            // Animate to new location with corrected rotation values
            window.globeChart.animate({{
                key: "rotationX",
                to: {rotation_x},
                duration: 1500,
                easing: am5.ease.inOut(am5.ease.cubic)
            }});

            window.globeChart.animate({{
                key: "rotationY",
                to: {rotation_y},
                duration: 1500,
                easing: am5.ease.inOut(am5.ease.cubic)
            }});
        }} else {{
            // Create new globe
            am5.ready(function() {{
                var root = am5.Root.new("chartdiv");
                root.setThemes([ am5themes_Animated.new(root) ]);

                var chart = root.container.children.push(
                    am5map.MapChart.new(root, {{
                        projection: am5map.geoOrthographic(),
                        panX: "rotateX",
                        panY: "rotateY"
                    }})
                );

                var polygonSeries = chart.series.push(
                    am5map.MapPolygonSeries.new(root, {{
                        geoJSON: am5geodata_worldLow
                    }})
                );

                polygonSeries.mapPolygons.template.setAll({{
                    fill: am5.color("#f5f5dc"),
                    stroke: am5.color("#8b7355"),
                    strokeWidth: 0.5
                }});

                var pointSeries = chart.series.push(am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }}));

                pointSeries.bullets.push(function(root, series, dataItem) {{
                    return am5.Bullet.new(root, {{
                        sprite: am5.Circle.new(root, {{
                            radius: 5,
                            fill: am5.color(dataItem.dataContext.color),
                            stroke: am5.color("#ffffff"),
                            strokeWidth: 1.3,
                            tooltipText:
                                "[bold]{{title}}[/]\\n" +
                                "{{country}}\\n" +
                                "Zone: {{zone}}\\n" +
                                "{{zone_name}}"
                        }})
                    }});
                }});

                pointSeries.data.setAll({df_js});

                var selectedSeries = chart.series.push(am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }}));

                selectedSeries.bullets.push(function(root, series, dataItem) {{
                    return am5.Bullet.new(root, {{
                        sprite: am5.Circle.new(root, {{
                            radius: 10,
                            fill: am5.color("#ff0000"),
                            stroke: am5.color("#ffffff"),
                            strokeWidth: 2,
                            tooltipText:
                                "[bold]{{title}}[/] (Selected)\\n" +
                                "Zone: {{zone}}\\n" +
                                "{{zone_name}}"
                        }})
                    }});
                }});

                selectedSeries.data.setAll([{selected_js}]);

                // Store references globally
                window.globeRoot = root;
                window.globeChart = chart;
                window.selectedSeries = selectedSeries;

                // Initial animation to selected location with corrected rotation values
                chart.animate({{
                    key: "rotationX",
                    to: {rotation_x},
                    duration: 2000,
                    easing: am5.ease.inOut(am5.ease.cubic)
                }});

                chart.animate({{
                    key: "rotationY",
                    to: {rotation_y},
                    duration: 2000,
                    easing: am5.ease.inOut(am5.ease.cubic)
                }});
            }});
        }}
    }})();
    </script>
    """

    st.components.v1.html(html_code, height=730, scrolling=False)

# Display globe in real-time (always visible)
with right_col:
    st.markdown('<div class="section-title">🌍 World Climate Zone Map</div>', unsafe_allow_html=True)
    
    if not result.empty:
        lat_selected = result.iloc[0]["Latitude"]
        lon_selected = result.iloc[0]["Longitude"]
        
        amcharts_world_globe(
            df,
            lat_selected,
            lon_selected,
            selected_location,
            climate_zone,
            climate_zone_name
        )
    else:
        st.info("Please select a location to view on the globe.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#999; padding:20px;">
        Climate Zone Finder Dashboard | Data-driven Climate Analysis
    </div>
""", unsafe_allow_html=True)