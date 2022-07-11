import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
     page_title="Tensorboard",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="collapsed",
)

# embed streamlit docs in a streamlit app
components.iframe("http://localhost:6006/",height=1024, scrolling=True)
print("tensorboard)")