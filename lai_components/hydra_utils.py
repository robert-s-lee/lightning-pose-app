import hydra
import omegaconf
import os
import datetime

def unroll_to_dict(cfg:omegaconf.OmegaConf,level=[]) -> dict:
  """unroll hierarchial dict to flat dict """
  flat_cfg={}
  for k,v in cfg.items():
    if isinstance(v,omegaconf.dictconfig.DictConfig):
      flat_cfg.update(unroll_to_dict(v,level + [k]))
    else:
      flat_k = ".".join(level + [k])
      #print(flat_k,v)
      flat_cfg[flat_k] = str(v) # Lightning App requires string
  return(flat_cfg)    

def read_hydra_config_from_file(root_dir="lightning-pose", config_dir="scripts/configs", config_name="config"):
  """read hydra conf"""
  abs_config_dir=os.path.join(os.path.abspath(os.path.expanduser(root_dir)), config_dir)
  hydra.core.global_hydra.GlobalHydra.instance().clear()
  hydra.initialize_config_dir(config_dir=abs_config_dir, version_base=None) # config_dir: absolute file system path
  cfg_nest = hydra.compose(config_name=config_name)
  cfg_flat = unroll_to_dict(cfg_nest)
  return(cfg_nest, cfg_flat)

def set_hydra_run_out() -> str:
  """return hydra.run.out in outputs/%Y-%m-%d/%H-%M-%S format"""
  return(datetime.datetime.today().strftime('outputs/%Y-%m-%d/%H-%M-%S')) 
  