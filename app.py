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
    ASHRAE Standard 169. Select the country, pick the location, and click 'REPORT'.
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("US&InternationStations-ClimateZones.xlsx")

df = load_data()

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Input Form
# -----------------------------
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

    # Fetch Selected Row
    result = df[(df["Country"] == selected_country) & (df["Location"] == selected_location)]

    # Climate Zone
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

    # Report Button
    r5_label, r5_input = st.columns([1, 2.5])
    with r5_label:
        st.markdown('<div class="label-text">Click to generate report</div>', unsafe_allow_html=True)
    with r5_input:
        report_clicked = st.button("REPORT", type="primary")

def amcharts_world_map(df, lat_sel, lon_sel, location_name, climate_zone):

    import json

    # Color palette for climate zones
    zone_color_palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
        "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
        "#bcbd22", "#17becf"
    ]

    climate_zones = sorted(df["Climate Zone"].unique())
    zone_colors = {
        zone: zone_color_palette[i % len(zone_color_palette)]
        for i, zone in enumerate(climate_zones)
    }

    # Tooltip-enabled dataset
    df_js = json.dumps([
        {
            "lat": float(row["Latitude"]),
            "lon": float(row["Longitude"]),
            "title": row["Location"],
            "country": row["Country"],
            "zone": row["Climate Zone"],
            "color": zone_colors[row["Climate Zone"]],
            "tooltip": (
                f"{row['Location']} ({row['Country']})\n"
                f"Climate Zone: {row['Climate Zone']}\n"
                f"Lat: {row['Latitude']}, Lon: {row['Longitude']}"
            )
        }
        for row in df.to_dict(orient="records")
    ])

    # Legend dataset (unique zones)
    legend_js = json.dumps([
        {
            "zone": zone,
            "color": zone_colors[zone]
        }
        for zone in climate_zones
    ])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            #chartdiv {{
                width: 100%;
                height: 600px;
                position: relative;
            }}

            /* Legend Styling */
            .legend {{
                position: absolute;
                top: 20px;
                right: 20px;
                background: white;
                padding: 12px 15px;
                border-radius: 8px;
                box-shadow: 0 0 12px rgba(0,0,0,0.15);
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
            .legend-title {{
                font-weight: bold;
                margin-bottom: 8px;
                text-align: center;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                margin-bottom: 6px;
            }}
            .legend-color {{
                width: 14px;
                height: 14px;
                border-radius: 50%;
                margin-right: 8px;
            }}
        </style>

        <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
        <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
        <script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
        <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
    </head>

    <body>
        <div id="chartdiv"></div>

        <!-- LEGEND HTML -->
        <div class="legend" id="legend-box">
            <div class="legend-title">Climate Zones</div>
        </div>

        <script>
        am5.ready(function() {{

            var root = am5.Root.new("chartdiv");
            root.setThemes([ am5themes_Animated.new(root) ]);

            var chart = root.container.children.push(
                am5map.MapChart.new(root, {{
                    panX: "translateX",
                    panY: "translateY",
                    projection: am5map.geoMercator()
                }})
            );

            var polygonSeries = chart.series.push(
                am5map.MapPolygonSeries.new(root, {{
                    geoJSON: am5geodata_worldLow
                }})
            );

            // ===============================
            // ALL POINTS (with tooltips)
            // ===============================
            var allPoints = chart.series.push(
                am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }})
            );

            allPoints.bullets.push(function(root, series, dataItem) {{
                return am5.Bullet.new(root, {{
                    sprite: am5.Circle.new(root, {{
                        radius: 5,
                        tooltipText: dataItem.dataContext.tooltip,
                        fill: am5.Color.fromString(dataItem.dataContext.color),
                        stroke: am5.color(0xffffff),
                        strokeWidth: 1
                    }})
                }});
            }});

            allPoints.data.setAll({df_js});

            // ===============================
            // SELECTED POINT (highlight)
            // ===============================
            var selectedPoint = chart.series.push(
                am5map.MapPointSeries.new(root, {{
                    latitudeField: "lat",
                    longitudeField: "lon"
                }})
            );

            selectedPoint.bullets.push(function(root, series, dataItem) {{
                return am5.Bullet.new(root, {{
                    sprite: am5.Circle.new(root, {{
                        radius: 10,
                        fill: am5.color(0xff0000),
                        stroke: am5.color(0xffffff),
                        strokeWidth: 2,
                        tooltipText:
                            "{location_name} (Selected)\\n" +
                            "Climate Zone: {climate_zone}\\n" +
                            "Lat: {lat_sel}, Lon: {lon_sel}"
                    }})
                }});
            }});

            selectedPoint.data.setAll([{{
                lat: {lat_sel},
                lon: {lon_sel}
            }}]);

            // ===============================
            // BUILD LEGEND
            // ===============================
            var legendData = {legend_js};
            var legendBox = document.getElementById("legend-box");

            legendData.forEach(function(item) {{
                var row = document.createElement("div");
                row.className = "legend-item";
                row.innerHTML = `
                    <div class="legend-color" style="background:${{item.color}}"></div>
                    <div>${{item.zone}}</div>
                `;
                legendBox.appendChild(row);
            }});

        }});
        </script>
    </body>
    </html>
    """

    st.components.v1.html(html_code, height=650, scrolling=False)

# -----------------------------
# Show Report
# -----------------------------
if report_clicked and not result.empty:

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🌍 Climate Zone on World Map")

    lat_selected = result.iloc[0]["Latitude"]
    lon_selected = result.iloc[0]["Longitude"]

    # # Replace Plotly with amCharts map
    # amcharts_world_map(
    #     lat_selected,
    #     lon_selected,
    #     selected_location,
    #     climate_zone
    # )
    amcharts_world_map(
    df,
    lat_selected,
    lon_selected,
    selected_location,
    climate_zone
    )


# -----------------------------
# Footer
# -----------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#999; padding:20px;">
        Climate Zone Finder Dashboard | Data-driven Climate Analysis
    </div>
""", unsafe_allow_html=True)
