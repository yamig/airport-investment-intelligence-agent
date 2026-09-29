def calculate_capacity_pressure(
    period_comparison: dict,
    passengers_field: str,
    seats_field: str
) -> dict:
    """
    Estimate capacity pressure between two periods.

    The calculation uses:
    - passenger growth
    - seat growth
    - load factor change
    - estimated additional seats required in period 2
      to maintain period 1's load factor

    This is a capacity-pressure proxy, not a direct measure
    of passengers who were unable to travel.
    """

    metrics = period_comparison["metrics"]

    passenger_data = metrics[passengers_field]
    seat_data = metrics[seats_field]

    period_1_passengers = passenger_data[
        "period_1_value"
    ]

    period_2_passengers = passenger_data[
        "period_2_value"
    ]

    period_1_seats = seat_data[
        "period_1_value"
    ]

    period_2_seats = seat_data[
        "period_2_value"
    ]

    passenger_growth_pct = passenger_data[
        "percentage_change"
    ]

    seat_growth_pct = seat_data[
        "percentage_change"
    ]

    if period_1_seats == 0:
        raise ValueError(
            "Period 1 seat capacity cannot be zero."
        )

    baseline_load_factor = (
        period_1_passengers
        / period_1_seats
    )

    current_load_factor = (
        period_2_passengers
        / period_2_seats
        if period_2_seats > 0
        else 0
    )

    required_seats = (
        period_2_passengers
        / baseline_load_factor
        if baseline_load_factor > 0
        else 0
    )

    estimated_capacity_gap = max(
        0,
        required_seats - period_2_seats
    )

    growth_gap = (
        passenger_growth_pct
        - seat_growth_pct
        if (
            passenger_growth_pct is not None
            and seat_growth_pct is not None
        )
        else None
    )

    load_factor_change = (
        current_load_factor
        - baseline_load_factor
    ) * 100

    return {
        "passenger_growth_pct":
            passenger_growth_pct,

        "seat_growth_pct":
            seat_growth_pct,

        "growth_gap_percentage_points": (
            round(growth_gap, 2)
            if growth_gap is not None
            else None
        ),

        "period_1_load_factor_pct":
            round(
                baseline_load_factor * 100,
                2
            ),

        "period_2_load_factor_pct":
            round(
                current_load_factor * 100,
                2
            ),

        "load_factor_change_points":
            round(
                load_factor_change,
                2
            ),

        "estimated_additional_seats_needed":
            round(
                estimated_capacity_gap
            ),

        "capacity_pressure_detected": (
            growth_gap is not None
            and growth_gap > 0
            and load_factor_change > 0
        )
    }