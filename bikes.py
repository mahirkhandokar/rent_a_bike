"""CSC108/A08: Fall 2020 -- Assignment 2: Rent-a-bike

This code is provided solely for the personal and private use of
students taking the CSC108 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.

"""

import copy
import math
from typing import List, TextIO

from constants import (ID, NAME, LATITUDE, LONGITUDE, CAPACITY,
                       BIKES_AVAILABLE, DOCKS_AVAILABLE, IS_RENTING,
                       IS_RETURNING, NO_KIOSK_LABEL, EARTH_RADIUS,
                       SOUTH, NORTH, EAST, WEST, DIRECTIONS)


'''For simplicity, we'll use "Station" in our type contracts to
indicate that we mean a list containing station data.

You can read "Station" in a type contract as:
List of: int, str, float, float, int, int, int, bool, bool

where the values at each index represent the station data as described
in the handout.
'''

# Sample data for use in docstring examples
SAMPLE_STATIONS = [
    [7090, 'Danforth Ave / Lamb Ave',
     43.681991, -79.329455, 15, 4, 10, True, True],
    [7486, 'Gerrard St E / Ted Reeve Dr',
     43.684261, -79.299332, 22, 5, 17, False, False],
    [7571, 'Highfield Rd / Gerrard St E - SMART',
     43.671685, -79.325176, 19, 14, 5, True, True]]
HANDOUT_STATIONS = [
    [7000, 'Ft. York / Capreol Crt.',
     43.639832, -79.395954, 31, 20, 11, True, True],
    [7001, 'Lower Jarvis St / The Esplanade',
     43.647992, -79.370907, 15, 5, 10, True, True]]
FAKE_STATIONS = [
    [1000, 'Street Ave / Road Ave',
     43.0, -79.3, 20, 0, 20, True, True],
    [1001, 'Street Ave / Road Ave',
     43.0, -79.4, 20, 20, 0, True, True],
    [1002, 'Street Ave / Road Ave - SMART',
     43.1, -79.3, 20, 20, 0, True, True],
    [1003, 'Street Ave / Road Ave',
     42.9, -79.3, 20, 10, 10, True, True]]

# Used in docstring examples to avoid using == with floats.
EPSILON = 0.01

#################### BEGIN HELPER FUNCTIONS ####################


def is_number(value: str) -> bool:
    """Return True if and only if value represents a decimal number.

    >>> is_number('csca108')
    False
    >>> is_number('  098 ')
    True
    >>> is_number('+3.14159')
    True

    """

    return value.strip().lstrip('-+').replace('.', '', 1).isnumeric()


