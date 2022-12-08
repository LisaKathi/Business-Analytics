#####

# web application code for predicting revenue of online shoppers

##### 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

st.set_page_config(
    page_title="Online Shopper Revenue App",
    layout="wide"
    )


# import dataset and cache it (so it has not to be loaded every time)
@st.cache()
def load_data():
    data = pd.read_csv("../Data/online_shoppers_app_dev.csv")
    return(data.dropna())
data = load_data()

@st.cache()
def load_model():
    filename = "finalized_default_model.sav"
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)
model = load_model


st.title("Online Shopper Revenue Predictor App")

st.write("This App predicts whether a person browsing online on shopping pages will eventually purchase something at the end of the session")

















