import os
from datetime import datetime, timedelta

import requests
import truststore


truststore.inject_into_ssl()

BASE_URL = "https://opensky-network.org/api"

TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)

TOKEN_REFRESH_MARGIN = 30


class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = None

    def get_token(self) -> str:
        if (
            self.token
            and self.expires_at
            and datetime.now() < self.expires_at
        ):
            return self.token

        return self._refresh()

    def _refresh(self) -> str:
        client_id = os.getenv("OPENSKY_CLIENT_ID")
        client_secret = os.getenv("OPENSKY_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise RuntimeError(
                "OpenSky credentials are missing. "
                "Set OPENSKY_CLIENT_ID and "
                "OPENSKY_CLIENT_SECRET."
            )

        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30,
        )

        if not response.ok:
            raise RuntimeError(
                f"OpenSky authentication failed "
                f"({response.status_code}): "
                f"{response.text}"
            )

        data = response.json()

        self.token = data["access_token"]

        expires_in = data.get("expires_in", 1800)

        self.expires_at = (
            datetime.now()
            + timedelta(
                seconds=expires_in - TOKEN_REFRESH_MARGIN
            )
        )

        return self.token

    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.get_token()}"
        }


tokens = TokenManager()


def fetch_departures(
    airport_icao: str,
    begin: int,
    end: int
) -> list[dict]:

    airport_icao = airport_icao.strip().upper()

    if not airport_icao:
        raise ValueError(
            "Airport ICAO code cannot be empty."
        )

    if begin >= end:
        raise ValueError(
            "begin must be earlier than end."
        )

    # OpenSky allows airport flight queries
    # covering at most two days.
    if end - begin > 2 * 24 * 60 * 60:
        raise ValueError(
            "OpenSky departure requests cannot "
            "cover more than two days."
        )

    params = {
        "airport": airport_icao,
        "begin": begin,
        "end": end,
    }

    try:
        response = requests.get(
            f"{BASE_URL}/flights/departure",
            params=params,
            headers=tokens.headers(),
            timeout=30,
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"OpenSky request failed: {error}"
        ) from error

    if response.status_code == 404:
        return []

    if response.status_code == 429:
        raise RuntimeError(
            "OpenSky API rate limit exceeded."
        )

    if not response.ok:
        raise RuntimeError(
            f"OpenSky API returned "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    if not isinstance(data, list):
        raise RuntimeError(
            f"Unexpected OpenSky response: {data}"
        )

    return data