from calendar import monthrange
from datetime import datetime, timedelta

HUNDRED_PERCENT = 100
DEFAULT_FTE = 1.0  # 100 %


def get_real_fte(successfactor, employeeFTE, date):
    """Calculate employee FTE.
    When we want to calculate the FTE of an employee, we do it for a specific
    month since this can change.

     Rules:
         - If the date we want to calculate the FTE is from the current
           month into the future, then we will take the FTE value returned
           by the Success factor Bigquery table.
         - If for the month we want to calculate the FTE is prior to
           the current one and it already has a value in the Capacity
           table, this means that it was already calculated and we will
           use that value.

     args:
        successfactor (dict): BigQuery results from the successfactor table.
        employeeFTE (dict): Bigquery results from the Capacity table.
        date (date): Month on which the FTE is being calculated

    Returns:
        float: Real FTE for a employee in specific month.
    """
    today = datetime.today()
    is_past_date = (date.year, date.month) <= (today.year, today.month)

    try:
        # Some employees has null as FTE.
        fte = successfactor['FTE'] / HUNDRED_PERCENT
    except (KeyError, TypeError):
        fte = DEFAULT_FTE

    if employeeFTE and is_past_date:
        fte = employeeFTE['fte']

    return fte


def calculate_real_capacity(
    agreement_hours,
    hiring_date,
    end_date,
    from_date,
    to_date,
    fte,
    calculate_range=False,
):
    if not hiring_date:
        return 0

    if not calculate_range:
        last_day_of_month = monthrange(from_date.year, from_date.month)[1]
        to_date = from_date.replace(day=last_day_of_month)

    if end_date and end_date <= from_date or hiring_date >= to_date:
        return 0

    if hiring_date > from_date:
        from_date = hiring_date

    if end_date and end_date < to_date:
        to_date = end_date

    if calculate_range:
        days = agreement_hours["days"]
        total_hours = 0
        current_date = from_date
        while current_date <= to_date:
            key = f"{current_date.day}-{current_date.month}"
            if key in days:
                total_hours += float(days[key])
            current_date += timedelta(days=1)
    else:
        total_hours = float(agreement_hours["totalHours"])

    real_capacity = total_hours * fte
    return real_capacity
