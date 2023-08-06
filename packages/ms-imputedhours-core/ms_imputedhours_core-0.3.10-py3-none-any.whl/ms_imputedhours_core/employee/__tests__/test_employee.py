import unittest
from datetime import datetime
from unittest.mock import Mock

from freezegun import freeze_time

from ms_imputedhours_core.employee import calculate_real_capacity, get_real_fte

DEFAULT_AGREEMENT_HOURS = {  # January 2022
    'totalHours': 168.0,
    'days': {
        '1-1': '0',
        '2-1': '0',
        '3-1': '8',
        '4-1': '8',
        '5-1': '8',
        '6-1': '8',
        '7-1': '8',
        '8-1': '0',
        '9-1': '0',
        '10-1': '8',
        '11-1': '8',
        '12-1': '8',
        '13-1': '8',
        '14-1': '8',
        '15-1': '0',
        '16-1': '0',
        '17-1': '8',
        '18-1': '8',
        '19-1': '8',
        '20-1': '8',
        '21-1': '8',
        '22-1': '0',
        '23-1': '0',
        '24-1': '8',
        '25-1': '8',
        '26-1': '8',
        '27-1': '8',
        '28-1': '8',
        '29-1': '0',
        '30-1': '0',
        '31-1': '8',
    },
}


class TestSuite(unittest.TestCase):
    @freeze_time("2022-11-11")
    def test_get_real_fte_returns_successfactor_fte_when_date_is_not_future_and_employee_has_not_fte(
        self,
    ):  # noqa: E501
        expected_result = 1.0  # 1.0 === 100%
        successfactor_data = {'FTE': 100}
        employeeFTE = {}
        date = Mock()
        date.year = 2021
        date.month = 10

        result = get_real_fte(successfactor_data, employeeFTE, date)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_get_real_fte_returns_employee_fte_when_date_is_not_future_and_employee_has_fte(
        self,
    ):  # noqa: E501
        expected_result = 0.5  # 0.5 === 50%
        successfactor_data = {'FTE': 100}
        employeeFTE = {'fte': 0.5}
        date = Mock()
        date.year = 2021
        date.month = 10

        result = get_real_fte(successfactor_data, employeeFTE, date)

        self.assertEqual(result, expected_result)

    @freeze_time("2021-11-11")
    def test_get_real_fte_returns_successfactor_fte_when_date_is_for_future(
        self,
    ):  # noqa: E501
        expected_result = 1  # 100%
        successfactor_data = {'FTE': 100}
        employeeFTE = {'fte': 50}
        date = Mock()
        date.year = 2022
        date.month = 10

        result = get_real_fte(successfactor_data, employeeFTE, date)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_full_capacity_when_is_normal_month(
        self,
    ):  # noqa: E501
        """
        A normal month is a definition for a month where the employee
        will work 100% of the hours of his agreement, and does not
        coincide with any special date as the end or start
        of the employment contract.
        """
        expected_result = 168.0
        hiring_date = datetime.strptime('17/09/2021', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1.0  # 100%
        calculate_range = True

        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_half_capacity_when_is_normal_month_and_fte_zero_point_five(
        self,
    ):  # noqa: E501
        """
        A normal month is a definition for a month where the employee
        will work 100% of the hours of his agreement, and does not
        coincide with any special date as the end or start
        of the employment contract.
        """
        expected_result = 84.0
        hiring_date = datetime.strptime('17/09/2021', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 0.5  # 50%
        calculate_range = False

        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_zero_when_date_is_before_hired(
        self,
    ):  # noqa: E501
        """
        A normal month is a definition for a month where the employee
        will work 100% of the hours of his agreement, and does not
        coincide with any special date as the end or start
        of the employment contract.
        """
        expected_result = 0.0
        hiring_date = datetime.strptime('01/02/2022', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
        calculate_range = False

        result = calculate_real_capacity(
            DEFAULT_AGREEMENT_HOURS,
            hiring_date,
            end_date,
            date,
            to_date,
            fte,
            calculate_range,
        )

        self.assertEqual(result, expected_result)

    @freeze_time("2022-1-31")
    def test_calculate_real_capacity_return_all_capacity_when_calculate_range_is_false(
        self,
    ):  # noqa: E501
        """
        A normal month is a definition for a month where the employee
        will work 100% of the hours of his agreement, and does not
        coincide with any special date as the end or start
        of the employment contract.
        """
        expected_result = 168.0
        hiring_date = datetime.strptime('01/02/2021', '%d/%m/%Y')
        end_date = datetime.strptime('15/01/2022', '%d/%m/%Y')
        from_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
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

        self.assertEqual(result, expected_result)

    @freeze_time("2022-1-31")
    def test_calculate_real_capacity_return_all_capacity_when_employee_end_or_hiring_date_months_are_not_equal_thant_calculation(
        self,
    ):  # noqa: E501
        """
        A normal month is a definition for a month where the employee
        will work 100% of the hours of his agreement, and does not
        coincide with any special date as the end or start
        of the employment contract.
        """
        expected_result = 168.0
        hiring_date = datetime.strptime('01/02/2021', '%d/%m/%Y')
        end_date = datetime.strptime('15/02/2022', '%d/%m/%Y')
        from_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
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

        self.assertEqual(result, expected_result)

    @freeze_time("2022-01-31")
    def test_calculate_real_capacity_return_only_work_days_when_employee_has_end_date(
        self,
    ):  # noqa: E501
        expected_result = 80.0
        hiring_date = datetime.strptime('01/02/2021', '%d/%m/%Y')
        end_date = datetime.strptime('15/01/2022', '%d/%m/%Y')
        from_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
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

        self.assertEqual(result, expected_result)

    @freeze_time("2022-01-31")
    def test_calculate_real_capacity_return_only_work_days_when_employee_hiring_date_is_same_month_than_calculation(  # noqa: E501
        self,
    ):
        expected_result = 88.0
        hiring_date = datetime.strptime('15/01/2022', '%d/%m/%Y')
        end_date = None
        from_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
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

        self.assertEqual(result, expected_result)

    @freeze_time("2022-01-31")
    def test_calculate_real_capacity_return_only_work_days_when_employee_hiring_and_end_date_are_in_calculation_month(  # noqa: E501
        self,
    ):
        expected_result = 80.0
        hiring_date = datetime.strptime('15/01/2022', '%d/%m/%Y')
        end_date = datetime.strptime('28/01/2022', '%d/%m/%Y')
        from_date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1  # 100%
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

        self.assertEqual(result, expected_result)
