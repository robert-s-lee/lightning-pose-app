# lightning run app ui/app.py
# streamlit run ui/About.py

from lai_components.hydra_utils import read_hydra_config_from_file
import lightning_app as L
import copy
import ui.About

class MySt(L.LightningFlow):
  def __init__(self, cfg_flat:dict = {}, cfg_help:dict = {}):
    super().__init__()
    self.current = copy.deepcopy(cfg_flat)
    self.target = copy.deepcopy(cfg_flat)
    self.default = copy.deepcopy(cfg_flat)
    self.help = copy.deepcopy(cfg_help)
    self.button = False
    self.end = None # TODO BUG: end has to toggled for state to transfer from streamlit to app  def run(self):
    pass  
  def configure_layout(self):
      return L.frontend.StreamlitFrontend(render_fn=ui.About.run)

class MyWork(L.LightningWork):
  def __init__(self):
    super().__init__()
  def run(self):
    pass  

class MyFlow(L.LightningFlow):
  def __init__(self):
    super().__init__()
    cfg_nested, cfg_flat = read_hydra_config_from_file()
    self.my_st   = MySt(cfg_flat=cfg_flat)
    self.my_work = MyWork()
  def run(self):
    if self.my_st.button:
      print(self.my_st.target)
    pass  

app = L.LightningApp(MyFlow())