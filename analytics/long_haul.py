from analytics.distance import calculate_distance


LONG_HAUL_THRESHOLD_MILES = 2485


def calculate_long_haul_percentage(
    flights: list[dict],
    airports: list[dict],
    threshold_miles: float = LONG_HAUL_THRESHOLD_MILES
) -> dict:
    """
    Calculate the percentage of departures classified as long-haul.

    Long-haul is defined by default as a route longer than
    2,485 statute miles (approximately 4,000 km).
    """

    airport_locations = {
        airport["icaoId"]: (
            float(airport["lat"]),
            float(airport["lon"])
        )
        for airport in airports
        if (
            airport.get("icaoId")
            and airport.get("lat") is not None
            and airport.get("lon") is not None
        )
    }

    valid_flights = 0
    long_haul_flights = 0
    missing_destination = 0
    missing_coordinates = 0

    routes = []

    for flight in flights:
        origin = flight.get("estDepartureAirport")
        destination = flight.get("estArrivalAirport")

        if not destination:
            missing_destination += 1
            continue

        if (
            origin not in airport_locations
            or destination not in airport_locations
        ):
            missing_coordinates += 1
            continue

        origin_lat, origin_lon = airport_locations[origin]
        dest_lat, dest_lon = airport_locations[destination]

        distance = calculate_distance(
            origin_lat,
            origin_lon,
            dest_lat,
            dest_lon
        )

        is_long_haul = distance >= threshold_miles

        valid_flights += 1

        if is_long_haul:
            long_haul_flights += 1

        routes.append({
            "origin": origin,
            "destination": destination,
            "distance_miles": round(distance, 2),
            "long_haul": is_long_haul
        })

    percentage = (
        long_haul_flights / valid_flights * 100
        if valid_flights > 0
        else 0
    )

    return {
        "long_haul_percentage": round(percentage, 2),
        "long_haul_flights": long_haul_flights,
        "valid_flights": valid_flights,
        "missing_destination": missing_destination,
        "missing_coordinates": missing_coordinates,
        "threshold_miles": threshold_miles,
        "routes": routes
    }