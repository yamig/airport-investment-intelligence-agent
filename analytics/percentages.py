from data.data_store import get_dataset


def calculate_percentage(
    dataset_id: str,
    part_field: str,
    total_field: str
) -> dict:

    data = get_dataset(dataset_id)

    if not data:
        raise ValueError("Dataset is empty.")

    part_total = 0.0
    total_total = 0.0

    for row in data:

        if part_field in row and row[part_field] is not None:
            part_total += float(row[part_field])

        if total_field in row and row[total_field] is not None:
            total_total += float(row[total_field])

    if total_total == 0:
        raise ValueError(
            f"Cannot calculate percentage because '{total_field}' sums to zero."
        )

    percentage = (
        part_total / total_total
    ) * 100

    return {
        "part_field": part_field,
        "total_field": total_field,
        "part_total": part_total,
        "total_total": total_total,
        "percentage": percentage
    }