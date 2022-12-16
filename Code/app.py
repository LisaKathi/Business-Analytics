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

@st.cache(hash_funcs={'xgboost.sklearn.XGBClassifier': id})
def load_model():
    filename = "finalized_default_model.sav"
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)
model = load_model()


st.title("Online Shopper Revenue Predictor App")

st.write("This App predicts whether a person browsing online on shopping pages will eventually purchase something at the end of the session")

st.header("Modell-Informationen")


# Introducing three colums for user inputs
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

p_value = row1_col1.slider("The PageValue according to Google Analytics",
                  data["PageValues"].min(),
                  data["PageValues"].max(),
                  (0.0, data["PageValues"].max()))

month = row1_col2.multiselect("Month of the Session", ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"))


names = data.columns
variable = row1_col3.selectbox("Select Variable to Compare", names)

# creating filtered data set according to slider inputs
#filtered_data = data.loc[(data["borrower_rate"] >= rate[0]) & 
#                         (data["borrower_rate"] <= rate[1]) &
#                         (data["monthly_income"] >= income[0]) & 
#                         (data["monthly_income"] <= income[1]), : ]


# defining two columns for layouting plots 
row2_col1, row2_col2  = st. columns([1,1])

explode = (0.05, 0.05)
fig1, ax = plt.subplots(figsize=[10,6])

plt.pie(x = data.groupby('Revenue').size(), autopct="%.2f%%", explode=explode, pctdistance=0.5, startangle=90, 
       labels = ['No revenue','Revenue'], textprops={'fontsize': 15}, colors = ['#4169E1', 'tomato'])

#ax.set_title("Revenue Share", fontsize=20);

# Put matplotlib figure in col 1 
row2_col1.subheader("Revenue")
row2_col1.pyplot(fig1)


# Zweiter Plot

#sns.set(style = 'darkgrid')
#sns.set(rc={'figure.figsize':(15, 7.5)})

#RevenueData = data.loc[data['Revenue'] == 1]
#NoRevenueData = data.loc[data['Revenue']!=1]

#ax2 = sns.kdeplot(data=RevenueData['ExitRates'], fill=True, common_norm=False, 
#   alpha=.33, linewidth=2, color = 'tomato')

#ax2 = sns.kdeplot(data=NoRevenueData['ExitRates'], fill=True, common_norm=False, 
#   alpha=.33, linewidth=2, color = '#4169E1')


#ax2.legend(labels=['Revenue','No revenue'])
#ax2.set_title('KDE Plot of YOUR VARIABLE', fontsize = 20)

# Put seaborn figure in col 2 
#ax2 = ax2.get_figure()
#row2_col2.subheader("Vergleich Variablen")
#row2_col2.pyplot(ax2)


# predict revenue for uploaded data
st.header("Predicting if customer purchases something or not")

uploaded_data = st.file_uploader("Choose a file with Customer Data for making predictions")

# only make predictions if data is uploaded
if uploaded_data is not None:
    new_customers = pd.read_csv(uploaded_data)
    new_customers = pd.get_dummies(new_customers, drop_first=True)
    st.write(new_customers)
    
    new_customers["predictions"] = model.predict(new_customers)
    
    st.download_button(label="Download Scored Customer Data",
                       data=new_customers.to_csv().encode("utf-8"),
                       file_name="scored_new_customers.csv")
    st.write(new_customers["predictions"])
    
    

# Sidebar Navigation

st.sidebar.markdown("# :earth_africa: App-Menü:<br/><br/><br/>", unsafe_allow_html=True)

st.sidebar.markdown(
    
'## :arrow_up_small: &ensp;'
'<b><a href="#online-shopper-revenue-predictor-app" style="color: red;text-decoration: none;">Start</a></b><br/><br/><br/>'

':books: &ensp;'
'<b><a href="#modell-informationen" style="color: black;text-decoration: none;">Modell-Informationen</a></b><br/><br/>'

':trophy: &ensp;'
'<b><a href="#guessing-game" style="color: black;text-decoration: none;">Guessing Game</a></b><br/><br/>'

':cloud: &ensp;'
'<b><a href="#predicting-if-customer-purchases-something-or-not" style="color: black;text-decoration: none;">Upload eigener Daten</a></b><br/><br/>'

, unsafe_allow_html=True)












