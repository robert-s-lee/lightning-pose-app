import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
     page_title="Fiftyone",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="collapsed",
)

# embed streamlit docs in a streamlit app
components.iframe("http://localhost:5151/",height=1024, scrolling=True)
print("tensorboard)")