from collections import defaultdict

from data.data_store import get_dataset


def calculate_ratio(
    dataset_id: str,
    numerator_field: str,
    denominator_field: str,
    multiplier: float = 1.0,
    group_by: str | None = None
) -> dict:
    """
    Calculate a ratio using summed numerator and denominator values.

    Example:
    total_passengers / total_departures

    multiplier=100 can be used for percentages such as load factor.
    """

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    # One ratio for the entire dataset
    if group_by is None:

        numerator_total = 0.0
        denominator_total = 0.0

        for row in data:

            if (
                numerator_field in row
                and row[numerator_field] is not None
            ):
                numerator_total += float(
                    row[numerator_field]
                )

            if (
                denominator_field in row
                and row[denominator_field] is not None
            ):
                denominator_total += float(
                    row[denominator_field]
                )

        if denominator_total == 0:
            raise ValueError(
                f"Cannot calculate ratio because "
                f"'{denominator_field}' sums to zero."
            )

        ratio = (
            numerator_total / denominator_total
        ) * multiplier

        return {
            "numerator_field": numerator_field,
            "denominator_field": denominator_field,
            "numerator_total": numerator_total,
            "denominator_total": denominator_total,
            "multiplier": multiplier,
            "ratio": ratio
        }

    # Ratio separately for each group
    totals = defaultdict(
        lambda: {
            "numerator": 0.0,
            "denominator": 0.0
        }
    )

    for row in data:

        if group_by not in row:
            continue

        group_value = row[group_by]

        if group_value is None:
            continue

        group_value = str(group_value)

        if (
            numerator_field in row
            and row[numerator_field] is not None
        ):
            totals[group_value]["numerator"] += float(
                row[numerator_field]
            )

        if (
            denominator_field in row
            and row[denominator_field] is not None
        ):
            totals[group_value]["denominator"] += float(
                row[denominator_field]
            )

    results = {}

    for group_value, values in totals.items():

        denominator = values["denominator"]

        ratio = None

        if denominator != 0:
            ratio = (
                values["numerator"] / denominator
            ) * multiplier

        results[group_value] = {
            "numerator_total": values["numerator"],
            "denominator_total": denominator,
            "ratio": ratio
        }

    return {
        "numerator_field": numerator_field,
        "denominator_field": denominator_field,
        "multiplier": multiplier,
        "group_by": group_by,
        "groups": results
    }