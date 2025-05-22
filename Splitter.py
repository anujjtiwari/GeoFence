#code to generate a CSV with latitude and longitude column while splitting the LOCATION column to latitude and longitude 
import pandas as pd

# provide the local path here ---> 
df = pd.read_csv('/content/Bulk Barnala, Bimber.csv') 

# Spliting 'LOCATION' column into two new columns
df[['latitude', 'longitude']] = df['LOCATION'].str.split(',', expand=True)

# Converting to float to ensure they're in the correct format
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# Save to a new CSV file
df.to_csv('updated_with_lat_lon.csv', index=False)

print(" NEW CSV CREATED SUCCESSFULLY! ")
