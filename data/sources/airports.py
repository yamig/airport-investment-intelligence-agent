import requests
import truststore


truststore.inject_into_ssl()

BASE_URL = "https://aviationweather.gov/api/data/airport"


def fetch_airports(
    airport_icao_codes: list[str]
) -> list[dict]:

    if not airport_icao_codes:
        raise ValueError(
            "At least one airport ICAO code is required."
        )

    codes = [
        code.strip().upper()
        for code in airport_icao_codes
        if code.strip()
    ]

    params = {
        "ids": ",".join(codes),
        "format": "json"
    }

    headers = {
        "User-Agent": "AirportInvestmentAgent/1.0"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=30
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Airport API request failed: {error}"
        ) from error

    if response.status_code == 204:
        return []

    if not response.ok:
        raise RuntimeError(
            f"Airport API returned "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    if not isinstance(data, list):
        raise RuntimeError(
            f"Unexpected Airport API response: {data}"
        )

    return data