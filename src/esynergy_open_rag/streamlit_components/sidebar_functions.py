import streamlit as st


def update_sidebar(selected: str, message: dict, placeholder=None):
    """
    Update the Streamlit sidebar with selected source information.

    Args:
        selected (str): The selected source.
        message (dict): The message containing source information.
        placeholder (streamlit.container._container_widget.WidgetsCollection): The placeholder container for the sidebar.

    Returns:
        None
    """
    if placeholder is None:
        placeholder = st.empty()
    with st.sidebar:
        with placeholder.container():
            st.markdown("## Selected Source")
            st.markdown(selected)
            # source = message["button_source"][selected]["source"]
            st.markdown("## Source Link")
            # st.markdown(source)
            st.markdown("## Source Content")
            # enumerate on message["button_source"][selected]["content"] and print document number and content
            for i, content in enumerate(message["button_source"][selected]["content"]):
                st.markdown(f"### Excerpt {i + 1}")
                st.markdown(content)
