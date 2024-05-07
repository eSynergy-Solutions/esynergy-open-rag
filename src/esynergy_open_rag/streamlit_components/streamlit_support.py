import hmac
import time
from urllib.parse import unquote

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_remote_ip() -> str | None:
    """
    Get the remote IP address of the Streamlit session.

    Returns:
        str | None: The remote IP address if available, else None.
    """

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        runtime = st.runtime
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception:
        return None

    return session_info.request.remote_ip


def check_password():
    """
    Check if the user-entered password matches the secret password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def create_markdown(dt) -> str:
    """
    Create Markdown text from a dictionary.

    Args:
        dt (dict): Dictionary containing source information.

    Returns:
        str: Markdown text containing source links.
    """
    markdown_text = ""
    for key in dt:
        url = dt[key]["source"]
        markdown_text += f"- [{key}]({url}) \n"
    return markdown_text


def _submit_feedback(user_response, emoji=None):
    """
    Submit user feedback and display a toast message.

    Args:
        user_response (_type_): The user's feedback.
        emoji (str, optional): Emoji to display in the toast message. Defaults to None.

    Returns:
        dict: Updated user response with metadata.
    """
    st.toast(f"Feedback submitted: {user_response}", icon=emoji)
    return user_response.update({"some metadata": 123})


def set_header(col1_title):
    """
    Set the header for the Streamlit app.

    Args:
        col1_title: The title for the header column.

    Returns:
        None
    """
    with col1_title:
        st.image("https://esynergy.co.uk/wp-content/themes/esynergy/images/eSynergy-Logo-1.png")
    # with col2_title:
    #     st.title("CoPilot")

    with st.expander("User Information", expanded=True):
        st.markdown("""##### GenAI App MVP Overview:""")
        st.markdown(
            "With this app, you can: **Search, summarise, and generate documents** (PDF, Word, and PowerPoint) "
            "from our bid repository."
        )
        st.markdown("Example query:")
        st.markdown("> Give me a summary of the Northern Trust Data Mesh    case study.")
        st.markdown("> Create a proposal similar to Utmost with these    specific details.")

        st.markdown("        *Please note: Chat history is not stored; each query is treated as a new session.* ")


def get_email() -> bool:
    """
    Get the user's email address and validate it.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re

    import streamlit as st

    regex = re.compile(r"^[7896]\d{9}$")

    def is_valid(input_email):
        if re.fullmatch(regex, input_email):
            return True
        else:
            return False

    with st.expander("User Information", expanded=True):
        with st.form("email_form"):
            email = st.text_input("Enter the Email")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit Email & Try Chatbot")
            if submitted:
                if is_valid(email):
                    # st.write("Valid Email")
                    # st.write("input_email", input_email)
                    st.session_state.authentication_status = True
                    st.session_state.user_id = str(email)
                    st.snow()
                    time.sleep(5)
                    st.rerun()
                    return st.session_state.authentication_status
                else:
                    st.session_state.authentication_status = False
                    st.error("Invalid Email", icon="🚨")
                    # st.write("Invalid Email")
    return st.session_state.authentication_status


def get_button_links(response) -> dict:
    """
    Extract button links from the response data.

    Args:
        response (_type_): The response data containing context information.

    Returns:
        dict: Dictionary containing button links and associated content.
    """
    button_links = {}
    counbt = 0
    for doc in response["context"]:
        # print(doc)
        data = dict(doc)
        if len(data["page_content"]):
            # print(data)
            try:
                title = unquote(data["metadata"]["title"])
            except Exception:
                counbt = 1 + counbt
                title = "Excerpt:" + str(counbt)
            # source=data["metadata"]["source"]
            # content=unquote(data["page_content"])
            if title not in button_links:
                button_links[title] = {}
                button_links[title]["source"] = ""
                button_links[title]["content"] = []
            button_links[title]["source"] = str(data["metadata"]["source"]).replace("s3://data-rag/", "")
            button_links[title]["content"].append(unquote(data["page_content"]))
        else:
            continue
    return button_links


def start_countdown(n=60):
    """
    Display a countdown message for a specified duration.

    Args:
        n (int, optional): The duration of the countdown in seconds. Defaults to 60.

    Returns:
        None
    """
    st.markdown(
        """ ## We are facing High Demand at the moment.

    Currently we are at free tier,
    Please wait untill the API is back live.
    If you feel this tool is useful, please contact us:

    Thank you for your patience Please Wait for 60 seconds."""
    )
    ph = st.empty()
    for secs in range(n, 0, -1):
        mm, ss = secs // 60, secs % 60
        ph.metric("", f"{mm: 02d} : {ss: 02d}")
        time.sleep(1)


def disclaimer():
    """
    Display a disclaimer message.

    Returns:
        None
    """
    st.markdown(
        """
        **This Copilot is in beta!** While it can help with studying, the information might not always be perfect.
        We recommend using it alongside other resources for the best results.\n
        **Basically:** We're still learning, so double-check everything and use it as a study buddy, not your only
        teacher. Good luck with your studies!
    """
    )
    with st.expander("Disclaimer", expanded=False):
        st.markdown(
            """
        The information provided by the Sales Copilot is for general informational and educational purposes only.
        All information provided by the Copilot is in good faith; however, we make no representation or warranty of
        any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability, or
        completeness of any information provided by the Copilot. Under no circumstance shall we have any liability
        to you for any loss or damage of any kind incurred as a result of the use of the Copilot or reliance on any
        information provided by it. Your use of the Copilot and your reliance on any information provided by it
        is solely at your own risk.
        """
        )
