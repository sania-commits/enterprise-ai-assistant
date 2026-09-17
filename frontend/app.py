import os
import uuid

import httpx
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="centered",
)


# --------------------------------------------------
# SESSION INITIALIZATION
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 Enterprise AI Assistant")

st.caption(
    "Ask questions about company policies, "
    "use built-in tools, or ask general questions."
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("Conversation")

    if st.button("New conversation"):
        st.session_state.thread_id = str(
            uuid.uuid4()
        )

        st.session_state.messages = []

        st.rerun()

    st.caption(
        f"Thread ID: "
        f"{st.session_state.thread_id}"
    )


# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message.get("route"):
            st.caption(
                f"Route: {message['route']}"
            )

        if message.get("sources"):

            with st.expander("Sources"):

                for source in message["sources"]:
                    st.write(source)


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask the enterprise assistant..."
)


# --------------------------------------------------
# PROCESS USER QUESTION
# --------------------------------------------------

if question:

    # Remove unnecessary spaces
    question = question.strip()

    # Frontend validation
    if len(question) < 3:
        st.warning(
            "Please enter a question with at least 3 characters."
        )

        st.stop()

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------
    # CALL FASTAPI BACKEND
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = httpx.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question,
                        "thread_id": (
                            st.session_state.thread_id
                        ),
                    },
                    timeout=60.0,
                )

                response.raise_for_status()

                data = response.json()

                answer = data["answer"]
                route = data["route"]
                sources = data["sources"]

                # --------------------------------------
                # DISPLAY ANSWER
                # --------------------------------------

                st.markdown(answer)

                st.caption(
                    f"Route: {route}"
                )

                # --------------------------------------
                # DISPLAY RAG SOURCES
                # --------------------------------------

                if sources:

                    with st.expander("Sources"):

                        for source in sources:
                            st.write(source)

                # --------------------------------------
                # SAVE ASSISTANT MESSAGE
                # --------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "route": route,
                        "sources": sources,
                    }
                )

            # ------------------------------------------
            # HTTP / BACKEND ERROR HANDLING
            # ------------------------------------------

                        except httpx.HTTPStatusError as error:
                try:
                    detail = error.response.json().get(
                        "detail",
                        "The AI service returned an error.",
                    )
                except ValueError:
                    detail = (
                        "The AI service returned an error."
                    )

                st.error(detail)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": detail,
                    }
                )

            except httpx.RequestError:
                error_message = (
                    "Unable to connect to the AI service. "
                    "Please check that the backend is running."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )