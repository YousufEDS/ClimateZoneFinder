import streamlit as st
import pandas as pd
import json


st.set_page_config(
    page_title="Climate Zone Finder",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
    <style>
    /* Remove top padding/margin */
    .block-container {
        padding-top: 1.4rem !important;
        padding-bottom: 0rem !important;
    }
    
    .main-header {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #1f1f1f;
        margin-top: 0px;
        margin-bottom: 5px;
    }
    .header-line {
        width: 100px;
        height: 4px;
        background-color: #ff6b35;
        margin: 0 auto 20px auto;
    }
    .description {
        text-align: center;
        color: #666;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 20px;
        padding: 0 20px;
    }
    .label-text {
        font-size: 18px;
        color: #555;
        font-weight: 500;
        margin-bottom: 5px;
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


st.markdown('<div class="main-header">CLIMATE ZONE FINDER</div>', unsafe_allow_html=True)
st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="description">
    Identify the climate zone of any location across the world using ASHRAE Standard 169 or 
    explore Indian climate zones using ECBC (Energy Conservation Building Code) classification.
    </div>
""", unsafe_allow_html=True)


@st.cache_data
def load_ashrae_data():
    df = pd.read_excel("ASHRAE-ClimateZoneMapping.xlsx")
    return df


@st.cache_data
def load_ecbc_data():
    df = pd.read_excel("INDIA-WeatherMapping.xlsx")
    return df


# Function to get color for a climate zone (ASHRAE)
def get_ashrae_zone_color(df, climate_zone):
    df["Climate Zone"] = df["Climate Zone"].astype(str).str.strip()
    climate_zone = str(climate_zone).strip()
    
    zone_list = sorted(df["Climate Zone"].unique())
    
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#005f99", "#cc5500", "#009933", "#990000", "#663399",
        "#00b3b3", "#b30047", "#ff66b2", "#66ff66", "#ffd966"
    ]
    
    while len(palette) < len(zone_list):
        palette = palette + palette
    
    zone_color_map = {z: palette[i] for i, z in enumerate(zone_list)}
    return zone_color_map.get(climate_zone, "#444444")


# Function to get color for a climate zone (ECBC)
def get_ecbc_zone_color(climate_zone):
    climate_zone = str(climate_zone).strip()
    
    ecbc_colors = {
        "Cold": "#02a0c5",
        "Composite": "#dec45e",
        "Hot-Dry": "#c60102",
        "Temperate": "#f89cc9",
        "Warm-Humid": "#e59704",
    }
    
    return ecbc_colors.get(climate_zone, "#444444")


# Globe visualization for ASHRAE (World)
def amcharts_world_globe(df, lat_sel, lon_sel, location_name, climate_zone, climate_zone_name):
    # Normalize zone values
    df["Climate Zone"] = df["Climate Zone"].astype(str).str.strip()
    climate_zone = str(climate_zone).strip()

    # Generate color map and zone name mapping
    zone_list = sorted(df["Climate Zone"].unique())
    
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
    
    rotation_x = -float(lon_sel)
    rotation_y = -float(lat_sel)

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
            width: 200px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            max-height: 700px;
            overflow-y: auto;
        }}
      
        #legend::-webkit-scrollbar {{
            width: 5px;
        }}

        #legend::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}

        #legend::-webkit-scrollbar-thumb {{
            background: #ff6b35;
            border-radius: 10px;
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
            gap: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            font-size: 13px;
            padding: 8px 10px;
            background: white;
            border-radius: 5px;
            transition: all 0.2s;
            gap: 10px;
        }}
        .legend-item:hover {{
            transform: translateX(5px);
            background: #fff5f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid #ccc;
            flex-shrink: 0;
        }}
        .legend-text {{
            font-size: 12px;
            color: #333;
            line-height: 1.3;
        }}
    </style>

    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>

    <div id="container">
        <div id="chartdiv"></div>
        <div id="legend">
            <h4>Climate Zone Legend</h4>
            <div class="legend-grid">
                {''.join([
                    f'<div class="legend-item">'
                    f'<div class="legend-color" style="background:{zone_color_map.get(z, default_color)};"></div>'
                    f'<span class="legend-text">{z} - {zone_name_map.get(z, "")}</span>'
                    f'</div>'
                    for z in zone_list
                ])}
            </div>
        </div>
    </div>

    <script>
    (function() {{
        if (window.globeChart && window.globeRoot) {{
            var selectedData = [{selected_js}];
            window.selectedSeries.data.setAll(selectedData);
            
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

                window.globeRoot = root;
                window.globeChart = chart;
                window.selectedSeries = selectedSeries;

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


# India Map visualization for ECBC
def amcharts_india_map(df, lat_sel, lon_sel, location_name, state_name, climate_zone):
    # Normalize zone values
    df["Climate Zone"] = df["Climate Zone"].astype(str).str.strip()
    climate_zone = str(climate_zone).strip()

    # Get unique climate zones for ECBC
    zone_list = sorted(df["Climate Zone"].unique())
    
    # ECBC Climate Zone Colors
    ecbc_colors = {
        "Cold": "#02a0c5",
        "Composite": "#dec45e",
        "Hot-Dry": "#c60102",
        "Temperate": "#f89cc9",
        "Warm-Humid": "#e59704",
    }

    zone_color_map = {z: ecbc_colors.get(z, "#444444") for z in zone_list}
    default_color = "#444444"

    # Filter out rows with missing coordinates
    df_valid = df.dropna(subset=['Latitude', 'Longitude'])
    
    # Build JS dataset
    df_js = json.dumps([
        {
            "lat": float(row["Latitude"]),
            "lon": float(row["Longitude"]),
            "title": row["Location"],
            "state": row["State"],
            "zone": row["Climate Zone"],
            "color": zone_color_map.get(row["Climate Zone"], default_color)
        }
        for _, row in df_valid.iterrows()
    ])

    selected_js = json.dumps({
        "lat": float(lat_sel),
        "lon": float(lon_sel),
        "title": location_name,
        "state": state_name,
        "zone": climate_zone,
        "color": "#ff0000"
    })

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
        #legend-ecbc {{
            width: 220px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            max-height: 300px;
            overflow-y: auto;
        }}
        #legend-ecbc::-webkit-scrollbar {{
            width: 5px;
        }}
        #legend-ecbc::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        #legend-ecbc::-webkit-scrollbar-thumb {{
            background: #ff6b35;
            border-radius: 10px;
        }}
        #legend-ecbc h4 {{
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #333;
            font-weight: bold;
        }}
        .legend-grid {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            font-size: 13px;
            padding: 8px 10px;
            background: white;
            border-radius: 5px;
            transition: all 0.2s;
            gap: 10px;
        }}
        .legend-item:hover {{
            transform: translateX(5px);
            background: #fff5f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid #ccc;
            flex-shrink: 0;
        }}
        .legend-text {{
            font-size: 12px;
            color: #333;
            line-height: 1.3;
        }}
    </style>

    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/geodata/indiaLow.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>

    <div id="container">
        <div id="chartdiv"></div>
        <div id="legend-ecbc">
            <h4>ECBC Climate Zones</h4>
            <div class="legend-grid">
                {''.join([
                    f'<div class="legend-item">'
                    f'<div class="legend-color" style="background:{zone_color_map.get(z, default_color)};"></div>'
                    f'<span class="legend-text">{z}</span>'
                    f'</div>'
                    for z in zone_list
                ])}
            </div>
        </div>
    </div>

    <script>
    (function() {{
        if (window.indiaChart && window.indiaRoot) {{
            var selectedData = [{selected_js}];
            window.indiaSelectedSeries.data.setAll(selectedData);
            
            // Animate to the selected location
            window.indiaChart.animate({{
                key: "rotationX",
                to: 0,
                duration: 1000,
                easing: am5.ease.out(am5.ease.cubic)
            }});
        }} else {{
            am5.ready(function() {{
                var root = am5.Root.new("chartdiv");
                root.setThemes([ am5themes_Animated.new(root) ]);

                var chart = root.container.children.push(
                    am5map.MapChart.new(root, {{
                        projection: am5map.geoMercator(),
                        panX: "translateX",
                        panY: "translateY",
                        wheelY: "zoom"
                    }})
                );

                var polygonSeries = chart.series.push(
                    am5map.MapPolygonSeries.new(root, {{
                        geoJSON: am5geodata_indiaLow
                    }})
                );

                polygonSeries.mapPolygons.template.setAll({{
                    fill: am5.color("#e8f4ea"),
                    stroke: am5.color("#2d5f3f"),
                    strokeWidth: 1.5,
                    tooltipText: "{{name}}"
                }});

                polygonSeries.mapPolygons.template.states.create("hover", {{
                    fill: am5.color("#c7e6cc")
                }});

                var pointSeries = chart.series.push(am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }}));

                pointSeries.bullets.push(function(root, series, dataItem) {{
                    var circle = am5.Circle.new(root, {{
                        radius: 7,
                        fill: am5.color(dataItem.dataContext.color),
                        stroke: am5.color("#ffffff"),
                        strokeWidth: 2,
                        tooltipText:
                            "[bold]{{title}}[/]\\n" +
                            "State: {{state}}\\n" +
                            "Climate Zone: {{zone}}"
                    }});
                    
                    circle.states.create("hover", {{
                        scale: 1.3
                    }});
                    
                    return am5.Bullet.new(root, {{
                        sprite: circle
                    }});
                }});

                pointSeries.data.setAll({df_js});

                var selectedSeries = chart.series.push(am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }}));

                selectedSeries.bullets.push(function(root, series, dataItem) {{
                    var container = am5.Container.new(root, {{}});
                    
                    // Outer pulse circle
                    var outerCircle = container.children.push(am5.Circle.new(root, {{
                        radius: 20,
                        fill: am5.color("#ff0000"),
                        fillOpacity: 0.3,
                        strokeWidth: 0
                    }}));
                    
                    // Animate pulse
                    outerCircle.animate({{
                        key: "scale",
                        from: 1,
                        to: 1.5,
                        duration: 1000,
                        easing: am5.ease.out(am5.ease.cubic),
                        loops: Infinity
                    }});
                    
                    outerCircle.animate({{
                        key: "opacity",
                        from: 0.5,
                        to: 0,
                        duration: 1000,
                        easing: am5.ease.out(am5.ease.cubic),
                        loops: Infinity
                    }});
                    
                    // Main circle
                    var mainCircle = container.children.push(am5.Circle.new(root, {{
                        radius: 14,
                        fill: am5.color("#ff0000"),
                        stroke: am5.color("#ffffff"),
                        strokeWidth: 3,
                        tooltipText:
                            "[bold]{{title}}[/] (Selected)\\n" +
                            "State: {{state}}\\n" +
                            "Climate Zone: {{zone}}"
                    }}));
                    
                    return am5.Bullet.new(root, {{
                        sprite: container
                    }});
                }});

                selectedSeries.data.setAll([{selected_js}]);

                // Zoom to fit India
                chart.set("zoomLevel", 1);
                chart.set("zoomControl", am5map.ZoomControl.new(root, {{}}));

                window.indiaRoot = root;
                window.indiaChart = chart;
                window.indiaSelectedSeries = selectedSeries;
                window.indiaPointSeries = pointSeries;
            }});
        }}
    }})();
    </script>
    """

    st.components.v1.html(html_code, height=730, scrolling=False)


# Main Application Logic
standard_options = ["ASHRAE", "ECBC"]
select_standard = st.selectbox("Select Standard", standard_options, index=0, width=300)

# Two Column Layout
left_col, right_col = st.columns([1, 2.5])

# ASHRAE Standard
if select_standard == "ASHRAE":
    df = load_ashrae_data()
    
    with left_col:
        st.markdown('<div class="section-title">📍 Location Selection</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="label-text">Country</div>', unsafe_allow_html=True)
        countries = sorted(df["Country"].unique())
        selected_country = st.selectbox("Country", countries, key="country", label_visibility="collapsed", width=300)
        
        st.markdown('<div class="label-text">Location</div>', unsafe_allow_html=True)
        locations = sorted(df[df["Country"] == selected_country]["Location"].unique())
        selected_location = st.selectbox("Location", locations, key="location", label_visibility="collapsed", width=300)
        
        result = df[(df["Country"] == selected_country) & (df["Location"] == selected_location)]
        
        st.markdown('<div class="label-text">Climate Zone:</div>', unsafe_allow_html=True)
        if not result.empty:
            climate_zone = result.iloc[0]["Climate Zone"]
            zone_color = get_ashrae_zone_color(df, climate_zone)
            st.markdown(
                f'<p style="font-size: 28px; font-weight: bold; color: {zone_color}; margin: 10px 0;">{climate_zone}</p>',
                unsafe_allow_html=True,
            )
        else:
            climate_zone = None
            st.markdown('<p style="font-size: 28px; font-weight: bold; color: #dc3545; margin: 10px 0;">-</p>',
                        unsafe_allow_html=True)
        
        st.markdown('<div class="label-text">Climate Zone Name:</div>', unsafe_allow_html=True)
        if not result.empty:
            climate_zone_name = result.iloc[0]["Climate Zone Name"]
            zone_color = get_ashrae_zone_color(df, climate_zone)
            st.markdown(
                f'<p style="font-size: 18px; font-weight: 500; color: {zone_color}; margin: 10px 0;">{climate_zone_name}</p>',
                unsafe_allow_html=True,
            )
        else:
            climate_zone_name = None
            st.markdown('<p style="font-size: 18px; font-weight: 500; color: #dc3545; margin: 10px 0;">-</p>',
                        unsafe_allow_html=True)
        
        report_clicked = st.button("GENERATE REPORT", type="primary", use_container_width=False, width=300)
        if not result.empty and pd.notna(result.iloc[0].get("EPW File", None)):
            epw_url = result.iloc[0]["EPW File"]
            if epw_url and str(epw_url).strip() != "" and str(epw_url) != "0":
                st.link_button("📥 DOWNLOAD EPW", epw_url, type="secondary", use_container_width=False, width=300)
            else:
                st.button("📥 DOWNLOAD EPW", type="secondary", disabled=True, use_container_width=False, width=300)
        else:
            st.button("📥 DOWNLOAD EPW", type="secondary", disabled=True, use_container_width=False, width=300)
        
        if report_clicked and not result.empty:
            epw_file = result.iloc[0].get("EPW File", "Not Available")
            epw_status = "Available" if (epw_file and str(epw_file).strip() != "" and str(epw_file) != "0") else "Not Available"
            
            st.markdown(f"""
                <div class="report-card">
                    <div class="report-title">Climate Zone Report</div>
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

# ECBC Standard (India)
elif select_standard == "ECBC":
    df = load_ecbc_data()
    
    with left_col:
        st.markdown('<div class="section-title">📍 Location Selection (India)</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # country is fixed to India
        st.markdown('<div class="label-text">Country</div>', unsafe_allow_html=True)
        country = "India"
        selected_country = st.selectbox(country, [country], index=0, key="country_ecbc", label_visibility="collapsed", disabled=True, width=300)

        st.markdown('<div class="label-text">State</div>', unsafe_allow_html=True)
        states = sorted(df["State"].unique())

        default_state = "Delhi"        
        default_index = states.index(default_state) if default_state in states else 0

        selected_state = st.selectbox("State", default_state, key="state", label_visibility="collapsed", width=300)
        
        st.markdown('<div class="label-text">Location</div>', unsafe_allow_html=True)
        locations = sorted(df[df["State"] == selected_state]["Location"].unique())
        selected_location = st.selectbox("Location", locations, key="ecbc_location", label_visibility="collapsed", width=300)
        
        result = df[(df["State"] == selected_state) & (df["Location"] == selected_location)]
        
        st.markdown('<div class="label-text">Climate Zone:</div>', unsafe_allow_html=True)
        if not result.empty:
            climate_zone = result.iloc[0]["Climate Zone"]
            zone_color = get_ecbc_zone_color(climate_zone)
            st.markdown(
                f'<p style="font-size: 28px; font-weight: bold; color: {zone_color}; margin: 10px 0;">{climate_zone}</p>',
                unsafe_allow_html=True,
            )
        else:
            climate_zone = None
            st.markdown('<p style="font-size: 28px; font-weight: bold; color: #dc3545; margin: 10px 0;">-</p>',
                        unsafe_allow_html=True)
        
        report_clicked = st.button("GENERATE REPORT", type="primary", use_container_width=False, width=300)
        if not result.empty and pd.notna(result.iloc[0].get("EPW File", None)):
            epw_url = result.iloc[0]["EPW File"]
            if epw_url and str(epw_url).strip() != "" and str(epw_url) != "0":
                st.link_button("📥 DOWNLOAD EPW", epw_url, type="secondary", use_container_width=False, width=300)
            else:
                st.button("📥 DOWNLOAD EPW", type="secondary", disabled=True, use_container_width=False, width=300)
        else:
            st.button("📥 DOWNLOAD EPW", type="secondary", disabled=True, use_container_width=False, width=300)
        
        if report_clicked and not result.empty:
            epw_file = result.iloc[0].get("EPW File", "Not Available")
            epw_display = f'<a href="{epw_file}" target="_blank" style="color: white; text-decoration: underline;">Download EPW</a>' if (epw_file and str(epw_file).strip() != "" and str(epw_file) != "0") else "Not Available"
            
            st.markdown(f"""
                <div class="report-card">
                    <div class="report-title">ECBC Climate Zone Report</div>
                    <div class="report-item">
                        <div class="report-label">Location</div>
                        <div class="report-value">{selected_location}</div>
                    </div>
                    <div class="report-item">
                        <div class="report-label">State</div>
                        <div class="report-value">{selected_state}</div>
                    </div>
                    <div class="report-item">
                        <div class="report-label">Climate Zone</div>
                        <div class="report-value">{climate_zone}</div>
                    </div>
                    <div class="report-item">
                        <div class="report-label">EPW File</div>
                        <div class="report-value">{epw_display}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-title">India Climate Zone Map (ECBC)</div>', unsafe_allow_html=True)
        
        if not result.empty:
            lat_selected = result.iloc[0]["Latitude"]
            lon_selected = result.iloc[0]["Longitude"]
            
            # Check if coordinates are valid
            if pd.notna(lat_selected) and pd.notna(lon_selected):
                amcharts_india_map(
                    df,
                    lat_selected,
                    lon_selected,
                    selected_location,
                    selected_state,
                    climate_zone
                )
            else:
                st.warning(f"⚠️ Coordinates not available for {selected_location}. Please select a different location.")
        else:
            st.info("Please select a location to view on the map.")


# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#999; padding:20px;">
        Climate Zone Finder Dashboard | Data-driven Climate Analysis
    </div>
""", unsafe_allow_html=True)