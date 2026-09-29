from analytics.aggregation import aggregate_by_group


def compare_items(
    dataset_id: str,
    group_by: str,
    metric_field: str,
    aggregation: str = "sum"
) -> dict:
    """
    Compare two or more groups using a numeric metric.

    The metric is aggregated for each group before comparison.
    """

    aggregated = aggregate_by_group(
        dataset_id=dataset_id,
        field=metric_field,
        group_by=[group_by],
        aggregation=aggregation
    )

    values = {}

    for item in aggregated["groups"]:
        group_name = item[group_by]
        values[group_name] = item["result"]

    if len(values) < 2:
        raise ValueError(
            "At least two groups are required for comparison."
        )

    sorted_values = sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=True
    )

    highest_name, highest_value = sorted_values[0]
    lowest_name, lowest_value = sorted_values[-1]

    absolute_difference = highest_value - lowest_value

    if lowest_value == 0:
        percentage_difference = None
    else:
        percentage_difference = (
            absolute_difference / lowest_value
        ) * 100

    return {
        "group_by": group_by,
        "metric_field": metric_field,
        "aggregation": aggregation,
        "values": values,
        "highest": {
            "item": highest_name,
            "value": highest_value
        },
        "lowest": {
            "item": lowest_name,
            "value": lowest_value
        },
        "absolute_difference": absolute_difference,
        "percentage_difference": percentage_difference
    }