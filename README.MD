# Airport Investment Intelligence Agent

An AI-powered analytical assistant for exploring airport traffic, capacity, utilization, and modernization opportunities in the United States.

The system combines public aviation data, deterministic Python analytics, and an LLM-based agent that dynamically selects data sources and analytical tools according to the user's question.

## Features

- Natural-language airport analysis
- Public aviation data retrieval
- Deterministic ranking and comparison
- Historical trend and capacity analysis
- Multi-step tool calling
- Conversational follow-up questions
- Streamlit chat interface
- Text-to-speech playback
- Handling of incomplete reporting periods and data limitations

The system is not hard-coded around a fixed set of questions. The agent dynamically combines the available data and analytics capabilities according to the user's request.

---

## Architecture

```text
User Question
      ↓
AI Agent
      ↓
Data Tools
(BTS / OpenSky / Airport Data)
      ↓
Dataset Store
      ↓
Deterministic Analytics
      ↓
AI Agent
      ↓
Natural-Language Answer
```

The main design principle is:

**AI decides what analysis is needed; Python performs the numerical analysis; AI explains the result.**

Retrieved datasets are stored internally and referenced using a `dataset_id`, instead of sending large raw datasets directly to the LLM.

---

## Data Sources

### Bureau of Transportation Statistics (BTS)

Used for airport-level historical traffic and capacity data, including:

- Passengers
- Departures
- Seats
- Load factor
- Domestic and international traffic
- Passengers per flight
- Seats per flight

A Socrata application token can optionally be provided to improve API request limits.

### OpenSky Network

Used for flight-level departure information.

The current implementation uses OpenSky OAuth2 authentication and therefore requires an OpenSky API Client ID and Client Secret.

### Airport Information

Airport metadata and coordinates are retrieved from the Aviation Weather Center Data API.

No additional API credentials are required for this data source in the current implementation.

---

## Deterministic Analytics

Numerical calculations are performed by Python tools instead of relying on the LLM.

Supported analytical capabilities include:

- Ranking
- Airport comparison
- Aggregation and grouping
- Ratios and percentages
- Growth calculations
- Period comparison
- CAGR
- Capacity-pressure analysis
- Geographic distance calculations
- Deterministic classification

The LLM selects the appropriate tools and interprets their results.

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## API Credentials

The project uses environment variables for API credentials.

### Required

#### Gemini

```text
GEMINI_API_KEY
```

This is required for the AI agent itself.

#### OpenSky

```text
OPENSKY_CLIENT_ID
OPENSKY_CLIENT_SECRET
```

These are required when the agent uses OpenSky flight data.

### Optional

#### BTS / Socrata

```text
SOCRATA_APP_TOKEN
```

The BTS dataset can be accessed without this token, but providing one may improve API rate limits.

### No Credentials Required

The Aviation Weather Center airport-information endpoint used by the project does not require an additional API key.

---

## Setting Credentials

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_gemini_key"
$env:OPENSKY_CLIENT_ID="your_opensky_client_id"
$env:OPENSKY_CLIENT_SECRET="your_opensky_client_secret"
```

Optional:

```powershell
$env:SOCRATA_APP_TOKEN="your_socrata_token"
```

### macOS / Linux

```bash
export GEMINI_API_KEY="your_gemini_key"
export OPENSKY_CLIENT_ID="your_opensky_client_id"
export OPENSKY_CLIENT_SECRET="your_opensky_client_secret"
```

Optional:

```bash
export SOCRATA_APP_TOKEN="your_socrata_token"
```

API credentials are not stored in the source code.

---

## Run the Application

After installing the dependencies and configuring the required credentials:

```bash
streamlit run app.py
```

The Streamlit application will open in the browser.

The user can then ask questions directly through the chat interface.

---

## Example Questions

Examples of supported analyses include:

```text
Compare passenger traffic at SFO and LAX.

How has passenger traffic at JFK changed since 2020?

Rank SFO, LAX, JFK and BOS by passenger volume.

Which airport has the highest load factor?

What percentage of flights departing Anchorage are long-haul?

Compare recent capacity trends at several airports.
```

These are examples only. The agent is based on reusable data and analytical capabilities rather than predefined question templates.

---

## Conversational Follow-Ups

Conversation history is preserved so the agent can understand follow-up questions.

For example:

```text
User:
Compare LAX and SNA.

User:
What about SFO?
```

The second question is interpreted using the context of the first.

---

## Scope and Limitations

The system relies on public aviation datasets and can only analyze information supported by the available data sources and analytical tools.

Public data may contain:

- Partial reporting periods
- Missing observations
- Incomplete flight coverage
- Missing route information

Some user concepts may not correspond directly to a field in the available datasets. In these cases, available metrics may be used as analytical indicators or proxies and should not be interpreted as direct measurements.

The system is intended as a decision-support prototype rather than a complete financial or operational airport-investment platform.

---

## Design Documentation

A separate **Design & Architecture Document** describes:

- System architecture
- Deterministic ranking and comparison methodology
- Where and how AI is used
- Key design tradeoffs
- Assumptions, uncertainty, and system scope

---

## Summary

The Airport Investment Intelligence Agent combines:

**Natural-language reasoning + public aviation data + deterministic Python analytics + conversational interaction**

The LLM determines which available capabilities are needed for a question, Python performs the numerical calculations, and the agent explains the results to the user.