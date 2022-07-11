import lightning_app as L
import pass_st_as_param_1

class MySt(L.LightningFlow):
  def __init__(self, cfg_flat:dict = None, cfg_help:dict = None):
    super().__init__()
    self.pass_st_as_param_2 = ""
  def run(self):
    pass  
  def configure_layout(self):
      return L.frontend.StreamlitFrontend(render_fn=pass_st_as_param_1.render)

class MyWork(L.LightningWork):
  def __init__(self):
    super().__init__()
  def run(self):
    pass  

class MyFlow(L.LightningFlow):
  def __init__(self):
    super().__init__()
    self.my_work = MyWork()
    self.my_st   = MySt()
  def run(self):
    if self.my_st.pass_st_as_param_2:
      print(self.my_st.pass_st_as_param_2)
    pass  

app = L.LightningApp(MyFlow())