def get_distance(lat1: float, lon1: float,
                 lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined
    by (lat1, lon1) and (lat2, lon2), rounded to the nearest metre.

    >>> answer = get_distance(43.659777, -79.397383, 43.657129, -79.399439)
    >>> abs(answer - 0.338) < EPSILON
    True
    >>> answer = get_distance(43.67, -79.37, 55.15, -118.8)
    >>> abs(answer - 3072.872) < EPSILON
    True

    """

    # This function uses the haversine function to find the distance
    # between two locations. You do NOT need to understand why it
    # works.  You will just need to call on the function and work with
    # what it returns.  Based on code at goo.gl/JrPG4j
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))
    lon_diff, lat_diff = lon2 - lon1, lat2 - lat1

    a_value = (math.sin(lat_diff / 2) ** 2 +
               math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c_value = 2 * math.asin(math.sqrt(a_value))

    return round(c_value * EARTH_RADIUS, 3)


# It isn't necessary to call this function to implement your bikes.py
# functions, but you can use it to create larger lists for testing.
# See the main block below for an example of how to do that.
def csv_to_list(csv_file: TextIO) -> List[List[str]]:
    """Return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of
    csv_file.

    Docstring examples not given since results depend on data to be
    input.

    """

    csv_file.readline()  # read and discard header

    data = []
    for line in csv_file:
        data.append(line.strip().split(','))
    return data

#################### END HELPER FUNCTIONS ####################


# Note: you will most certainly need more examples to test your
# functions!

def clean_data(data: List[List[str]]) -> None:
    """Replace each string in all sublists of data as follows: replace
    with
    - an int iff it represents a whole number,
    - a float iff it represents a number that is not a whole number,
    - True iff it is 'True' (case-insensitive),
    - False iff it is 'False' (case-insensitive),
    - None iff it is 'null' or the empty string.

    >>> data = [['abc', '123', '45.6', 'true', 'False']]
    >>> clean_data(data)
    >>> data
    [['abc', 123, 45.6, True, False]]
    >>> data = [['ab2'], ['-123'], ['FALSE', '3.2'], ['3.0', '+4', '-5.0']]
    >>> clean_data(data)
    >>> data
    [['ab2'], [-123], [False, 3.2], [3, 4, -5]]
    >>> data = [['null', '', 'FaLse', 'tRUe']]
    >>> clean_data(data)
    >>> data
    [[None, None, False, True]]

    """

    i = 0

    while i < len(data):
        for j in range(len(data[i])):
            if is_number(data[i][j]):
                data[i][j] = convert_to_num(data[i][j])
            elif data[i][j].lower() == 'true' or data[i][j].lower() == 'false':
                # If the current object is equal to a string form of true the
                # True will be assigned otherwise False will be assigned as the
                # string will be some form of false.
                data[i][j] = data[i][j].lower() == 'true'
            elif data[i][j] == 'null' or data[i][j] == '':
                data[i][j] = None
        i += 1


def convert_to_num(num: str) -> object:
    """Return the string num, as a float if it is not a whole number when
    converted to a float, or as an integer if it is a whole number when
    converted to a float.

    >>> convert_to_num('5.0')
    5
    >>> convert_to_num('2.3')
    2.3

    """

    if float(num) % 1 != 0:
        num = float(num)
    else:
        num = int(float(num))
    return num


def has_kiosk(station: 'Station') -> bool:
    """Return True if and only if the given station has a kiosk.

    >>> has_kiosk(SAMPLE_STATIONS[0])
    True
    >>> has_kiosk(SAMPLE_STATIONS[2])
    False

    """

    # Have to iterate through the list as 'SMART' is not an item itself.
    for info in station:
        if NO_KIOSK_LABEL in str(info):
            return False
    return True


def get_station_info(station_id: int, stations: List['Station']) -> list:
    """Return a list containing the following information from stations
    about the station with id number station_id:
        - station name (str)
        - number of bikes available (int)
        - number of docks available (int)
        - whether or not the station has a kiosk (bool)
    (in this order)
    If station_id is not in stations, return an empty list.

    Precondition: stations has at most one station with id station_id.

    >>> get_station_info(7090, SAMPLE_STATIONS)
    ['Danforth Ave / Lamb Ave', 4, 10, True]
    >>> get_station_info(7571, SAMPLE_STATIONS)
    ['Highfield Rd / Gerrard St E - SMART', 14, 5, False]

    """

    station_info = []
    valid_station = get_station(station_id, stations)

    station_info.append(valid_station[NAME])
    station_info.append(valid_station[BIKES_AVAILABLE])
    station_info.append(valid_station[DOCKS_AVAILABLE])
    station_info.append(has_kiosk(valid_station))
    return station_info


def get_total(index: int, stations: List['Station']) -> int:
    """Return the sum of the column in stations given by index. Return 0
    if stations is empty.

    Preconditions: index is a valid index into each station in stations.
                   The items in stations at the position that index
                    refers to are ints.

    >>> get_total(BIKES_AVAILABLE, SAMPLE_STATIONS)
    23
    >>> get_total(DOCKS_AVAILABLE, SAMPLE_STATIONS)
    32

    """

    total_available = 0

    for station in stations:
        total_available = total_available + station[index]
    return total_available


def get_station_with_max_bikes(stations: List['Station']) -> int:
    """Return the station id of the station that has the most bikes
    available.  If there is a tie for the most available, return the
    station id that appears first in stations.

    Preconditions: len(stations) > 0

    >>> get_station_with_max_bikes(SAMPLE_STATIONS)
    7571
    >>> get_station_with_max_bikes(HANDOUT_STATIONS)
    7000

    """

    max_bikes = 0
    station_id = 0

    for station in stations:
        if station[BIKES_AVAILABLE] > max_bikes:
            station_id = station[ID]
            max_bikes = station[BIKES_AVAILABLE]
    return station_id


def get_stations_with_n_docks(num: int, stations: List['Station']) -> List[int]:
    """Return a list containing the station ids for the stations in
    stations that have at least num docks available, in the same order
    as they appear in stations.

    Precondition: num >= 0

    >>> get_stations_with_n_docks(2, SAMPLE_STATIONS)
    [7090, 7486, 7571]
    >>> get_stations_with_n_docks(12, SAMPLE_STATIONS)
    [7486]

    """

    stations_with_enough_docks = []

    for station in stations:
        if station[DOCKS_AVAILABLE] >= num:
            stations_with_enough_docks.append(station[ID])
    return stations_with_enough_docks


def get_direction(start_id: int, end_id: int, stations: List['Station']) -> str:
    """Return the direction to travel to get from station start_id to
    station end_id according to data in stations. Possible directions
    are defined by DIRECTIONS.

    Preconditions: start_id and end_id appears in stations.
                   start_id and end_id are ids of stations at different
                   locations.

    >>> get_direction(7486, 7090, SAMPLE_STATIONS)
    'SOUTHWEST'
    >>> get_direction(1000, 1002, FAKE_STATIONS)
    'NORTH'

    """

    direction = ''
    valid_start_station = get_station(start_id, stations)
    valid_end_station = get_station(end_id, stations)
    start_lat = valid_start_station[LATITUDE]
    start_lon = valid_start_station[LONGITUDE]
    end_lat = valid_end_station[LATITUDE]
    end_lon = valid_end_station[LONGITUDE]

    if start_lat - end_lat < 0:
        direction = NORTH
    elif start_lat - end_lat > 0:
        direction = SOUTH

    if start_lon - end_lon < 0:
        direction = direction + EAST
    elif start_lon - end_lon > 0:
        direction = direction + WEST
    return direction


def get_nearest_station(lat: float, lon: float, with_kiosk: bool,
                        stations: List['Station']) -> int:
    """Return the id of the station from stations that is nearest to the
    location given by lat and lon.  If with_kiosk is True, return the
    id of the closest station with a kiosk.

    In the case of a tie, return the ID of the first station in
    stations with that distance.

    Preconditions: len(stations) > 1

    If with_kiosk, then there is at least one station in stations with a kiosk.

    >>> get_nearest_station(43.671134, -79.325164, False, SAMPLE_STATIONS)
    7571
    >>> get_nearest_station(43.674312, -79.299221, True, SAMPLE_STATIONS)
    7486

    """

    distances = []
    closest_station = 0
    distance = 0

    for station in stations:
        distance = get_distance(lat, lon, station[LATITUDE],
                                station[LONGITUDE])
        if with_kiosk and has_kiosk(station):
            distances.append(distance)
            # If the current distance is the smallest among the ones we have
            # then it is the closest station as of this moment.
            if distance == min(distances):
                closest_station = station[ID]
        elif not with_kiosk:
            distances.append(distance)
            if distance == min(distances):
                closest_station = station[ID]
    return closest_station


def rent_bike(station_id: int, stations: List['Station']) -> bool:
    """Update the available bike count and the docks available count for
    the station in stations with id station_id as if a single bike was
    removed, leaving an additional dock available. Return True if and
    only if the rental was successful, i.e. there was at least one
    bike available and the station is renting.

    Precondition: station_id appears in stations.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> rent_bike(7090, stations)
    True
    >>> stations[0][BIKES_AVAILABLE]
    3
    >>> stations[0][DOCKS_AVAILABLE]
    11
    >>> rent_bike(7486, stations)
    False
    >>> stations[1][BIKES_AVAILABLE]
    5
    >>> stations[1][DOCKS_AVAILABLE]
    17

    """

    station = get_station(station_id, stations)

    if station[IS_RENTING] and station[BIKES_AVAILABLE] >= 1:
        station[BIKES_AVAILABLE] = station[BIKES_AVAILABLE] - 1
        station[DOCKS_AVAILABLE] = station[DOCKS_AVAILABLE] + 1
        return True
    return False


def return_bike(station_id: int, stations: List['Station']) -> bool:
    """Update the available bike count and the docks available count for
    station in stations with id station_id as if a single bike was
    added, making an additional dock unavailable. Return True if and
    only if the return was successful, i.e. there was at least one
    dock available and the station is allowing returns.

    Precondition: station_id appears in stations.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> return_bike(7090, stations)
    True
    >>> stations[0][BIKES_AVAILABLE]
    5
    >>> stations[0][DOCKS_AVAILABLE]
    9
    >>> return_bike(7486, stations)
    False
    >>> stations[1][BIKES_AVAILABLE]
    5
    >>> stations[1][DOCKS_AVAILABLE]
    17

    """

    station = get_station(station_id, stations)

    if station[IS_RETURNING] and station[DOCKS_AVAILABLE] >= 1:
        station[BIKES_AVAILABLE] = station[BIKES_AVAILABLE] + 1
        station[DOCKS_AVAILABLE] = station[DOCKS_AVAILABLE] - 1
        return True
    return False


def balance_all_bikes(stations: List['Station']) -> int:
    """Return the difference between the number of bikes rented and the
    number of bikes returned as a result of the following balancing:

    Calculate the percentage of bikes available across all stations
    and evenly distribute the bikes so that each station has as close
    to the overall percentage of bikes available as possible. Remove a
    bike from a station if and only if the station is renting and
    there is a bike available to rent, and return a bike if and only
    if the station is allowing returns and there is a dock available.

    >>> stations = copy.deepcopy(SAMPLE_STATIONS)
    >>> balance_all_bikes(stations)
    4
    >>> stations == [
    ...  [7090, 'Danforth Ave / Lamb Ave',
    ...   43.681991, -79.329455, 15, 6, 8, True, True],    # return 2
    ...  [7486, 'Gerrard St E / Ted Reeve Dr',
    ...   43.684261, -79.299332, 22, 5, 17, False, False], # no change
    ...  [7571, 'Highfield Rd / Gerrard St E - SMART',
    ...   43.671685, -79.325176, 19, 8, 11, True, True]]   # rent 6
    True
    >>> stations = copy.deepcopy(HANDOUT_STATIONS)
    >>> balance_all_bikes(stations)
    0
    >>> stations == [
    ...  [7000, 'Ft. York / Capreol Crt.', 43.639832, -79.395954, 31, 17,
    ...   14, True, True],
    ...  [7001, 'Lower Jarvis St / The Esplanade', 43.647992, -79.370907,
    ...   15, 8, 7, True, True]]
    True

    """

    target_percent = calculate_target_percentage(stations)
    rented = 0
    returned = 0

    for station in stations:
        # This gives us the bikes we want to get close to target_percent.
        target_bikes = round(station[CAPACITY] * target_percent)
        if target_bikes > station[BIKES_AVAILABLE] and station[IS_RETURNING]:
            while (station[BIKES_AVAILABLE] != target_bikes
                   and station[DOCKS_AVAILABLE] != 0):
                return_bike(station[ID], stations)
                returned = returned + 1
        elif target_bikes < station[BIKES_AVAILABLE] and station[IS_RENTING]:
            while (station[BIKES_AVAILABLE] != target_bikes
                   and station[BIKES_AVAILABLE] != 0):
                rent_bike(station[ID], stations)
                rented = rented + 1
    return rented - returned


# We suggest using this as a helper function for the function
# balance_all_bikes.
def calculate_target_percentage(stations: List['Station']) -> float:
    """Return the target percentage of available bikes at each station
    from stations, for the purpose of re-balancing.

    >>> target_percent = calculate_target_percentage(FAKE_STATIONS)
    >>> abs(target_percent - 0.625) < EPSILON
    True

    """

    total_bikes = 0
    available_bikes = 0

    for station in stations:
        total_bikes = total_bikes + station[CAPACITY]
        available_bikes = available_bikes + station[BIKES_AVAILABLE]
    return available_bikes / total_bikes


def get_station(station_id: int, stations: List['Station']) -> 'Station':
    """Return the station from stations with id station_id. If there is
    no such station, return the empty list.

    >>> station = [7486, 'Gerrard St E / Ted Reeve Dr', 43.684261, -79.299332,
    ...            22, 5, 17, False, False]
    >>> get_station(7486, SAMPLE_STATIONS) == station
    True

    """

    for station in stations:
        if station[ID] == station_id:
            return station
    return []


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    ## To test your code with larger lists, you can uncomment the code
    ## below to read data from the provided CSV file.
    stations_file = open('stations.csv')
    bike_stations = csv_to_list(stations_file)
    clean_data(bike_stations)

    ## For example,
    print('This is the station with the most bikes:',
          get_station_with_max_bikes(bike_stations))
    print('This is the closest station:', get_nearest_station(43.671134, -79.325164, False, SAMPLE_STATIONS))
    ##pass
