import os
import logging
from datetime import datetime

import hydra
import omegaconf

import streamlit as st
from lightning_app.utilities.state import AppState
from lai_components.hydra_utils import read_hydra_config_from_file
import ui.hydra_run_out

from pathlib import Path

global key_hydra_config_name
global key_hydra_config_dir
global key_hydra_config_file
global key_hydra_config_file_edit

key_hydra_config_name="hydra_config_name" # "--config_name={st.state[key_hydra_config_name]}")
key_hydra_config_dir="hydra_config_dir"   # "--config-dir={st.state[key_hydra_config_dir]}")
key_hydra_config_file="hydra_config_file"
key_hydra_config_file_edit="hydra_config_file_edit"

input_params=[ "data.data_dir", "data.csv_file", "data.video_dir"]
output_params=["hydra.run.out"]
control_params=["model.losses_to_use", "training.max_epochs", "training.num_workers" ]
auto_params=["eval.hydra_paths", "eval.test_videos_directory", "eval.saved_vid_preds_dir" ]

def hydra_config_name_selected(context=st) -> str:
  if key_hydra_config_name in st.session_state and not(st.session_state[key_hydra_config_name] is None):
    return(f"{st.session_state[key_hydra_config_name]}")
  else:
    return("")  

def hydra_config_dir_selected(context=st) -> str:
  try:
    config_dir = st.session_state[key_hydra_config_dir]
  except:
    config_dir = None
  return(config_dir)

def get_hydra_config():
  """return --config_name --config_dir "hydra.run.out as dict"""
  ret = {}
  if key_hydra_config_name in st.session_state and not(st.session_state[key_hydra_config_name] is None) and st.session_state[key_hydra_config_name] != "":
    ret["--config_name"]="'%s'" % st.session_state[key_hydra_config_name]
  if not (hydra_config_dir_selected() is None):
    ret["--config_dir"]="'%s'" % hydra_config_dir_selected()['rel_dir']
  if key_hydra_run_out in st.session_state and not(st.session_state[key_hydra_config_name] is None) and st.session_state[key_hydra_config_name] != "":
    ret["hydra.run.out"]="'%s'" % st.session_state[key_hydra_run_out]
  return(ret)  

def get_hydra_config_name():
  if key_hydra_config_name in st.session_state and not(st.session_state[key_hydra_config_name] is None):
    return(f"--config_name={st.session_state[key_hydra_config_name]}")
  else:
    return("")  

def get_hydra_dir_name():
  if not (hydra_config_dir_selected() is None):
    return(f"--config_dir={hydra_config_dir_selected()}")
  else:
    return("")

def get_hydra_config_from_ui():
  config_dir_selected = os.path.join(os.getcwd(),hydra_config_dir_selected(context=st)['abs_dir'])
  print(config_dir_selected)
  config_name_selected = hydra_config_name_selected(context=st)
  print("hydra_config_dir_selected", config_dir_selected)
  print("hydra_config_name_selected",config_name_selected )
  cfg_dict, cfg_list = read_hydra_config_from_file(config_dir=config_dir_selected, config_name=config_name_selected)
  return(cfg_dict, cfg_list)  



def set_hydra_config_name(config_name="config.yaml", context=st):
  """set --config_name=config.yaml"""
  x = context.text_input("hydra default config name", value=config_name, placeholder=config_name, key=key_hydra_config_name)
  if x=="":
    context.error(f"config name cannot be empty")

def set_hydra_config_dir(config_dir=".", context=st, root_dir="."):
  """set --config_dir=dir from a list of dir that has config.yaml"""

  config_name = st.session_state[key_hydra_config_name]
  root_dir = os.path.expanduser(root_dir)

  # options = [ [dirname,full_path, rel_path] ...]
  options_show_basename = lambda opt: opt["rel_dir"]

  # options should have just .yaml
  options=[]  
  try:
    if not options:
      for file in Path(os.path.join(root_dir,config_dir)).rglob(config_name):
        abs_dir = os.path.dirname(file)
        rel_dir = os.path.relpath(os.path.dirname(file),root_dir)
        rel_path = os.path.relpath(file, root_dir)
        options.append({"rel_dir":rel_dir, "abs_dir":abs_dir, "root_dir":root_dir, "rel_path":rel_path, "abs_path":str(file)})
  except:
    pass      

  # show it 
  context.selectbox("hydra config dir", options, key=key_hydra_config_dir, format_func=options_show_basename)


def set_hydra_config_file(config_dir=None, config_ext="*.yaml", context=st):
  """select a file from a list of *.yaml files"""
  config_dir = hydra_config_dir_selected(context=context)
  # options should have just .yaml 
  # options = [ [dirname,full_path, rel_path] ...]
  options_show_basename = lambda opt: opt["rel_path"]
  options=[] 
  try:
    if not options:
      for file in Path(config_dir["abs_dir"]).rglob(config_ext):
        rel_path = os.path.relpath(file,config_dir["root_dir"])
        options.append({"rel_path":rel_path, "abs_path":str(file)})
  except:
    pass

  # NOTE: pasing array of array somtimes produces error when format_func=options_show_basename is used
  # don't use format_func here
  # ValueError: ['config.yaml', 'configs/rick-configs-1/config.yaml'] is not in iterable
  context.selectbox("override hydra config", options, key=key_hydra_config_file, format_func=options_show_basename)

def edit_hydra_config_file(language="yaml", context=st):
  """edit a content of .yaml file"""    
  filename = st.session_state[key_hydra_config_file]
  if filename is None:
    return

  filename = filename["abs_path"]

  if not(key_hydra_config_file_edit in st.session_state):
    st.session_state[key_hydra_config_file_edit]={}

  content_changed = False
  if filename in st.session_state[key_hydra_config_file_edit]:
    content_raw = st.session_state[key_hydra_config_file_edit][filename]
    content_changed = True
  else:
    try:
      with open(filename) as input:
        content_raw = input.read()
    except FileNotFoundError:
      context.error("File not found.")
    except Exception as err:
      context.error(f"can't process select file. {err}")
      return
  content_new = st_ace(value=content_raw, language=language)
  if content_changed or content_raw != content_new:
    context.warning("content changed")
    if not(key_hydra_config_file_edit in st.session_state):
      st.session_state[key_hydra_config_file_edit]={}
    st.session_state[key_hydra_config_file_edit][filename] = content_new


def run(st, state:AppState = None):
  ui.hydra_run_out.run(st=st, state=state)
  set_hydra_config_name(config_name=config_name, context=st)
  set_hydra_config_dir(root_dir=root_dir, config_dir=config_dir, context=st)
  cfg_dict, cfg_list = get_hydra_config_from_ui()
  st.write(cfg_dict)
  st.write(cfg_list)
  return(get_hydra_config(),cfg_dict, cfg_list)
  
# only for testing streamlit run hydra_ui.py
# if run from pages, the will also run
if __name__ == "__main__":
  print("os.path.realpath(__file__)", os.path.realpath(__file__))
  print("os.path.dirname(__file__)", os.path.dirname(__file__))

  x = run(root_dir="../lightning-pose")
