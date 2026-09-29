from collections import defaultdict

from data.data_store import get_dataset


def calculate_growth(
    dataset_id: str,
    field: str,
    time_field: str,
    group_by: str | None = None
) -> dict:
    """
    Calculate absolute and percentage growth over time.

    Values belonging to the same time period are summed first.

    If group_by is provided, growth is calculated separately
    for each group.
    """

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    # --------------------------------------------------
    # Case 1: one time series
    # Example: SFO passengers by year
    # --------------------------------------------------

    if group_by is None:

        totals_by_time = defaultdict(float)

        for row in data:

            if field not in row or time_field not in row:
                continue

            value = row[field]
            time_value = row[time_field]

            if value is None or time_value is None:
                continue

            totals_by_time[str(time_value)] += float(value)

        if len(totals_by_time) < 2:
            raise ValueError(
                "At least two time periods are required "
                "to calculate growth."
            )

        sorted_times = sorted(
            totals_by_time.keys(),
            key=lambda value: int(value)
        )

        start_time = sorted_times[0]
        end_time = sorted_times[-1]

        start_value = totals_by_time[start_time]
        end_value = totals_by_time[end_time]

        absolute_growth = end_value - start_value

        if start_value == 0:
            percentage_growth = None
        else:
            percentage_growth = (
                absolute_growth / start_value
            ) * 100

        return {
            "field": field,
            "time_field": time_field,
            "start_period": start_time,
            "end_period": end_time,
            "start_value": start_value,
            "end_value": end_value,
            "absolute_growth": absolute_growth,
            "percentage_growth": percentage_growth,
            "values_by_period": dict(totals_by_time)
        }


    # --------------------------------------------------
    # Case 2: multiple entities
    # Example: SFO and LAX passengers by year
    # --------------------------------------------------

    totals_by_group = defaultdict(
        lambda: defaultdict(float)
    )

    for row in data:

        if (
            field not in row
            or time_field not in row
            or group_by not in row
        ):
            continue

        value = row[field]
        time_value = row[time_field]
        group_value = row[group_by]

        if (
            value is None
            or time_value is None
            or group_value is None
        ):
            continue

        totals_by_group[str(group_value)][
            str(time_value)
        ] += float(value)

    results = {}

    for group_value, totals_by_time in totals_by_group.items():

        if len(totals_by_time) < 2:
            continue

        sorted_times = sorted(
            totals_by_time.keys(),
            key=lambda value: int(value)
        )

        start_time = sorted_times[0]
        end_time = sorted_times[-1]

        start_value = totals_by_time[start_time]
        end_value = totals_by_time[end_time]

        absolute_growth = end_value - start_value

        if start_value == 0:
            percentage_growth = None
        else:
            percentage_growth = (
                absolute_growth / start_value
            ) * 100

        results[group_value] = {
            "start_period": start_time,
            "end_period": end_time,
            "start_value": start_value,
            "end_value": end_value,
            "absolute_growth": absolute_growth,
            "percentage_growth": percentage_growth,
            "values_by_period": dict(totals_by_time)
        }

    if not results:
        raise ValueError(
            "Not enough data to calculate growth."
        )

    return {
        "field": field,
        "time_field": time_field,
        "group_by": group_by,
        "groups": results
    }

def calculate_cagr(
    dataset_id: str,
    field: str,
    time_field: str,
    group_by: str | None = None
) -> dict:
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Values within each time period are summed first.
    """

    growth = calculate_growth(
        dataset_id=dataset_id,
        field=field,
        time_field=time_field,
        group_by=group_by
    )

    # --------------------------------------------------
    # Case 1: one time series
    # --------------------------------------------------

    if group_by is None:

        start_period = float(
            growth["start_period"]
        )

        end_period = float(
            growth["end_period"]
        )

        number_of_years = (
            end_period - start_period
        )

        if number_of_years <= 0:
            raise ValueError(
                "CAGR requires at least two different years."
            )

        start_value = growth["start_value"]
        end_value = growth["end_value"]

        if start_value <= 0:
            raise ValueError(
                "CAGR requires a positive start value."
            )

        cagr = (
            (
                end_value / start_value
            ) ** (1 / number_of_years)
            - 1
        ) * 100

        return {
            "field": field,
            "start_period": growth["start_period"],
            "end_period": growth["end_period"],
            "start_value": start_value,
            "end_value": end_value,
            "years": number_of_years,
            "cagr_percentage": cagr
        }

    # --------------------------------------------------
    # Case 2: multiple groups
    # --------------------------------------------------

    results = {}

    for group_value, group_growth in growth[
        "groups"
    ].items():

        start_period = float(
            group_growth["start_period"]
        )

        end_period = float(
            group_growth["end_period"]
        )

        number_of_years = (
            end_period - start_period
        )

        start_value = group_growth[
            "start_value"
        ]

        end_value = group_growth[
            "end_value"
        ]

        if (
            number_of_years <= 0
            or start_value <= 0
        ):
            continue

        cagr = (
            (
                end_value / start_value
            ) ** (1 / number_of_years)
            - 1
        ) * 100

        results[group_value] = {
            "start_period": group_growth[
                "start_period"
            ],
            "end_period": group_growth[
                "end_period"
            ],
            "start_value": start_value,
            "end_value": end_value,
            "years": number_of_years,
            "cagr_percentage": cagr
        }

    if not results:
        raise ValueError(
            "Not enough valid data to calculate CAGR."
        )

    return {
        "field": field,
        "group_by": group_by,
        "groups": results
    }