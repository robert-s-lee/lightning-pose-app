import streamlit as st 
import lai_components.lpa_settings as lpa
from lai_components.hydra_utils import set_hydra_run_out
from lightning_app.utilities.state import AppState
import copy


def print_value():
  for k in st.session_state[lpa.hydra_config]:
    print(f"{lpa.hydra_config}.{k}")
    try:
      print(f"{lpa.hydra_config}.{k}=",st.session_state[lpa.hydra_config][k][lpa.hydra_run_out])
    except:
      pass  

def run(st, state:AppState = None):
  """set hydra.run.out=outputs/YY-MM-DD/HH-MM-SS"""
  
  if not (lpa.hydra_run_out in st.session_state[lpa.hydra_config]['default']):
    x = set_hydra_run_out()
    st.session_state[lpa.hydra_config]['default'][lpa.hydra_run_out] = x
    st.session_state[lpa.hydra_config]['current'][lpa.hydra_run_out] = x

  x = st.text_input("hydra.dir.out", 
    value =st.session_state[lpa.hydra_config]['current'][lpa.hydra_run_out], 
    placeholder = st.session_state[lpa.hydra_config]['default'][lpa.hydra_run_out])
  print(x)
  if x == "":
    st.error(f"{lpa.hydra_run_out} dir cannot be empty")
  else:
    st.session_state[lpa.hydra_config]['target'][lpa.hydra_run_out] = x  
    #print_value()

  y = st.button("Submit")

  if y:
    st.session_state[lpa.hydra_config]['current'][lpa.hydra_run_out] = st.session_state[lpa.hydra_config]['target'][lpa.hydra_run_out]
    st.info("saved")

if __name__ == "__main__":
  run(st)