# https://www.credo.ai/gen-ai-ops-landscape
import logging

import streamlit as st

from esynergy_open_rag.chat import chat_here
from esynergy_open_rag.streamlit_components.streamlit_support import (
    disclaimer,
    get_email,
    set_header,
)

if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = None
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = False
if "user_id" not in st.session_state:
    st.session_state.user_id = "test"

css = """
<style>
    [data-testid="stSidebar"]{
        min-width: 100px;
        max-width: 120px;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

if 'authentication_status' in st.session_state:

    if not st.session_state.authentication_status:
        disclaimer()
        status = get_email()
        st.image("Banners.png")

        if not st.session_state.authentication_status:
            st.stop()
    else:
        logging.info("Authenticated {st.session_state.authentication_status}")

        col1_title, col2_title = st.columns(2)
        set_header(col1_title)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "history" not in st.session_state:
            st.session_state.history = [{"Human": "", "AI": ""}]
        with st.sidebar:
            # st.markdown("## Reference Documents")
            placeholder = st.empty()

        chat_here(placeholder)
