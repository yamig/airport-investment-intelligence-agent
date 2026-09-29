from collections import defaultdict

from data.data_store import get_dataset


def rank_items(
    dataset_id: str,
    group_by: str,
    metric_field: str,
    order: str = "descending"
) -> dict:
    """
    Rank groups by the summed value of a numeric metric field.
    """

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    totals = defaultdict(float)

    for row in data:

        if group_by not in row or metric_field not in row:
            continue

        group_value = row[group_by]
        metric_value = row[metric_field]

        if group_value is None or metric_value is None:
            continue

        totals[str(group_value)] += float(metric_value)

    if not totals:
        raise ValueError(
            "No valid values were found for ranking."
        )

    if order not in {"ascending", "descending"}:
        raise ValueError(
            "Order must be 'ascending' or 'descending'."
        )

    reverse = order == "descending"

    ranked = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=reverse
    )

    results = [
        {
            "rank": index,
            group_by: group,
            metric_field: value
        }
        for index, (group, value)
        in enumerate(ranked, start=1)
    ]

    return {
        "group_by": group_by,
        "metric_field": metric_field,
        "order": order,
        "ranking": results
    }