from analytics.aggregation import (
    aggregate_data as _aggregate_data,
    aggregate_by_group as _aggregate_by_group
)

from analytics.percentages import (
    calculate_percentage as _calculate_percentage
)

from analytics.growth import (
    calculate_growth as _calculate_growth,
    calculate_cagr as _calculate_cagr
)

from analytics.ranking import (
    rank_items as _rank_items
)

from analytics.ratios import (
    calculate_ratio as _calculate_ratio
)

from analytics.comparison import (
    compare_items as _compare_items
)

from data.data_store import get_dataset
from analytics.long_haul import calculate_long_haul_percentage

from analytics.period_comparison import (
    compare_periods as compare_periods_data
)

from analytics.capacity_pressure import (
    calculate_capacity_pressure as calculate_capacity_pressure_data
)


def aggregate_data(
    dataset_id: str,
    field: str,
    aggregation: str
) -> dict:
    """
    Aggregate a numeric field from a stored dataset.

    Supported aggregations:
    sum, average, min, max, count.
    """

    return _aggregate_data(
        dataset_id=dataset_id,
        field=field,
        aggregation=aggregation
    )


def calculate_percentage(
    dataset_id: str,
    part_field: str,
    total_field: str
) -> dict:
    """
    Calculate what percentage one numeric field represents
    out of another numeric field.
    """

    return _calculate_percentage(
        dataset_id=dataset_id,
        part_field=part_field,
        total_field=total_field
    )


def calculate_growth(
    dataset_id: str,
    field: str,
    time_field: str,
    group_by: str | None = None
) -> dict:
    """
    Calculate deterministic growth of a numeric field over time.

    Values within the same time period are summed first.

    If group_by is provided, growth is calculated separately
    for each group.
    """

    return _calculate_growth(
        dataset_id=dataset_id,
        field=field,
        time_field=time_field,
        group_by=group_by
    )

def rank_items(
    dataset_id: str,
    group_by: str,
    metric_field: str,
    order: str = "descending"
) -> dict:
    """
    Rank groups by a numeric metric.

    The metric is summed for each group before ranking.
    """

    return _rank_items(
        dataset_id=dataset_id,
        group_by=group_by,
        metric_field=metric_field,
        order=order
    )

def aggregate_by_group(
    dataset_id: str,
    field: str,
    group_by: list[str],
    aggregation: str = "sum"
) -> dict:
    """
    Aggregate a numeric field separately for one or more groups.
    """

    return _aggregate_by_group(
        dataset_id=dataset_id,
        field=field,
        group_by=group_by,
        aggregation=aggregation
    )

def calculate_ratio(
    dataset_id: str,
    numerator_field: str,
    denominator_field: str,
    multiplier: float = 1.0,
    group_by: str | None = None
) -> dict:
    """
    Calculate a ratio between two numeric fields.

    Use this tool for questions involving:
    - per departure
    - per flight
    - ratios
    - passengers per departure
    - passengers per seat

    The numerator and denominator are summed before
    calculating the ratio.

    Use multiplier=100 only when the result should
    be expressed as a percentage.
    """

    return _calculate_ratio(
        dataset_id=dataset_id,
        numerator_field=numerator_field,
        denominator_field=denominator_field,
        multiplier=multiplier,
        group_by=group_by
    )


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

    return _compare_items(
        dataset_id=dataset_id,
        group_by=group_by,
        metric_field=metric_field,
        aggregation=aggregation
    )

def calculate_cagr(
    dataset_id: str,
    field: str,
    time_field: str,
    group_by: str | None = None
) -> dict:
    """
    Calculate Compound Annual Growth Rate for a numeric metric.

    Use this tool when the user asks for CAGR,
    annualized growth, or average annual growth rate
    across multiple years.
    """

    return _calculate_cagr(
        dataset_id=dataset_id,
        field=field,
        time_field=time_field,
        group_by=group_by
    )



def calculate_long_haul(
    flights_dataset_id: str,
    airports_dataset_id: str,
    threshold_miles: float = 2485
) -> dict:
    """
    Calculate the percentage of flights classified as long-haul.

    flights_dataset_id:
        Dataset containing individual OpenSky flight records.

    airports_dataset_id:
        Dataset containing airport information and coordinates.

    threshold_miles:
        Minimum route distance considered long-haul.
        Defaults to 2,485 statute miles
        (approximately 4,000 km).
    """

    flights = get_dataset(
        flights_dataset_id
    )

    airports = get_dataset(
        airports_dataset_id
    )

    result = calculate_long_haul_percentage(
        flights=flights,
        airports=airports,
        threshold_miles=threshold_miles
    )

    total_flights = len(flights)

    excluded_flights = (
        result["missing_destination"]
        + result["missing_coordinates"]
    )

    coverage_percentage = (
        result["valid_flights"] / total_flights * 100
        if total_flights > 0
        else 0
    )

    return {
        "long_haul_percentage":
            result["long_haul_percentage"],

        "long_haul_flights":
            result["long_haul_flights"],

        "valid_flights":
            result["valid_flights"],

        "total_flights":
            total_flights,

        "excluded_flights":
            excluded_flights,

        "coverage_percentage":
            round(coverage_percentage, 2),

        "missing_destination":
            result["missing_destination"],

        "missing_coordinates":
            result["missing_coordinates"],

        "threshold_miles":
            result["threshold_miles"]
    }

def calculate_capacity_pressure(
    dataset_id: str,
    date_field: str,
    period_1_start: str,
    period_1_end: str,
    period_2_start: str,
    period_2_end: str,
    passengers_field: str,
    seats_field: str
) -> dict:
    """
    Estimate demand-versus-capacity pressure between two periods.

    Use this when analyzing whether passenger demand is
    growing faster than available seat capacity.

    The result includes passenger growth, seat growth,
    load factor change, and an estimated number of
    additional seats that would have been needed in
    period 2 to maintain period 1's load factor.

    This is a capacity-pressure / unmet-demand proxy.
    It is not a direct count of passengers who were
    unable to travel.
    """

    data = get_dataset(dataset_id)

    comparison = compare_periods_data(
        data=data,
        date_field=date_field,
        period_1_start=period_1_start,
        period_1_end=period_1_end,
        period_2_start=period_2_start,
        period_2_end=period_2_end,
        metric_fields=[
            passengers_field,
            seats_field
        ],
        ratio_numerator_field=passengers_field,
        ratio_denominator_field=seats_field,
        ratio_multiplier=100
    )

    pressure = calculate_capacity_pressure_data(
        period_comparison=comparison,
        passengers_field=passengers_field,
        seats_field=seats_field
    )

    return {
        "period_1": comparison["period_1"],
        "period_2": comparison["period_2"],
        **pressure
    }

def compare_periods(
    dataset_id: str,
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
    """
    Compare numeric metrics between any two time periods.

    Use this for month-over-month, year-over-year,
    quarter comparisons, or arbitrary date ranges.

    Metric fields are summed within each period.

    Optionally calculates a ratio from two summed fields,
    such as passengers / seats * 100 for load factor.
    """

    data = get_dataset(dataset_id)

    return compare_periods_data(
        data=data,
        date_field=date_field,
        period_1_start=period_1_start,
        period_1_end=period_1_end,
        period_2_start=period_2_start,
        period_2_end=period_2_end,
        metric_fields=metric_fields,
        ratio_numerator_field=ratio_numerator_field,
        ratio_denominator_field=ratio_denominator_field,
        ratio_multiplier=ratio_multiplier
    )