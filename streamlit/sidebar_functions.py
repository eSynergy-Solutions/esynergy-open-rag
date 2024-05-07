import streamlit as st


def update_sidebar(selected, message, placeholder):
    with st.sidebar:
        with placeholder.container():
            st.markdown("## Selected Source")
            st.markdown(selected)
            source = message["button_source"][selected]["source"]
            st.markdown("## Source Link")
            # st.markdown(source)
            st.markdown(source.replace("s3://data-rag/", ""))
            st.markdown("## Source Content")
            # enumerate on message["button_source"][selected]["content"] and print document number and content
            for i, content in enumerate(message["button_source"][selected]["content"]):
                st.markdown(f"### Excerpt {i + 1}")
                st.markdown(content)
