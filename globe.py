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

def amcharts_world_globe(df, lat_sel, lon_sel, location_name, climate_zone, climate_zone_name):

    import json

    # ----------------------------------------------------
    # Normalize zone values
    # ----------------------------------------------------
    df["Climate Zone"] = df["Climate Zone"].astype(str).str.strip()
    climate_zone = str(climate_zone).strip()

    # ----------------------------------------------------
    # Generate color map safely
    # ----------------------------------------------------
    zone_list = sorted(df["Climate Zone"].unique())

    # A long list of colors (expandable)
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#005f99", "#cc5500", "#009933", "#990000", "#663399",
        "#00b3b3", "#b30047", "#ff66b2", "#66ff66", "#ffd966"
    ]

    # Expand palette if needed
    while len(palette) < len(zone_list):
        palette = palette + palette

    zone_color_map = {z: palette[i] for i, z in enumerate(zone_list)}

    # Default fallback color
    default_color = "#444444"

    # ----------------------------------------------------
    # Build JS dataset
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # HTML/JS Rendering
    # ----------------------------------------------------
    html_code = f"""
    <style>
        #container {{
            display: flex;
            align-items: flex-start;
            gap: 20px;
        }}
        #chartdiv {{
            flex: 1;
            height: 600px;
        }}
        #legend {{
            width: 200px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }}
        #legend h4 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 16px;
            color: #333;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            margin-right: 10px;
            border-radius: 3px;
            border: 1px solid #ccc;
        }}
    </style>

    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>

    <div id="container">
        <div id="chartdiv"></div>
        <div id="legend">
            <h4>Climate Zone Colors</h4>
            {''.join([
                f'<div class="legend-item"><div class="legend-color" style="background:{zone_color_map.get(z, default_color)};"></div><span>{z}</span></div>'
                for z in zone_list
            ])}
        </div>
    </div>

    <script>
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

    }});
    </script>
    """

    st.components.v1.html(html_code, height=750, scrolling=False)

# -----------------------------
# Show Report
# -----------------------------
if report_clicked and not result.empty:

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🌍 Climate Zone on World Map")

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