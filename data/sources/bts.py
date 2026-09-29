import os
import requests


BASE_URL = (
    "https://data.transportation.gov/"
    "api/v3/views/r495-tyji/query.json"
)


def fetch_bts_data(
    query: str,
    page_size: int = 5000
) -> list[dict]:

    if not query.strip():
        raise ValueError("BTS query cannot be empty.")

    all_data = []
    page_number = 1

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    app_token = os.getenv("SOCRATA_APP_TOKEN")

    if app_token:
        headers["X-App-Token"] = app_token

    while True:

        body = {
            "query": query,
            "page": {
                "pageNumber": page_number,
                "pageSize": page_size
            },
            "includeSynthetic": False
        }

        try:
            response = requests.post(
                BASE_URL,
                json=body,
                headers=headers,
                timeout=30
            )

            if not response.ok:
                raise RuntimeError(
                    f"BTS API returned {response.status_code}: "
                    f"{response.text}"
                )

            data = response.json()

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"BTS API request failed: {error}"
            ) from error

        if not isinstance(data, list):
            raise RuntimeError(
                f"Unexpected BTS response: {data}"
            )

        all_data.extend(data)

        if len(data) < page_size:
            break

        page_number += 1

    return all_data