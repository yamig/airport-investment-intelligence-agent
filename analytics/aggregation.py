from data.data_store import get_dataset


def aggregate_data(
    dataset_id: str,
    field: str,
    aggregation: str
) -> dict:

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    values = []

    for row in data:
        if field not in row:
            continue

        value = row[field]

        if value is not None:
            values.append(float(value))

    if not values:
        raise ValueError(
            f"No numeric values found for field '{field}'."
        )

    if aggregation == "sum":
        result = sum(values)

    elif aggregation == "average":
        result = sum(values) / len(values)

    elif aggregation == "min":
        result = min(values)

    elif aggregation == "max":
        result = max(values)

    elif aggregation == "count":
        result = len(values)

    else:
        raise ValueError(
            f"Unsupported aggregation: {aggregation}"
        )

    return {
        "field": field,
        "aggregation": aggregation,
        "result": result
    }

from collections import defaultdict


def aggregate_by_group(
    dataset_id: str,
    field: str,
    group_by: list[str],
    aggregation: str = "sum"
) -> dict:
    """
    Aggregate a numeric field separately for each group.

    group_by may contain one or more fields.

    Example:
    group_by=["origin_airport_code", "year"]
    """

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    if not group_by:
        raise ValueError(
            "At least one group_by field is required."
        )

    grouped_values = defaultdict(list)

    for row in data:

        if field not in row:
            continue

        if any(
            group_field not in row
            for group_field in group_by
        ):
            continue

        value = row[field]

        if value is None:
            continue

        group_key = tuple(
            str(row[group_field])
            for group_field in group_by
        )

        grouped_values[group_key].append(
            float(value)
        )

    if not grouped_values:
        raise ValueError(
            "No valid data found for grouping."
        )

    results = []

    for group_key, values in grouped_values.items():

        if aggregation == "sum":
            result = sum(values)

        elif aggregation == "average":
            result = sum(values) / len(values)

        elif aggregation == "min":
            result = min(values)

        elif aggregation == "max":
            result = max(values)

        elif aggregation == "count":
            result = len(values)

        else:
            raise ValueError(
                f"Unsupported aggregation: {aggregation}"
            )

        group_result = {
            group_by[index]: group_key[index]
            for index in range(len(group_by))
        }

        group_result["result"] = result

        results.append(group_result)

    return {
        "field": field,
        "aggregation": aggregation,
        "group_by": group_by,
        "groups": results
    }