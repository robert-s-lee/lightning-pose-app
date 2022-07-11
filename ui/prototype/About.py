import streamlit as st
import streamlit.components.v1 as components

# refer to https://docs.streamlit.io/library/get-started/multipage-apps

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.write("# Welcome Lightning Pose App")

st.markdown("""<img src="https://github.com/danbider/lightning-pose/raw/main/assets/images/LightningPose_horizontal_light.png" alt="Wide Lightning Pose Logo" width="200"/>

Convolutional Networks for pose tracking implemented in **Pytorch Lightning**, 
supporting massively accelerated training on *unlabeled* videos using **NVIDIA DALI**.

### A Single application with pre-integrated components
* Lightning Pose Configuration
* Train
* Train Diagnostics
* Image/Video Diagnostics Preparation
* Image/Video Diagnostics
* Image/Video Annotation

### Built with the coolest Deep Learning packages
* `pytorch-lightning` for multiple-GPU training and to minimize boilerplate code
* `nvidia-DALI` for accelerated GPU dataloading
* `Hydra` to orchestrate the config files and log experiments
* `kornia` for differntiable computer vision ops
* `torchtyping` for type and shape assertions of `torch` tensors
* `FiftyOne` for visualizing model predictions
* `Tensorboard` to visually diagnoze training performance

### Configuration

""", unsafe_allow_html=True)

