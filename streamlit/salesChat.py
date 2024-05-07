import os
import re

# https://www.credo.ai/gen-ai-ops-landscape
import time

from sidebar_functions import update_sidebar
from streamlit_pills import pills
from streamlit_support import (
    _submit_feedback,
    check_password,
    create_markdown,
    get_button_links,
    get_remote_ip,
    set_header,
)
from trubrics.integrations.streamlit import FeedbackCollector

import streamlit as st
from esynergy_open_rag.config import chain

# from trubrics_utils import trubrics_config, trubrics_successful_feedback


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = None
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0

try:
    collector = FeedbackCollector(
        email=os.getenv("STREAMLIT_FEEDBACK_EMAIL"),
        password=os.getenv("STREAMLIT_FEEDBACK_PASSWORD"),
        project="default",
    )
except Exception as e:
    print(e)
    collector = None

widget_id = (id for id in range(1, 10000))

# enter the lamda url here
# url = "https://0rwpep6d65.execute-api.us-east-1.amazonaws.com/Prod/get-response"
# url = "http://0.0.0.0:8001/get-response"
url = os.getenv("STREAMLIT_URL")

# print(response.text)

# image = Image.open('https://esynergy.co.uk/wp-content/themes/esynergy/images/eSynergy-Logo-1.png')
st.set_page_config(
    page_title="Esynergy CoPilot",
    page_icon="https://esynergy.co.uk/wp-content/uploads/2022/02/cropped-fav-icon-32x32.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

css = """
<style>
    [data-testid="stSidebar"]{
        min-width: 0px;
        max-width: 700px;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

col1_title, col2_title = st.columns(2)

set_header(col1_title)

with st.sidebar:
    st.markdown("## Reference Documents")
    placeholder = st.empty()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = str(get_remote_ip())

if "history" not in st.session_state:
    st.session_state.history = [{"Human": "", "AI": ""}]

# Display chat messages from history on app rerun
# print(st.session_state.messages)

feedback_kwargs = {
    "feedback_type": "thumbs",
    "optional_text_label": "Please provide extra information",
    "on_submit": _submit_feedback,
}

for n, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and n >= 1:
            feedback_key = f"feedback_{int(n / 2)}"

            if feedback_key not in st.session_state:
                st.session_state[feedback_key] = None

            user_feedback = collector.st_feedback(
                component="streamlitfeedback",
                feedback_type="thumbs",
                open_feedback_label="[Optional] Provide additional feedback",
                model=st.session_state.logged_prompt.config_model.model,
                prompt_id=st.session_state.logged_prompt.id,
                key=feedback_key,
                align="flex-end",
                user_id=st.session_state.user_id,
                metadata={"prompt": message["prompt"], "response": message["content"]},
            )
        if "button_source" in message and len(list(message["button_source"].keys())) > 1:
            selected = None
            selected = pills(
                "Source",
                list(message["button_source"].keys()),
                key=next(widget_id),
                index=None,
            )
            if selected:
                placeholder.empty()
                # ToDo: Add the relevant function
                update_sidebar(selected, message, placeholder)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # payload = json.dumps({
        #     "message": str(prompt),
        #     "data": st.session_state.history
        # })
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': st.secrets["key"]
        # }
        with st.spinner("Fetching the Response for your Query from the AI Engine..."):
            # response = requests.request("POST",
            #                             url,
            #                             headers=headers,
            #                             data=payload)
            response = chain.invoke(prompt)
            # print(response.json())
        try:
            assistant_response = response["answer"]
        except Exception:
            # st.markdown("Sorry, I didn't get that. Please try again.")
            assistant_response = "Sorry, I didn't get that. Please try again."
        if collector:
            st.session_state.logged_prompt = collector.log_prompt(
                config_model={"model": "ClaudeV2_S#_Sharepoint"},
                prompt=str(prompt),
                generation=assistant_response,
                user_id=st.session_state.user_id,
            )

        for chunk in re.split(r"(\s+)", assistant_response):
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(f"{full_response}")
        button_links = {}
        counbt = 0
        try:
            button_links = get_button_links(response)
            link_markdown = create_markdown(button_links)

            # pills("Source", list(button_links.keys()),key=next(widget_id))
            selected_current = None

            selected_current = pills("Source", list(button_links.keys()), key=next(widget_id))
            # update_sidebar(selected=selected_current,
            #                source=Source,
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
