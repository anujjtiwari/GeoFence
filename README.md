# GeoFence
- This is a python script which takes telecom log files as an input and a target GPS coordinate
- Next it creates a 500 meter radius Geofence around the Target coordinate
- finally it produces it produces a xcel sheet which contains following IPs:
  - Inbound IPs:  ( ip which entered the circle during the time interval)
  - Outbound IPs ( Ips which left the circle during the interval)
  - Stayed-in IPs ( IPs which stayed during the whole interval within the radius)  
