#!/usr/local/bin/python

import csv
import datetime
import sys
import os

def run():
    str2dt = lambda x: datetime.time(*list(map(int, x.split(":"))))

    today = "{:%Y%m%d}".format(datetime.date.today())
    now = str2dt(datetime.datetime.now().strftime("%H:%M"))

    stops_txt = os.environ["HOME"] + "/google_transit/stops.txt"
    trips_txt = os.environ["HOME"] + "/google_transit/trips.txt"
    routes_txt = os.environ["HOME"] + "/google_transit/routes.txt"
    stop_times_txt = os.environ["HOME"] + "/google_transit/stop_times.txt"
    calendar_dates_txt = os.environ["HOME"] + "/google_transit/calendar_dates.txt"

    trip_ids = []
    service_ids = []
    trains = {}
    station_lookup = {}

    with open(calendar_dates_txt, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        next(csvreader)

        for row in csvreader:
            service_id = row[0]
            date = row[1]
            exception_type = int(row[2])

            if date == today:
                service_ids.append(service_id)

    if not service_ids:
        print(f"No service ids found for {today}.")
        sys.exit(1)

    with open(stops_txt, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        next(csvreader)

        for row in csvreader:
            stop_id = row[0]
            stop_name = row[1]

            station_lookup[stop_id] = stop_name

    with open(trips_txt, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        # Skip over the header of the csv file
        next(csvreader)

        for row in csvreader:
            route_id = int(row[0])
            service_id = row[1]
            direction_id = int(row[5])

            if route_id == 2 and direction_id == 0 and service_id in service_ids:
                # This is a train that is heading eastbound on the hempstead branch
                trip_ids.append(row[2])

    with open(stop_times_txt, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        # Skip over the header of the csv file
        next(csvreader)

        for row in csvreader:
            trip_id = row[0]
            arrival_time = row[1]
            departure_time = row[2]
            stop_id = int(row[3])
            stop_sequence = int(row[4])

            if stop_id == 8 and stop_sequence == 0 and trip_id in trip_ids:
                trains[trip_id] = {"depart": departure_time, "arrive": None}

            if stop_id == 38 and trip_id in trains:
                trains[trip_id]["arrive"] = arrival_time

    for train in sorted(trains):
        if trains[train]["arrive"] is None:
            continue

        departure_time = datetime.datetime.now()
        arrival_time = datetime.datetime.now()

        """
        For trips that cross midnight, the arrival and depature times are
        listed as 24:XX:XX. To convert this to standard military time subtract
        24 from the hour and pad it with a 0
        """
        arrival_hour = int(trains[train]["arrive"].split(":", 1)[0])
        if arrival_hour >= 24:
            normalized_arrival_hour = "{:02d}".format(arrival_hour - 24)
            trains[train]["arrive"] = trains[train]["arrive"].replace(
                "%s:" % (arrival_hour), "%s:" % (normalized_arrival_hour)
            )
            arrival_time = arrival_time + datetime.timedelta(days=1)

        depart = str2dt(trains[train]["depart"])
        arrive = str2dt(trains[train]["arrive"])

        departure_time = departure_time.replace(
            hour=depart.hour, minute=depart.minute, second=depart.second, microsecond=00
        )
        arrival_time = arrival_time.replace(
            hour=arrive.hour, minute=arrive.minute, second=arrive.second, microsecond=00
        )

        travel_time = arrival_time - departure_time

        hours, remainder = divmod(int(travel_time.total_seconds()), 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        travel_time = str2dt("%s:%s" % (hours, minutes))

        if depart > now:
            print(
                "{} -> {} ({}{})".format(
                    depart.strftime("%H:%M"),
                    arrive.strftime("%H:%M"),
                    travel_time.strftime("%H hour ") if travel_time.hour > 0 else "",
                    travel_time.strftime("%M minutes"),
                )
            )

if __name__ == '__main__':
    run()
    sys.exit(0)
