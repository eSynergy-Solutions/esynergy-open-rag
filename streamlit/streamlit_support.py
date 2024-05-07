import hmac
import os
from urllib.parse import unquote

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_remote_ip() -> str | None:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        # runtime = ctx.env.runtime
        runtime = st.runtime
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception:
        return None

    return session_info.request.remote_ip


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""

        if hmac.compare_digest(st.session_state["password"], os.getenv("STREAMLIT_PASSWORD")):
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


def create_markdown(dt):
    markdown_text = ""
    for key in dt:
        url = dt[key]["source"]
        markdown_text += f"- [{key}]({url}) \n"
    return markdown_text


def _submit_feedback(user_response, emoji=None):
    st.toast(f"Feedback submitted: {user_response}", icon=emoji)
    return user_response.update({"some metadata": 123})


def set_header(col1_title):
    with col1_title:
        st.image("https://esynergy.co.uk/wp-content/themes/esynergy/images/eSynergy-Logo-1.png")
    # with col2_title:
    #     st.title("CoPilot")

    with st.expander("User Information", expanded=True):
        st.markdown("""##### GenAI App MVP Overview:""")
        st.markdown(
            "With this app, you can: **Search, summarise, and generate documents** (PDF, Word, and PowerPoint) from our bid repository."
        )
        st.markdown("Example query:")
        st.markdown("> Give me a summary of the Northern Trust Data Mesh    case study.")
        st.markdown("> Create a proposal similar to Utmost with these    specific details.")

        st.markdown("        *Please note: Chat history is not stored; each query is treated as a new session.* ")


def get_button_links(response):
    """_summary_

    Args:
        response (_type_): _description_

    Returns:
        _type_: _description_
    """
    button_links = {}
    counbt = 0
    for doc in response["context"]:
        data = dict(doc)

        # print(data)
        try:
            title = unquote(data["metadata"]["name"])
        except Exception:
            counbt = 1 + counbt
            title = "Excerpt:" + str(counbt)
        # source=data["metadata"]["source"]
        # content=unquote(data["page_content"])
        if title not in button_links:
            button_links[title] = {}
            button_links[title]["source"] = ""
            button_links[title]["content"] = []
        print(data["metadata"])
        button_links[title]["source"] = str(data["metadata"]["web_link"])
        button_links[title]["content"].append(unquote(data["page_content"]))

    return button_links


# def get_button_links(response):
#     """_summary_
#
#     Args:
#         response (_type_): _description_
#
#     Returns:
#         _type_: _description_
#     """
#     button_links = {}
#     counbt = 0
#     for doc in response["context"]:
#         data = dict(doc)
#         if len(data["page_content"]) > 500:
#             # print(data)
#             try:
#                 title = unquote(data["metadata"]["title"])
#             except:
#                 counbt = 1 + counbt
#                 title = "Excerpt:" + str(counbt)
#             # source=data["metadata"]["source"]
#             # content=unquote(data["page_content"])
#             if title not in button_links:
#                 button_links[title] = {}
#                 button_links[title]["source"] = ""
#                 button_links[title]["content"] = []
#             button_links[title]["source"] = str(
#                 data["metadata"]["source"]).replace("s3://data-rag/", "")
#             button_links[title]["content"].append(unquote(
#                 data["page_content"]))
#         else:
#             continue
#     return button_links
