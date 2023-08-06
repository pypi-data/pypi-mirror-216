import unittest
from datetime import date

from ms_imputedhours_core.employee import calculate_real_capacity

DEFAULT_AGREEMENT_HOURS = {
    'totalHours': 142.0,
    'days': {
        '1-4': '0',
        '2-4': '0',
        '3-4': '8',
        '4-4': '5.5',
        '5-4': '0',
        '6-4': '0',
        '7-4': '8',
        '8-4': '8',
        '9-4': '0',
        '10-4': '8',
        '11-4': '5.5',
        '12-4': '0',
        '13-4': '0',
        '14-4': '8',
        '15-4': '8',
        '16-4': '8',
        '17-4': '8',
        '18-4': '5.5',
        '19-4': '0',
        '20-4': '0',
        '21-4': '8',
        '22-4': '8',
        '23-4': '8',
        '24-4': '8',
        '25-4': '5.5',
        '26-4': '0',
        '27-4': '0',
        '28-4': '8',
        '29-4': '8',
        '30-4': '8',
    },
}


class TestRealCapacity(unittest.TestCase):
    def test_no_hiring_date(self):
        hiring_date = None
        end_date = None
        from_date = date(2023, 2, 1)
        to_date = date(2023, 2, 28)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, from_date, to_date, fte, calculate_range)

        self.assertEqual(result, 0)

    def test_same_month_hiring_date(self):
        hiring_date = date(2023, 4, 1)
        end_date = None
        from_date = date(2023, 4, 1)
        to_date = date(2023, 4, 30)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, from_date, to_date, fte, calculate_range)

        self.assertEqual(result, 142.0)

    def test_same_month_hiring_and_end_date(self):
        hiring_date = date(2023, 4, 1)
        end_date = date(2023, 4, 15)
        from_date = date(2023, 4, 1)
        to_date = date(2023, 4, 30)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, from_date, to_date, fte, calculate_range)

        self.assertEqual(result, 59.0)

    def test_same_month_end_date(self):
        hiring_date = date(2023, 3, 1)
        end_date = date(2023, 4, 15)
        from_date = date(2023, 5, 1)
        to_date = date(2023, 5, 31)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, from_date, to_date, fte, calculate_range)

        self.assertEqual(result, 0)

    def test_end_date_within_range(self):
        agreement_hours = {
            'totalHours': 142.0,
            'days': {
                '1-5': '0',
                '2-5': '0',
                '3-5': '8',
                '4-5': '5.5',
                '5-5': '0',
                '6-5': '0',
                '7-5': '8',
                '8-5': '8',
                '9-5': '0',
                '10-5': '8',
                '11-5': '5.5',
                '12-5': '0',
                '13-5': '0',
                '14-5': '8',
                '15-5': '8',
                '16-5': '8',
                '17-5': '8',
                '18-5': '5.5',
                '19-5': '0',
                '20-5': '0',
                '21-5': '8',
                '22-5': '8',
                '23-5': '8',
                '24-5': '8',
                '25-5': '5.5',
                '26-5': '0',
                '27-5': '0',
                '28-5': '8',
                '29-5': '8',
                '30-5': '8',
            },
        }
        hiring_date = date(2023, 3, 1)
        end_date = date(2023, 5, 15)
        from_date = date(2023, 5, 1)
        to_date = date(2023, 5, 31)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(
            agreement_hours,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 59)

    def test_start_date_after_end_date(self):
        hiring_date = date(2023, 1, 1)
        end_date = date(2023, 2, 15)
        from_date = date(2023, 5, 1)
        to_date = date(2023, 5, 31)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 0)

    def test_partial_month(self):
        hiring_date = date(2023, 3, 1)
        end_date = None
        from_date = date(2023, 4, 2)
        to_date = date(2023, 4, 30)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 142.0)

    def test_full_month(self):
        hiring_date = date(2023, 3, 1)
        end_date = None
        from_date = date(2023, 4, 1)
        to_date = date(2023, 4, 30)
        fte = 1
        calculate_range = True
        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 142.0)

    def test_fte(self):
        hiring_date = date(2023, 3, 1)
        end_date = None
        from_date = date(2023, 4, 1)
        to_date = date(2023, 4, 30)
        fte = 0.5
        calculate_range = True
        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 71.0)

    def test_calculate_range_false(self):
        hiring_date = date(2023, 4, 15)
        end_date = None
        from_date = date(2023, 4, 1)
        to_date = date(2023, 4, 30)
        fte = 1
        calculate_range = False
        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            from_date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, 142.0)
