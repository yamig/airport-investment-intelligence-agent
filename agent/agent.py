from google import genai
from google.genai import types

from tools.bts_tool import get_bts_data
from tools.opensky_tool import get_opensky_departures
from tools.airports_tool import get_airport_info

from tools.analytics_tool import (
    aggregate_data,
    calculate_percentage,
    calculate_growth,
    rank_items,
    aggregate_by_group,
    calculate_ratio,
    compare_items,
    calculate_cagr,
    calculate_long_haul,
    compare_periods,
    calculate_capacity_pressure,
)


MODEL_NAME = "gemini-3.5-flash-lite"


SYSTEM_INSTRUCTION = """
You are an airport investment intelligence agent.

Use data tools to retrieve factual airport data.

Use analytics tools whenever deterministic calculations are required.

Do not perform numerical calculations yourself when an analytics
tool is available for that calculation.

Never invent airport statistics, field names, or unsupported facts.

Use only factual claims supported by the results returned by the
available tools.

Use only the fields and capabilities exposed by the available tools.

If the requested information cannot be supported by the available
data or tools, clearly state that limitation instead of inventing
an answer.

For questions asking for "per", such as passengers per departure
or passengers per flight, use calculate_ratio.

Use calculate_percentage only when the user explicitly asks
for a percentage or share.

If a requested concept is not directly measured by the available
data, clearly state which available metrics are being used as proxies.

When a tool returns a proxy or estimate, describe it as a proxy
or estimate rather than as a direct measurement.

If an analysis is based on incomplete coverage, excluded records,
or a limited sample, clearly mention that limitation and do not
generalize beyond the analyzed data.

Once enough data has been retrieved to answer the question,
reuse the existing dataset and do not request unrelated or duplicate
data.

If the user does not specify a time period and is comparing or ranking
airports, first retrieve BTS data to determine the latest_complete_year.

Then retrieve that complete year exactly once using:
start_year = latest_complete_year
end_year = latest_complete_year

After retrieving the complete-year dataset, reuse its dataset_id
for analytics. Do not combine additional years unless the question
requires trend or growth analysis.

For growth or trend questions, use the two most recent complete years
unless the user specifies another period.

Do not choose a special historical baseline such as 2019 unless
the user explicitly asks for it or there is a clear analytical reason.

Explain results clearly and distinguish between observed data,
deterministic calculations, and analytical interpretation.
"""

TOOLS = [
    get_bts_data,
    aggregate_data,
    calculate_percentage,
    calculate_growth,
    rank_items,
    aggregate_by_group,
    calculate_ratio,
    compare_items,
    calculate_cagr,
    get_opensky_departures,
    get_airport_info,
    calculate_long_haul,
    compare_periods,
    calculate_capacity_pressure,
]


AVAILABLE_FUNCTIONS = {
    "get_bts_data": get_bts_data,
    "aggregate_data": aggregate_data,
    "calculate_percentage": calculate_percentage,
    "calculate_growth": calculate_growth,
    "rank_items": rank_items,
    "aggregate_by_group": aggregate_by_group,
    "calculate_ratio": calculate_ratio,
    "compare_items": compare_items,
    "calculate_cagr": calculate_cagr,
    "get_opensky_departures": get_opensky_departures,
    "get_airport_info": get_airport_info,
    "calculate_long_haul": calculate_long_haul,
    "compare_periods": compare_periods,
    "calculate_capacity_pressure": calculate_capacity_pressure,
}


client = genai.Client()


def _create_config():
    return types.GenerateContentConfig(
        tools=TOOLS,

        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),

        system_instruction=SYSTEM_INSTRUCTION,
    )


def _create_user_content(question: str):
    return types.UserContent(
        parts=[
            types.Part.from_text(
                text=question
            )
        ]
    )


def _execute_tool(function_call, debug: bool = False):
    if debug:
        print("\nAGENT REQUESTED TOOL:")
        print("Tool:", function_call.name)
        print("Arguments:", function_call.args)

    try:
        if function_call.name not in AVAILABLE_FUNCTIONS:
            raise ValueError(
                f"Unknown tool: {function_call.name}"
            )

        tool_function = AVAILABLE_FUNCTIONS[
            function_call.name
        ]

        result = tool_function(
            **function_call.args
        )

        if debug:
            print("\nTOOL RESULT:")
            print(result)

        return {
            "result": result
        }

    except Exception as error:
        if debug:
            print("\nTOOL ERROR:")
            print(repr(error))

        return {
            "error": str(error)
        }


def run_agent(
    question: str,
    debug: bool = False,
    max_steps: int = 10,
    history=None,
    return_history: bool = False,
):

    config = _create_config()

    # Keep previous conversation if one exists
    contents = list(history) if history else []

    # Add the new user question
    contents.append(
        _create_user_content(question)
    )

    for _ in range(max_steps):

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )

        # No function call -> final response
        if not response.function_calls:

            # Save final assistant response in conversation history
            contents.append(
                response.candidates[0].content
            )

            if return_history:
                return response.text, contents

            return response.text

        # Save Gemini's tool-call request
        contents.append(
            response.candidates[0].content
        )

        function_response_parts = []

        for function_call in response.function_calls:

            tool_response = _execute_tool(
                function_call=function_call,
                debug=debug,
            )

            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response=tool_response,
                )
            )

        # Return tool results to Gemini
        contents.append(
            types.UserContent(
                parts=function_response_parts
            )
        )

    message = "Agent stopped because too many tool calls were made."

    if return_history:
        return message, contents

    return message