import streamlit as st
import lightning_app as L
import time
import hydra
import omegaconf
import os
import copy

def unroll_to_dict(cfg:omegaconf.OmegaConf,level=[]) -> dict:
  """unroll hierarchial dict to flat dict """
  flat_cfg={}
  for k,v in cfg.items():
    if isinstance(v,omegaconf.dictconfig.DictConfig):
      flat_cfg.update(unroll_to_dict(v,level + [k]))
    else:
      flat_k = ".".join(level + [k])
      #print(flat_k,v)
      flat_cfg[flat_k] = str(v)
  return(flat_cfg)    

def read_hydra_config_from_file(root_dir="../lightning-pose", config_dir="scripts/configs", config_name="config"):
  """read hydra conf"""
  abs_config_dir=os.path.join(os.path.abspath(os.path.expanduser(root_dir)), config_dir)
  hydra.core.global_hydra.GlobalHydra.instance().clear()
  hydra.initialize_config_dir(config_dir=abs_config_dir, version_base=None) # config_dir: absolute file system path
  cfg_nest = hydra.compose(config_name=config_name)
  cfg_flat = unroll_to_dict(cfg_nest)
  return(cfg_nest, cfg_flat)

def render(state):
  button = st.button("submit")
  if button:
    state.button = True
  for k,v in state.current.items():
    state.new[k] = st.text_input(k,value=state.current[k], placeholder=state.current[k], help=state.help[k])
  state.end = True

class MySt(L.LightningFlow):
  def __init__(self, cfg_flat:dict, cfg_help:dict):
    super().__init__()
    self.current = copy.deepcopy(cfg_flat)
    self.placeholder = copy.deepcopy(cfg_flat)
    self.new = copy.deepcopy(cfg_flat)
    self.help = copy.deepcopy(cfg_help)
    self.button = False
    self.end = None # TODO BUG: end has to toggled for state to transfer from streamlit to app
  def run(self):
    pass  
  def configure_layout(self):
      return L.frontend.StreamlitFrontend(render_fn=render)

class MyWork(L.LightningWork):
  def __init__(self):
    super().__init__()
  def run(self):
    pass  

class MyFlow(L.LightningFlow):
  def __init__(self):
    super().__init__()
    cfg_nest, cfg_flat = read_hydra_config_from_file()
    cfg_help = {}
    for k,v in cfg_flat.items():
      cfg_help[k]=None
    cfg_help["model.losses_to_use"] = "use this and that"
    print(type(cfg_flat))
    self.my_st = MySt(cfg_flat, cfg_help)
    self.count = 0

  def run(self):
    if self.my_st.button:
      for k,v in self.my_st.new.items():
        print(f"{k}={v}")
      self.my_st.button = False  

app = L.LightningApp(MyFlow())