import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# --- Re-run the previous logic to get the IP sets ---

# Load your CSV file
df = pd.read_csv('Bulk Barnala, Bimber.csv')

# Target coordinates and radius
target_lat = 32.86783735156178
target_lon = 74.25641198819648
radius_meters = 500

# Earth's radius in meters
R = 6371000

# Function to calculate Haversine distance in meters
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Check if 'latitude' and 'longitude' columns exist. If not, try to parse 'LOCATION'.
if 'latitude' not in df.columns or 'longitude' not in df.columns:
    if 'LOCATION' in df.columns:
        # Assuming LOCATION is in the format "latitude, longitude"
        df[['latitude', 'longitude']] = df['LOCATION'].str.split(',', expand=True).astype(float)
    else:
        print("Error: 'latitude', 'longitude', or 'LOCATION' column not found in the CSV.")
        exit()

# Rename 'REQ. TIME' to 'TIME STAMP' for consistency and easy access
if 'REQ. TIME' in df.columns:
    df['TIME STAMP'] = pd.to_datetime(df['REQ. TIME'])
else:
    print("Error: 'REQ. TIME' column not found in the CSV.")
    exit()

# Rename 'IP ADDRESS' to 'IP' for consistency and easy access
if 'IP ADDRESS' in df.columns:
    df['IP'] = df['IP ADDRESS']
else:
    print("Error: 'IP ADDRESS' column not found in the CSV.")
    exit()

# Sort by IP and TIME STAMP
df_sorted = df.sort_values(by=['IP', 'TIME STAMP'])

inbound_ips = set()
outbound_ips = set()
stayed_in_ips = set()

# Group by IP and process each device's movements
for ip, group in df_sorted.groupby('IP'):
    previous_in_circle = None
    in_circle_at_any_point = False
    out_circle_at_any_point = False
    transition_in_detected = False
    transition_out_detected = False

    for _, row in group.iterrows():
        current_lat = row['latitude']
        current_lon = row['longitude']

        distance = haversine_distance(target_lat, target_lon, current_lat, current_lon)
        current_in_circle = distance <= radius_meters

        if current_in_circle:
            in_circle_at_any_point = True
        else:
            out_circle_at_any_point = True

        if previous_in_circle is not None:
            if not previous_in_circle and current_in_circle:
                transition_in_detected = True
            elif previous_in_circle and not current_in_circle:
                transition_out_detected = True
        
        previous_in_circle = current_in_circle
    
    if transition_in_detected:
        inbound_ips.add(ip)
    
    if transition_out_detected:
        outbound_ips.add(ip)
    
    # A device 'stayed in' if all its recorded points were within the circle.
    if in_circle_at_any_point and not out_circle_at_any_point:
        stayed_in_ips.add(ip)

# --- End of IP sets generation ---

# Convert sets to lists for easier handling
inbound_list = list(inbound_ips)
outbound_list = list(outbound_ips)
stayed_in_list = list(stayed_in_ips)

# Determine the maximum length among the lists to pad shorter ones
max_len = max(len(inbound_list), len(outbound_list), len(stayed_in_list))

# Pad shorter lists with None to make them equal length
inbound_list.extend([None] * (max_len - len(inbound_list)))
outbound_list.extend([None] * (max_len - len(outbound_list)))
stayed_in_list.extend([None] * (max_len - len(stayed_in_list)))

# Create a dictionary for the DataFrame
data = {
    'Inbound IPs': inbound_list,
    'Outbound IPs': outbound_list,
    'Stayed-In IPs': stayed_in_list
}

# Create the DataFrame
df_ips = pd.DataFrame(data)

# Define the output Excel file name
output_excel_file = 'IP_Categorization.xlsx'

# Save the DataFrame to an Excel file
df_ips.to_excel(output_excel_file, index=False)

print(f"Excel file '{output_excel_file}' created successfully with categorized IP addresses.")
