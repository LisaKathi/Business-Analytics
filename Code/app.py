#####

# web application code for predicting revenue of online shoppers

##### 

import streamlit as st
import numpy as np
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

#definition for adding more space between paragraphs
def add_space(lines):
    for i in range(lines):
        st.write("\n")


st.title("Online Shopper Revenue Predictor App")

st.write("This App predicts whether a person browsing online on shopping pages will eventually purchase something at the end of the session")

st.header("Modell-Informationen")

add_space(3)

# Introducing three colums for user inputs
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

p_value = row1_col1.slider("PageValue",
                  data["PageValues"].min(),
                  data["PageValues"].max(),
                  (0.0, data["PageValues"].max()))


monatsnamen = {"Februar": 2, "März": 3, "Mai": 5, "Juni": 6, "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12}

month = row1_col2.multiselect("Monat der Session", monatsnamen.keys())

if month:
    Monat = [monatsnamen[n] for n in month]
else:
    Monat = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12]



names = data.columns
variable = row1_col3.selectbox("Auswahl der Variable", names)

# creating filtered data set according to slider inputs
filtered_data = data.loc[(data["PageValues"] >= p_value[0]) & 
                         (data["PageValues"] <= p_value[1]) &
                         (data["Month"].isin(Monat)), : ]


add_space(3)


# defining two columns for layouting plots 

row2_col1, row2_col2  = st. columns([1,1])

row2_col1.subheader("Revenue")

if filtered_data.empty:
    
    row2_col1.write("\n")
    row2_col1.write("\n")
    row2_col1.write("\n")
    row2_col1.error("Keine Daten erfüllen die Vorgaben.")
    
else:
            
        
    fig1, ax = plt.subplots(figsize=(10,6))

    if filtered_data.groupby("Revenue").size().count() == 2:  

        plt.pie(x = filtered_data.groupby("Revenue").size(), explode = (0.05, 0.05), autopct="%.2f%%", pctdistance=0.5, startangle=90, 
                textprops={'fontsize': 15}, labels = ["Kein Kauf", "Kauf"], colors = ['#4169E1', 'tomato'])
        
# Put matplotlib figure in col 1
        
        row2_col1.pyplot(fig1)

    else:
        
        row2_col1.write("\n")
        row2_col1.write("\n")
        row2_col1.write("\n")
        row2_col1.info("100% der Daten führen zu Käufen.")
          
        



# Zweiter Plot


fig2 = sns.displot(x=data[variable], hue=data["Revenue"], kind="kde", palette="Set2", multiple="stack")
row2_col2.subheader("Dichteverteilung der Variable")
row2_col2.pyplot(fig2)

add_space(5)


############################# Guessing Game #################################

# create subsample for the guessing game
test_frac = data.iloc[16:27,:].reset_index().drop(columns="index")
test_frac["Persons"] = test_frac.index
test_frac["Persons"].replace({0:"Justus-Aurelius",1:"Daniel",2:"Jule",
                           3:"David",4:"Tgetg",5:"Lisa",6:"Leo",
                           7:"Isabel",8:"Maximilian",9:"Lara",10:"Marie"},inplace=True)
test_frac.set_index("Persons", drop=True, inplace=True)
test_frac["Prediction"] = model.predict(test_frac.drop(columns="Revenue"))
test_samples = test_frac[["PageValues","Month","VisitorType_Returning_Visitor"]]


# create two columns for the guessing game
row3_col1, row3_col2 = st.columns([1,1])

### guessing game

st.markdown("***")

row3_col1.subheader("Guessing Game")
row3_col1.write("Select a person and predict based on the given\
                parameters in the table on the right, whether \
                this online shopper will generate a revenue or not\
                meaning if a purchase happens or not")
with row3_col1.form(key="sample_form"):
    sample = st.selectbox("Select a person:", 
                          test_samples.index)
    guess = st.radio("Make a prediction based on the values for that person as to whether that person will purchase something online (Revenue) or not (No Revenue)",
                     ('Revenue', 'No Revenue'))
    submit = st.form_submit_button("Submit")
    if submit:
        sample_rev = test_frac.loc[test_frac.index == sample, "Revenue"].item()
        sample_pred = test_frac.loc[test_frac.index == sample, "Prediction"].item()
        #st.write(test_samples.loc[test_samples.index == sample,])
        
        
        if ((sample_rev == 1) and (guess == "Revenue")) or((sample_rev == 0) and (guess == "No Revenue")):
            st.write("Congratulations, your prediction is **correct**")
        elif ~((sample_rev == 0) and (guess == "No Revenue")) or ~((sample_rev == 1) and (guess == "Revenue")):
            st.write("Unfortunately your prediction is **wrong**")
        if sample_rev == 1:
            st.write("In this case the online shopper **does** generate a revenue")
        if sample_rev == 0:
            st.write("In this case the online shopper **does not** generate a revenue")
        if ((sample_pred == 0) and (guess == "No Revenue")) or ((sample_pred == 1) and (guess == "Revenue")):
            st.write("Your Predictions is **congruent** with the prediction of the model")
        elif ~((sample_pred == 0) and (guess == "No Revenue")) or ~((sample_pred == 1) and (guess == "Revenue")):
            st.write("Your prediction is **different** from the models' prediction")
        else: 
            st.write("Please check your input again")

### Display the table with the values for the guessing game        

if row3_col2.checkbox("Press here to see the Values for each person"):

    row3_col2.write("This table shows for each person three of the most relevant values\
                    determining whether an online shopper will generate\
                    a revenue")
    table_samples = test_samples.copy()
    table_samples.rename(columns={"PageValues": "Page Value in US-Dollar",
                                  "VisitorType_Returning_Visitor": "Returning Visitor"}, inplace=True)
    table_samples["Month"].replace({2:'Feburary',3:"March",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}, inplace=True)
    table_samples["Returning Visitor"].replace({1:"Yes",0:"No"}, inplace=True)
    table_samples.index = table_samples.index.rename("Person")
    
    row3_col2.write(table_samples.to_html(), unsafe_allow_html=True)

############################# Data Upload and Prediction #################################
add_space(5)

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












