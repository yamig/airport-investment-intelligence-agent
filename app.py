import json
import re

import streamlit as st

from agent.agent import run_agent


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def clean_text_for_speech(text: str) -> str:
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    return text


def add_speak_button(text: str, button_id: str):
    clean_text = clean_text_for_speech(text)
    js_text = json.dumps(clean_text)

    st.html(
        f"""
        <button
            id="{button_id}"
            onclick="speak_{button_id}()"
            style="
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px 12px;
                background: white;
                cursor: pointer;
                font-size: 14px;
            "
        >
            🔊 Read answer aloud
        </button>

        <button
            onclick="stop_{button_id}()"
            style="
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px 12px;
                background: white;
                cursor: pointer;
                font-size: 14px;
                margin-left: 5px;
            "
        >
            ⏹ Stop
        </button>

        <script>
            function speak_{button_id}() {{
                window.speechSynthesis.cancel();

                const text = {js_text};

                const utterance =
                    new SpeechSynthesisUtterance(text);

                utterance.lang = "en-US";
                utterance.rate = 1.0;

                window.speechSynthesis.speak(utterance);
            }}

            function stop_{button_id}() {{
                window.speechSynthesis.cancel();
            }}
        </script>
        """,
        unsafe_allow_javascript=True,
    )


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Airport Investment Intelligence Agent",
    page_icon="✈️",
)

st.title("✈️ Airport Investment Intelligence Agent")

st.caption(
    "Analyze airport traffic, capacity, demand, "
    "and investment opportunities."
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_history" not in st.session_state:
    st.session_state.agent_history = []


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":
            add_speak_button(
                message["content"],
                f"speak_{index}",
            )


# --------------------------------------------------
# Text input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about US airports..."
)


# --------------------------------------------------
# Send question to agent
# --------------------------------------------------

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing airport data..."):

            answer, updated_history = run_agent(
                question=question,
                history=st.session_state.agent_history,
                return_history=True,
            )

        st.markdown(answer)

        add_speak_button(
            answer,
            "latest_answer",
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })

    st.session_state.agent_history = updated_history