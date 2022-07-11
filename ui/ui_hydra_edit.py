import streamlit as st

def show_hydra_field(k, kv, keys_already_displayed,disabled=False):
  if not(k in keys_already_displayed):
    if k in kv:
      v=kv[k]
    else:
      v=""
    if not(k in st.session_state["config.yaml"]):
      st.session_state["config.yaml"][k] = ""  
    st.text_input(k,value=st.session_state["config.yaml"][k],key=k,placeholder=v,disabled=disabled)

def show_hydra_group(kv:dict, control_params, input_params, output_params, auto_params):
  keys_displayed = {}
  if not("config.yaml" in st.session_state):
    st.session_state["config.yaml"]={}
  # common controls
  with st.expander("Common Controls", expanded=True):
    for k in control_params:
      show_hydra_field(k, kv, keys_displayed)
      keys_displayed[k] = None  # input
  with st.expander("Inputs", expanded=True):
    for k in input_params:
      show_hydra_field(k, kv, keys_displayed)
      keys_displayed[k] = None
  # output
  with st.expander("Outputs", expanded=True):
    for k in output_params:
      print(k)
      show_hydra_field(k, kv, keys_displayed)
      keys_displayed[k] = None
  # control by the program
  with st.expander("Auto Set (will be overwritten by the program)", expanded=True):
    for k in auto_params:
      print(k)
      show_hydra_field(k, kv, keys_displayed,disabled=True)
      keys_displayed[k] = None
  # the rest
  with st.expander("full controls"):
    for k,v in kv.items():
      show_hydra_field(k, kv, keys_displayed)
      keys_displayed[k] = None

def edit_hydra_params(hydra_config):
  try:
    config_dir_selected = abs_config_dir
    # os.path.join(os.getcwd(),hydra_config_dir_selected(context=context)['abs_dir'])
    print(config_dir_selected)
    config_name_selected = config_name
    # hydra_config_name_selected(context=context)
    print("hydra_config_dir_selected", config_dir_selected)
    print("hydra_config_name_selected",config_name_selected )
    x = read_hydra_config(config_dir=config_dir_selected, config_name=config_name_selected)
    y = convert_dict_to_array(x)
    show_hydra_group(y,
      control_params=control_params, 
      input_params=input_params, 
      output_params=output_params, 
      auto_params=auto_params)
  except:
    pass
