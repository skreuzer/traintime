# traintime
LIRR Train Schedules

# GTFS specification
https://developers.google.com/transit/gtfs/reference/

## routes.txt
### route_id
Contains an ID that uniquely identifies a route.

Frequently used routes:

|id|line|
|-|-|
|1|Babylon|
|2|Hempstead|
|6|Long Beach|
|10|Port Jefferson|

### route_short_name
Contains the short name of a route.

### route_long_name
Contains the full name of a route.

### route_type
Describes the type of transportation used on a route.

Valid values for this field are:

|id|value|
|-|-|
|0|Tram, Streetcar, Light rail|
|1|Subway|
|2|Rail|
|3|Bus|
|4|Ferry|
|5|Cable car|
|6|Gondola, Suspended cable car|
|7|Funicular|

### route_color
In systems that have colors assigned to routes, this defines a color that corresponds to a route.

### route_text_color
Specifies a legible color to use for text drawn against a background of route_color.

## trips.txt
### route_id
Contains an ID that uniquely identifies a route. This value is referenced from the routes.txt file.

### service_id
Contains an ID that uniquely identifies a set of dates when service is available for one or more routes.

### trip_id
Contains an ID that identifies a trip. The trip_id is dataset unique.

### trip_headsign
Contains the text that appears on a sign that identifies the trip's destination to passengers.

### trip_short_name
Contains the text that appears in schedules and sign boards to identify the trip to passengers.

### direction_id
Contains a binary value that indicates the direction of travel for a trip.

Valid values for this field are:

|id|direction|
|-|-|
|0|Points East (outbound travel)|
|1|Points West (inbound travel)|

### shape_id
Contains an ID that defines a shape for the trip. This value is referenced from the shapes.txt file.

## stop_times.txt
### trip_id
Contains an ID that identifies a trip. This value is referenced from the trips.txt file.

### arrival_time
Specifies the arrival time at a specific stop for a specific trip on a route.

### departure_time
Specifies the departure time from a specific stop for a specific trip on a route.

### stop_id
Contains an ID that uniquely identifies a stop. The stop_id is referenced from the stops.txt file.

Frequently used stations:
|id|station|
|---|---|
|8|Penn Station|
|12|Atlantic Terminal|
|15|Jamaica|
|38|Country Life Press|
|42|Mineola|
|102|East Rockaway|
|106|Rockville Centre|

### stop_sequence
Identifies the order of the stops for a particular trip.