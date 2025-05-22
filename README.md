# GeoFence
- This is a python script which takes telecom log files as an input and a target GPS coordinate
- Next it creates a 500 meter radius around the Target coordinate
- finally it produces a xcel sheet which contains following IPs:
  - Inbound IPs:  ( ip which entered the circle during the time interval)
  - Outbound IPs ( Ips which left the circle during the interval)
  - Stayed-in IPs ( IPs which stayed during the whole interval within the radius)  


How to use: 
- some sample .CSV files are provided in the "Logs" Folder simply import them in your code
- use the Splitter.py to split the "LOCATION" column into latitude and longitude and create a new CSV file with these columns it will ease out further processing.
- Now use GeoFencer.py and add the path of the newly created CSV and the simply run the program, it will create a XCEL sheet for you.
- (Optional step): You can use the GeoFenceMapper.py to visualize the the cordinates on the World Map ( Folium required ). 
