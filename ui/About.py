# lightning run app ui/app.py
# streamlit run ui/About.py

import lai_components.lpa_settings as lpa
from lai_components.hydra_utils import read_hydra_config_from_file
from lightning_app.utilities.state import AppState
import streamlit as st
import copy

import ui.ui_about
import ui.select_config
import ui.ui_data
import ui.ui_train
import ui.ui_evaluate
import ui.hydra_run_out

# refer to https://docs.streamlit.io/library/get-started/multipage-apps

name = "myapp"
menu = ["About", "Configure", "Data", "Train", "Evaluate", "Annotate", "Out"]

def on_menu_click(*args, **kwargs):
  st.session_state[name+"Menu"] = kwargs["key"]

def my_menu(key, title="About"):
  st.subheader(title)
  for m in menu:
    st.button(m,on_click=on_menu_click, key=key+m, kwargs={'key':key+m})

def run(state:AppState = None):
  """ state = Lightning AppState if call from Lightning App"""

  if not(lpa.app_config in st.session_state):
    st.session_state[lpa.app_config] = {}
    if state:
      st.session_state[lpa.app_config]['default'] = state.session_state[lpa.app_config]['default']
      st.session_state[lpa.app_config]['current'] = state.session_state[lpa.app_config]['current']
      st.session_state[lpa.app_config]['target']  = state.session_state[lpa.app_config]['target']
    else:  
      st.session_state[lpa.app_config]['default'] = copy.deepcopy(lpa.app_config_default)
      st.session_state[lpa.app_config]['current'] = copy.deepcopy(lpa.app_config_default)
      st.session_state[lpa.app_config]['target']  = copy.deepcopy(lpa.app_config_default)

  if not(lpa.hydra_config in st.session_state):
    st.session_state[lpa.hydra_config] = {}
    if state:
      st.session_state[lpa.hydra_config]['default'] = state.session_state[lpa.hydra_config]['default']
      st.session_state[lpa.hydra_config]['current'] = state.session_state[lpa.hydra_config]['current']
      st.session_state[lpa.hydra_config]['target']  = state.session_state[lpa.hydra_config]['target']
    else:  
      cfg_nested, cfg_flat = read_hydra_config_from_file()
      st.session_state[lpa.hydra_config]['default'] = copy.deepcopy(cfg_flat)
      st.session_state[lpa.hydra_config]['current'] = copy.deepcopy(cfg_flat)
      st.session_state[lpa.hydra_config]['target']  = copy.deepcopy(cfg_flat)

  st.set_page_config(
      page_title="Lightning Pose App",
      layout="wide",
      initial_sidebar_state="collapsed",
    )

  if not(name+"Menu" in st.session_state):
    st.session_state[name+"Menu"] = ""

  with st.sidebar:
    my_menu(name)

  if st.session_state[name+"Menu"] == name+"Train":
    ui.ui_train.run("../lightning_pose")
  elif st.session_state[name+"Menu"] == name+"Configure":
    ui.select_config.run(st=st, state=state)
  elif st.session_state[name+"Menu"] == name+"Data":
   ui.ui_data.run("../lightning_pose")    
  elif st.session_state[name+"Menu"] == name+"Evaluate":
    ui.ui_evaluate.run("../lightning_pose")    
  elif st.session_state[name+"Menu"] == name+"Annotate":
    st.write("Annotate stuff")
  elif st.session_state[name+"Menu"] == name+"Out":
    ui.hydra_run_out.run(st=st, state=state)
  else:
    ui.ui_about.run(st=st, state=state)



if __name__ == "__main__":
  run()