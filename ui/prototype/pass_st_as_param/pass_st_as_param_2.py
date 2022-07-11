import streamlit as st
from lightning_app.utilities.state import AppState

def render(state:AppState = None):
  st.write(st.session_state['config'])
  if state:
    state.pass_st_as_param_2 = "here"

if __name__ == "__main__":
  print("main")
  render()