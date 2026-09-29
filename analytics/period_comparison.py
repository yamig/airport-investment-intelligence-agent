import calendar
from datetime import datetime


def _parse_date(
    value: str,
    is_end: bool = False
) -> datetime:

    value = value.strip()

    # Example: 2023-01-01T00:00:00.000
    if "T" in value:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
    )

    # Example: 2024-06-15
    if len(value) == 10:
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        )

    # Example: 2024-06
    if len(value) == 7:
        year, month = map(
            int,
            value.split("-")
        )

        if is_end:
            last_day = calendar.monthrange(
                year,
                month
            )[1]

            return datetime(
                year,
                month,
                last_day
            )

        return datetime(
            year,
            month,
            1
        )

    # Example: 2024
    if len(value) == 4:
        year = int(value)

        if is_end:
            return datetime(
                year,
                12,
                31
            )

        return datetime(
            year,
            1,
            1
        )

    raise ValueError(
        f"Unsupported date format: {value}"
    )


def compare_periods(
    data: list[dict],
    date_field: str,
    period_1_start: str,
    period_1_end: str,
    period_2_start: str,
    period_2_end: str,
    metric_fields: list[str],
    ratio_numerator_field: str | None = None,
    ratio_denominator_field: str | None = None,
    ratio_multiplier: float = 100.0
) -> dict:

    start_1 = _parse_date(
        period_1_start,
        is_end=False
    )

    end_1 = _parse_date(
        period_1_end,
        is_end=True
    )

    start_2 = _parse_date(
        period_2_start,
        is_end=False
    )

    end_2 = _parse_date(
        period_2_end,
        is_end=True
    )

    period_1_rows = []
    period_2_rows = []

    for row in data:
        raw_date = row.get(date_field)

        if not raw_date:
            continue

        row_date = _parse_date(
            str(raw_date)
        )

        if start_1 <= row_date <= end_1:
            period_1_rows.append(row)

        if start_2 <= row_date <= end_2:
            period_2_rows.append(row)

    metrics = {}

    for field in metric_fields:

        period_1_value = sum(
            float(row.get(field) or 0)
            for row in period_1_rows
        )

        period_2_value = sum(
            float(row.get(field) or 0)
            for row in period_2_rows
        )

        absolute_change = (
            period_2_value
            - period_1_value
        )

        if period_1_value != 0:
            percentage_change = (
                absolute_change
                / period_1_value
                * 100
            )
        else:
            percentage_change = None

        metrics[field] = {
            "period_1_value": period_1_value,
            "period_2_value": period_2_value,
            "absolute_change": absolute_change,
            "percentage_change": (
                round(percentage_change, 2)
                if percentage_change is not None
                else None
            )
        }

    result = {
        "period_1": {
            "start": period_1_start,
            "end": period_1_end,
            "rows": len(period_1_rows)
        },
        "period_2": {
            "start": period_2_start,
            "end": period_2_end,
            "rows": len(period_2_rows)
        },
        "metrics": metrics
    }

    if (
        ratio_numerator_field
        and ratio_denominator_field
    ):

        numerator_1 = sum(
            float(
                row.get(
                    ratio_numerator_field
                ) or 0
            )
            for row in period_1_rows
        )

        denominator_1 = sum(
            float(
                row.get(
                    ratio_denominator_field
                ) or 0
            )
            for row in period_1_rows
        )

        numerator_2 = sum(
            float(
                row.get(
                    ratio_numerator_field
                ) or 0
            )
            for row in period_2_rows
        )

        denominator_2 = sum(
            float(
                row.get(
                    ratio_denominator_field
                ) or 0
            )
            for row in period_2_rows
        )

        ratio_1 = (
            numerator_1
            / denominator_1
            * ratio_multiplier
            if denominator_1 != 0
            else None
        )

        ratio_2 = (
            numerator_2
            / denominator_2
            * ratio_multiplier
            if denominator_2 != 0
            else None
        )

        ratio_change = (
            ratio_2 - ratio_1
            if (
                ratio_1 is not None
                and ratio_2 is not None
            )
            else None
        )

        result["ratio"] = {
            "numerator_field":
                ratio_numerator_field,
            "denominator_field":
                ratio_denominator_field,
            "period_1_value": (
                round(ratio_1, 2)
                if ratio_1 is not None
                else None
            ),
            "period_2_value": (
                round(ratio_2, 2)
                if ratio_2 is not None
                else None
            ),
            "change": (
                round(ratio_change, 2)
                if ratio_change is not None
                else None
            )
        }

    return result