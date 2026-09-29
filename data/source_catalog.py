DATA_SOURCES = {
    "bts_summary": {
        "name": "AFF - T100 Segment Summary By Origin Airport",

        "description": (
            "BTS airport-level T-100 summary data containing traffic, "
            "passenger, seat, load factor, distance, payload, freight, "
            "mail, domestic, outbound international, and inbound "
            "international metrics."
        ),

        "fields": {
            # Airport and time identification
            "origin_airport_id": {
                "description": "ORIGIN_AIRPORT_ID",
                "type": "text",
            },

            "year": {
                "description": "Year",
                "type": "text",
            },

            "reporting_month": {
                "description": "Date",
                "type": "floating_timestamp",
            },

            "origin_airport_code": {
                "description": "Origin Airport Code",
                "type": "text",
            },

            # Total traffic
            "total_departures": {
                "description": "Total Departures",
                "type": "number",
            },

            "total_passengers": {
                "description": "Total Passengers",
                "type": "number",
            },

            "total_seats": {
                "description": "Total Seats",
                "type": "number",
            },

            "total_load_factor": {
                "description": "Total Load Factor (%)",
                "type": "number",
            },

            "total_passengers_flight": {
                "description": "Total Passengers/Flight",
                "type": "number",
            },

            "total_seats_flight": {
                "description": "Total Seats/Flight",
                "type": "number",
            },

            "total_distance_flight_sm": {
                "description": "Total Distance/Flight (sm)",
                "type": "number",
            },

            "total_distance_passenger": {
                "description": "Total Distance/Passenger (sm)",
                "type": "number",
            },

            "total_payload_lbs": {
                "description": "Total Payload (lbs)",
                "type": "number",
            },

            "total_freight_lbs": {
                "description": "Total Freight (lbs)",
                "type": "number",
            },

            "total_mail_lbs": {
                "description": "Total Mail (lbs)",
                "type": "number",
            },

            # Domestic traffic
            "domestic_departures": {
                "description": "Domestic Departures",
                "type": "number",
            },

            "domestic_passengers": {
                "description": "Domestic Passengers",
                "type": "number",
            },

            "domestic_seats": {
                "description": "Domestic Seats",
                "type": "number",
            },

            "domestic_load_factor": {
                "description": "Domestic Load Factor (%)",
                "type": "number",
            },

            "domestic_passengers_flight": {
                "description": "Domestic Passengers/Flight",
                "type": "number",
            },

            "domestic_seats_flight": {
                "description": "Domestic Seats/Flight",
                "type": "number",
            },

            "domestic_distance_flight": {
                "description": "Domestic Distance/Flight (sm)",
                "type": "number",
            },

            "domestic_distance_passenger": {
                "description": "Domestic Distance/Passenger (sm)",
                "type": "number",
            },

            "domestic_payload_lbs": {
                "description": "Domestic Payload (lbs)",
                "type": "number",
            },

            "domestic_freight_lbs": {
                "description": "Domestic Freight (lbs)",
                "type": "number",
            },

            "domestic_mail_lbs": {
                "description": "Domestic Mail (lbs)",
                "type": "number",
            },

            # Outbound international traffic
            "outbound_international": {
                "description": "Outbound International Departures",
                "type": "number",
            },

            "outbound_international_1": {
                "description": "Outbound International Passengers",
                "type": "number",
            },

            "outbound_international_seats": {
                "description": "Outbound International Seats",
                "type": "number",
            },

            "outbound_international_load": {
                "description": "Outbound International Load Factor (%)",
                "type": "number",
            },

            "outbound_international_2": {
                "description": "Outbound International Passengers/Flight",
                "type": "number",
            },

            "outbound_international_seats_1": {
                "description": "Outbound International Seats/Flight",
                "type": "number",
            },

            "outbound_international_3": {
                "description": "Outbound International Distance/Flight (sm)",
                "type": "number",
            },

            "outbound_international_4": {
                "description": "Outbound International Distance/Passenger (sm)",
                "type": "number",
            },

            "outbound_international_payload": {
                "description": "Outbound International Payload (lbs)",
                "type": "number",
            },

            "outbound_international_freight": {
                "description": "Outbound International Freight (lbs)",
                "type": "number",
            },

            "outbound_international_mail": {
                "description": "Outbound International Mail (lbs)",
                "type": "number",
            },

            # Inbound international traffic
            "inbound_international": {
                "description": "Inbound International Departures",
                "type": "number",
            },

            "inbound_international_1": {
                "description": "Inbound International Passengers",
                "type": "number",
            },

            "inbound_international_seats": {
                "description": "Inbound International Seats",
                "type": "number",
            },

            "inbound_international_load": {
                "description": "Inbound International Load Factor (%)",
                "type": "number",
            },

            "inbound_international_2": {
                "description": "Inbound International Passengers/Flight",
                "type": "number",
            },

            "inbound_international_seats_1": {
                "description": "Inbound International Seats/Flight",
                "type": "number",
            },

            "inbound_international_distance": {
                "description": "Inbound International Distance/Flight (sm)",
                "type": "number",
            },

            "inbound_international_distance_1": {
                "description": "Inbound International Distance/Passenger (sm)",
                "type": "number",
            },

            "inbound_international_payload": {
                "description": "Inbound International Payload (lbs)",
                "type": "number",
            },

            "inbound_international_freight": {
                "description": "Inbound International Freight (lbs)",
                "type": "number",
            },

            "inbound_international_mail": {
                "description": "Inbound International Mail (lbs)",
                "type": "number",
            },

            # Airport location/name
            "origin_city_name": {
                "description": "Origin City Name",
                "type": "text",
            },

            "origin_airport_name": {
                "description": "Origin Airport Name",
                "type": "text",
            },
        },
    }
}