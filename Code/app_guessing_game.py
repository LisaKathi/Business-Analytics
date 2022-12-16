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

# create subsample for the guessing game
test_frac = data.iloc[16:27,:].reset_index().drop(columns="index")
test_frac["Prediction"] = model.predict(test_frac.drop(columns="Revenue"))
test_samples = test_frac[["PageValues","Month","VisitorType_Returning_Visitor"]]
st.write(test_samples.iloc[0:11,:])

st.title("Online Shopper Revenue Predictor App")

st.write("This App predicts whether a person browsing online on shopping pages will eventually purchase something at the end of the session")

# create two columns for the guessing game
row3_col1, row3_col2 = st.columns([1,1])

### guessing game

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
            st.write("Congratulations, your prediction was correct")
        elif ~((sample_rev == 0) and (guess == "No Revenue")) or ~((sample_rev == 1) and (guess == "Revenue")):
            st.write("Unfortunately your prediction was wrong")
        if sample_rev == 1:
            st.write("In this case the online shopper **does** generate a revenue")
        if sample_rev == 0:
            st.write("In this case the online shopper **does not** generate a revenue")
        if ((sample_pred == 0) and (guess == "No Revenue")) or ((sample_pred == 1) and (guess == "Revenue")):
            st.write("Your Predictions is congruent with the prediction of the model")
        elif ~((sample_pred == 0) and (guess == "No Revenue")) or ~((sample_pred == 1) and (guess == "Revenue")):
            st.write("Your prediction is different from the models' prediction")
        else: 
            st.write("Please check your input again")

### Display the table with the values for the guessing game        
row3_col2.subheader("Values for each Person")
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

sns.set(style = 'darkgrid')
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
















