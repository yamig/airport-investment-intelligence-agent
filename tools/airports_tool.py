from data.sources.airports import fetch_airports
from data.data_store import save_dataset, get_dataset


def get_airport_info(
    airport_icao_codes: list[str] | None = None,
    flights_dataset_id: str | None = None
) -> dict:
    """
    Retrieve airport information.

    Airport codes can be supplied directly using airport_icao_codes.

    If flights_dataset_id is provided, airport codes are automatically
    extracted from the OpenSky flight dataset, including departure
    and arrival airports.

    The returned airport data may include coordinates, elevation,
    runways, tower information, services, and other characteristics.
    """

    codes = set()

    # Option 1:
    # Airport codes were supplied directly.
    if airport_icao_codes:
        codes.update(
            code.strip().upper()
            for code in airport_icao_codes
            if code.strip()
        )

    # Option 2:
    # Extract airport codes automatically from flight data.
    if flights_dataset_id:
        flights = get_dataset(
            flights_dataset_id
        )

        for flight in flights:
            origin = flight.get(
                "estDepartureAirport"
            )

            destination = flight.get(
                "estArrivalAirport"
            )

            if origin:
                codes.add(origin)

            if destination:
                codes.add(destination)

    if not codes:
        raise ValueError(
            "Provide airport_icao_codes "
            "or flights_dataset_id."
        )

    codes = sorted(codes)

    data = fetch_airports(codes)

    dataset_id = save_dataset(data)

    found_codes = {
        airport.get("icaoId")
        for airport in data
        if airport.get("icaoId")
    }

    missing_codes = [
        code
        for code in codes
        if code not in found_codes
    ]

    return {
        "dataset_id": dataset_id,
        "row_count": len(data),
        "requested_airport_count": len(codes),
        "found_airports": sorted(found_codes),
        "missing_airports": missing_codes
    }