"""A simple checker for types of functions in bikes.py."""

from typing import Any, Dict
import unittest
import checker_generic
import bikes

FILENAME = 'bikes.py'
PYTA_CONFIG = 'pyta/a2_pyta.txt'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'ID': 0, 'NAME': 1, 'LATITUDE': 2, 'LONGITUDE': 3, 'CAPACITY': 4,
    'BIKES_AVAILABLE': 5, 'DOCKS_AVAILABLE': 6, 'IS_RENTING': 7,
    'IS_RETURNING': 8, 'NO_KIOSK_LABEL': 'SMART', 'EARTH_RADIUS': 6371,
    'SOUTH': 'SOUTH', 'NORTH': 'NORTH', 'EAST': 'EAST', 'WEST': 'WEST'
}


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def setUp(self):
        """Init samle inputs."""

        self.stations = [
            [7090, 'Danforth Ave / Lamb Ave',
             43.681991, -79.329455, 15, 4, 10, True, True],
            [7486, 'Gerrard St E / Ted Reeve Dr',
             43.684261, -79.299332, 22, 5, 17, False, False],
            [7571, 'Highfield Rd / Gerrard St E - SMART',
             43.671685, -79.325176, 19, 14, 5, True, True]]

    def test_clean_data(self) -> None:
        """Function clean_data."""

        self._check_simple_type(
            bikes.clean_data,
            [[['abc', '123', '45.6', 'true', 'False']]],
            type(None))

    def test_has_kiosk(self) -> None:
        """Function has_kiosk."""

        self._check_simple_type(
            bikes.has_kiosk,
            [[7090, 'Danforth Ave / Lamb Ave', 43.681991, -79.329455,
              15, 4, 10, True, True]],
            bool)

    def test_get_total(self) -> None:
        """Function get_total."""

        self._check_simple_type(bikes.get_total, [5, self.stations], int)

    def test_get_station_with_max_bikes(self) -> None:
        """Function get_station_with_max_bikes."""

        self._check_simple_type(bikes.get_station_with_max_bikes,
                                [self.stations], int)

    def test_get_direction(self) -> None:
        """Function get_direction."""

        self._check_simple_type(bikes.get_direction,
                                [7090, 7571, self.stations],
                                str)

    def test_rent_bike(self) -> None:
        """Function rent_bike."""

        self._check_simple_type(bikes.rent_bike,
                                [7090, self.stations],
                                bool)

    def test_return_bike(self) -> None:
        """Function return_bike."""

        self._check_simple_type(bikes.return_bike,
                                [7090, self.stations],
                                bool)

    def test_get_nearest_station(self) -> None:
        """Function get_nearest_station."""

        self._check_simple_type(bikes.get_nearest_station,
                                [43.671134, -79.325164, False, self.stations],
                                int)

    def test_balance_all_bikes(self) -> None:
        """Function balance_all_bikes."""

        self._check_simple_type(bikes.balance_all_bikes,
                                [self.stations],
                                int)

    def test_calcualte_target_percentage(self) -> None:
        """Function calculate_target_percentage."""

        self._check_simple_type(bikes.calculate_target_percentage,
                                [self.stations],
                                float)

    def test_get_station(self) -> None:
        """Function get_station."""

        types = (int, str, float, float, int, int, int, bool, bool)
        self._test_returns_list_of(bikes.get_station,
                                   [7486, self.stations],
                                   types)

    def test_get_station_info(self) -> None:
        """Function get_station_info."""

        types = (str, int, int, bool)
        self._test_returns_list_of(bikes.get_station_info,
                                   [7486, self.stations],
                                   types)

    def test_get_stations_with_n_docks(self) -> None:
        """Function get_stations_with_n_docks."""

        print('\nChecking get_stations_with_n_docks...')
        result = checker_generic.returns_list_of_Ts(
            bikes.get_stations_with_n_docks,
            [2, self.stations],
            int)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, bikes)
        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.type_check_simple(func, args, expected)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _test_returns_list_of(self, func, args, types):
        """Check that func when called with args returns a list of elements
        of typef from types.

        """

        print('\nChecking {}...'.format(func.__name__))

        result = checker_generic.type_check_simple(func, args, list)
        self.assertTrue(result[0], result[1])

        msg = '{} should return a list of length {}'
        self.assertEqual(len(result[1]), len(types),
                         msg.format(func.__name__, len(types)))

        msg = ('Element at index {} in the list returned by get_station '
               'should be of type {}. Got {}.')
        for i, typ in enumerate(types):
            self.assertTrue(isinstance(result[1][i], typ),
                            msg.format(i, typ, result[1][i]))

        print('  check complete')

    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


checker_generic.ensure_no_io('bikes')

print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
