import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
     page_title="Ex-stream-ly Cool App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
)

# embed streamlit docs in a streamlit app
components.iframe("https://docs.streamlit.io/en/latest",height=1024, scrolling=True)
print("here)")
