from datetime import datetime, timedelta, timezone

from data.sources.opensky import fetch_departures
from data.data_store import save_dataset


def get_opensky_departures(
    airport_icao: str,
    date: str
) -> dict:
    """
    Retrieve observed flights departing from an airport
    on a specific date.

    airport_icao:
        ICAO airport code, for example PANC for Anchorage.

    date:
        Date in YYYY-MM-DD format.
    """

    try:
        start = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).replace(
            tzinfo=timezone.utc
        )

    except ValueError as error:
        raise ValueError(
            "date must use YYYY-MM-DD format."
        ) from error

    end = start + timedelta(
        hours=23,
        minutes=59,
        seconds=59
    )

    data = fetch_departures(
        airport_icao=airport_icao,
        begin=int(start.timestamp()),
        end=int(end.timestamp())
    )

    dataset_id = save_dataset(data)

    destinations = sorted({
        flight["estArrivalAirport"]
        for flight in data
        if flight.get("estArrivalAirport")
    })

    destinations_identified = sum(
        1
        for flight in data
        if flight.get("estArrivalAirport")
    )

    return {
        "dataset_id": dataset_id,
        "row_count": len(data),
        "destinations_identified": destinations_identified,
        "destination_airports": destinations,
        "airport_icao": airport_icao.upper(),
        "date": date
    }