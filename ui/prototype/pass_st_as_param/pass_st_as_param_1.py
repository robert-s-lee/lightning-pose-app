import streamlit as st
from lightning_app.utilities.state import AppState
import pass_st_as_param_2

def render(state:AppState = None):
  if not('config' in st.session_state):
    st.session_state['config'] = 'here'
  st.write("at 1")
  pass_st_as_param_2.render(state=state)

if __name__ == "__main__":
  render()