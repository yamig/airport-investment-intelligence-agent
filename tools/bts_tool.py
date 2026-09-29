from enum import Enum

from data.sources.bts import fetch_bts_data
from data.data_store import save_dataset
from data.source_catalog import DATA_SOURCES


BTS_FIELDS = list(
    DATA_SOURCES["bts_summary"]["fields"].keys()
)


BTSField = Enum(
    "BTSField",
    {field: field for field in BTS_FIELDS},
    type=str
)


def get_bts_data(
    airport_codes: list[str],
    fields: list[BTSField],
    start_year: int | None = None,
    end_year: int | None = None
) -> dict:
    """
    Retrieve historical airport-level data from the BTS summary dataset.

    Use this tool for BTS airport metrics such as passengers,
    departures, seats, load factor, freight, and domestic or
    international traffic.

    Args:
        airport_codes:
            IATA airport codes, for example ["SFO", "LAX"].

        fields:
            BTS fields to retrieve.

        start_year:
            Optional first year to include.

        end_year:
            Optional last year to include.

    Returns:
        Information about the stored BTS dataset.
    """

    selected_fields = [
        field.value if isinstance(field, BTSField) else str(field)
        for field in fields
    ]

    # These fields are needed internally by the tool
    if "origin_airport_code" not in selected_fields:
        selected_fields.append("origin_airport_code")

    if "year" not in selected_fields:
        selected_fields.append("year")

    if "reporting_month" not in selected_fields:
        selected_fields.append("reporting_month")

    query = "SELECT " + ", ".join(selected_fields)

    filters = []

    if airport_codes:
        airports = ", ".join(
            f"'{code.upper()}'"
            for code in airport_codes
        )

        filters.append(
            f"origin_airport_code IN ({airports})"
        )

    if start_year is not None:
        filters.append(
            f"year >= '{start_year}'"
        )

    if end_year is not None:
        filters.append(
            f"year <= '{end_year}'"
        )

    if filters:
        query += " WHERE " + " AND ".join(filters)

    print("\nBTS TOOL CALLED")
    print(query)

    # Retrieve real data from BTS
    data = fetch_bts_data(query)

    # Store the dataset so analytics tools can use it later
    dataset_id = save_dataset(data)

    # --------------------------------------------------
    # Find latest year available
    # --------------------------------------------------

    years = [
        int(row["year"])
        for row in data
        if row.get("year")
    ]

    latest_year = max(years) if years else None

    # --------------------------------------------------
    # Find latest COMPLETE year
    #
    # reporting_month is returned by BTS as something like:
    # "2025-01-01T00:00:00.000"
    #
    # Therefore we extract the month from the date string.
    # A year is considered complete only if every requested
    # airport has data for all 12 months.
    # --------------------------------------------------

    months_by_year_and_airport = {}

    for row in data:
        year = row.get("year")
        reporting_month = row.get("reporting_month")
        airport = row.get("origin_airport_code")

        if not year or not reporting_month or not airport:
            continue

        year = int(year)

        # Example:
        # "2025-03-01T00:00:00.000" -> 3
        if isinstance(reporting_month, str) and "-" in reporting_month:
            month = int(reporting_month.split("-")[1])
        else:
            month = int(reporting_month)

        if year not in months_by_year_and_airport:
            months_by_year_and_airport[year] = {}

        if airport not in months_by_year_and_airport[year]:
            months_by_year_and_airport[year][airport] = set()

        months_by_year_and_airport[year][airport].add(month)

    requested_airports = {
        code.upper()
        for code in airport_codes
    }

    complete_years = []

    for year, airports_data in months_by_year_and_airport.items():

        all_airports_complete = all(
            airport in airports_data
            and len(airports_data[airport]) == 12
            for airport in requested_airports
        )

        if all_airports_complete:
            complete_years.append(year)

    latest_complete_year = (
        max(complete_years)
        if complete_years
        else None
    )

    # --------------------------------------------------
    # Return metadata to the agent
    # --------------------------------------------------

    return {
        "dataset_id": dataset_id,
        "row_count": len(data),
        "fields": selected_fields,
        "latest_year": latest_year,
        "latest_complete_year": latest_complete_year
    }