import logging
import re
import time

from streamlit_pills import pills

import streamlit as st
from esynergy_open_rag.config import chain
from esynergy_open_rag.streamlit_components.sidebar_functions import update_sidebar
from esynergy_open_rag.streamlit_components.streamlit_support import (
    get_button_links,
    start_countdown,
)

css = """
<style>
    [data-testid="stSidebar"]{
        min-width: 0px;
        max-width: 700px;
    }
</style>
"""
collector = None

widget_id = (id for id in range(1, 10000))


def chat_here(placeholder):
    """
    Main function to manage the chat interface.

    Args:
        placeholder: A placeholder container to update the sidebar.

    Returns:
        None
    """
    # Display chat messages from history on app rerun
    logging.debug(st.session_state.messages)

    for n, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and n >= 1:
                feedback_key = f"feedback_{int(n / 2)}"

                if feedback_key not in st.session_state:
                    st.session_state[feedback_key] = None

            if "button_source" in message and len(list(message["button_source"].keys())) > 1:
                with st.expander("Click to view Sources", expanded=False):
                    selected = pills(
                        "Source",
                        list(message["button_source"].keys()),
                        key=next(widget_id),
                        index=None,
                    )
                    if selected:
                        placeholder.empty()
                        update_sidebar(selected, message=message, placeholder=placeholder)

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Fetching the Response for your Query from the AI Engine..."):
                try:
                    response = chain.invoke(prompt)
                except Exception:
                    response = {"answer": "Sorry, I didn't get that. Please try again."}
                    message_placeholder.markdown(response["answer"])
                    start_countdown()
                    st.stop()
            try:
                assistant_response = response["answer"]
            except Exception as e:
                print(e)
                assistant_response = "Sorry, I didn't get that. Please try again."
            st.session_state.messages.append({"role": "user", "content": prompt})
            for chunk in re.split(r"(\s+)", assistant_response):
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(f"{full_response}")
            button_links = {}
            # count = 0
            try:
                button_links = get_button_links(response)
                # print(f"button_links {button_links}")
                # link_markdown = create_markdown(button_links)

                # pills("Source", list(button_links.keys()),key=next(widget_id))
                # selected_current = None
                # selected_current = pills("Source", list(button_links.keys()), key=next(widget_id))
                # update_sidebar(selected=selected_current,
                #                placeholder=placeholder)
            except Exception as e:
                print(e)
                st.markdown("*No source documents found*")

        st.session_state.history.append({"Human": prompt, "AI": assistant_response})
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
                "prompt": prompt,
                "button_source": button_links,
            }
        )
        st.rerun()

    footer = """<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    }
    </style>
    """
    st.markdown(footer, unsafe_allow_html=True)
