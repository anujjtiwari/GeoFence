import pandas as pd
import folium
from IPython.display import display
from math import radians, sin, cos, sqrt, atan2

# Load the CSV with lat/lon and IP info
df = pd.read_csv('Bulk Barnala, Bimber.csv')

# Target point
target_lat = 32.86783735156178
target_lon = 74.25641198819648
radius_meters = 500
R = 6371000  # Earth radius in meters

# Haversine distance function
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))

# Extract lat/lon if needed
if 'latitude' not in df.columns or 'longitude' not in df.columns:
    df[['latitude', 'longitude']] = df['LOCATION'].str.split(',', expand=True).astype(float)

# Rename columns
df['TIME STAMP'] = pd.to_datetime(df['REQ. TIME'])
df['IP'] = df['IP ADDRESS']
df_sorted = df.sort_values(by=['IP', 'TIME STAMP'])

# Track IPs by behavior
inbound_ips, outbound_ips, stayed_in_ips = set(), set(), set()

for ip, group in df_sorted.groupby('IP'):
    previous_in = None
    in_any, out_any = False, False
    transition_in, transition_out = False, False

    for _, row in group.iterrows():
        dist = haversine_distance(target_lat, target_lon, row['latitude'], row['longitude'])
        inside = dist <= radius_meters

        if inside: in_any = True
        else: out_any = True

        if previous_in is not None:
            if not previous_in and inside:
                transition_in = True
            elif previous_in and not inside:
                transition_out = True
        previous_in = inside

    if transition_in: inbound_ips.add(ip)
    if transition_out: outbound_ips.add(ip)
    if in_any and not out_any: stayed_in_ips.add(ip)

# Prepare the map
mymap = folium.Map(location=[target_lat, target_lon], zoom_start=15)

# Add the 500m circle around the target
folium.Circle(
    location=[target_lat, target_lon],
    radius=radius_meters,
    color='red',
    fill=True,
    fill_opacity=0.2,
    popup='Target Area'
).add_to(mymap)

# Add target marker
folium.Marker(
    location=[target_lat, target_lon],
    popup='🎯 Target Location',
    icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')
).add_to(mymap)

# Plot IPs by behavior
def add_markers(ip_set, color, label):
    for ip in ip_set:
        rows = df_sorted[df_sorted['IP'] == ip]
        lat = rows.iloc[0]['latitude']
        lon = rows.iloc[0]['longitude']
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"{label}: {ip}"
        ).add_to(mymap)

# Add all IP types
add_markers(inbound_ips, 'blue', 'Inbound IP')
add_markers(outbound_ips, 'green', 'Outbound IP')
add_markers(stayed_in_ips, 'orange', 'Stayed-in IP')

# adding legend using custom HTML Tags
legend_html = '''
<div style="position: fixed; 
     bottom: 30px; left: 30px; width: 180px; height: 150px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     box-shadow: 2px 2px 5px rgba(0,0,0,0.4); padding: 10px;">
<b>🗺 Legend</b><br>
<i style="background:red; color:red;">⬤</i> Target Circle<br>
<i style="color:blue;">⬤</i> Inbound IP<br>
<i style="color:green;">⬤</i> Outbound IP<br>
<i style="color:orange;">⬤</i> Stayed-in IP<br>
</div>
'''
mymap.get_root().html.add_child(folium.Element(legend_html))

# Display inline
display(mymap)
