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
    layout="wide")

############# Funtionen, Modelle und Daten laden ####################

# import dataset and cache it (so it has not to be loaded every time)
@st.cache()
def load_data():
    data = pd.read_csv("../Data/online_shoppers_app_dev.csv")
    return(data.dropna())
data = load_data()

@st.cache()
def load_variable_explanation():
    data = pd.read_excel("../Data/Variable_Explanation.xlsx")
    return(data.dropna())
variable_explanation = load_variable_explanation()

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

################### Einleitung #########################

st.title("Online Shopper Revenue Predictor App")

st.header("Einführung: Die Revenue-Predictor App")

st.write("Kaufen oder nicht kaufen? Diese Frage stellt sich nicht nur für Besucher von Online Shopping Portalen, sondern auch die Betreiber \
         der Webseiten. Zum einem ist Kenntnis über Kunden ein großer Vorteil für effektives Marketing. Zum anderen hilft es realistische \
        Budgets zu erstellen, wenn Einnahmen verlässlich vorhergesagt werden können. Wissen über Kaufentscheidungen ist daher eine wertvolle \
        Ressource für zahlreiche Unternehmen. Um diese Fragen zu beantworten sagt diese App für individuelle Kunden voraus, ob es am Ende eines\
        Website-Besuchs zu einer Transaktion kommt oder nicht.")
st.write("Für die Vorhersage wird ein XGBoost-Model verwendet, welches schnell und zuverlässig eine Vorhersage trifft.\
         Die ausschlagebensten Variablen sind PageValue, Month und ReturingVisitor.")

if st.checkbox("Klicke hier, um die Erklärung der Variablen anzuzeigen"):
    st.write(variable_explanation)

st.header("Modell-Informationen")

add_space(3)


#################### User Input #########################


# Introducing three colums for user inputs
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

# slider page values
p_value = row1_col1.slider("Page-Value",
                  data["PageValues"].min(),
                  data["PageValues"].max(),
                  (0.0, data["PageValues"].max()))

#input für Monat
monatsnamen = {"Februar": 2, "März": 3, "Mai": 5, "Juni": 6, "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12}
month = row1_col2.multiselect("Monat der Session", monatsnamen.keys())

if month:
    Monat = [monatsnamen[n] for n in month]
else:
    Monat = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12]

names = data.drop(columns="Revenue").columns

# input individuelle variablen
variable = row1_col3.selectbox("Auswahl der Variable", names)

# creating filtered data set according to slider inputs
filtered_data = data.loc[(data["PageValues"] >= p_value[0]) & 
                         (data["PageValues"] <= p_value[1]) &
                         (data["Month"].isin(Monat)), : ]


add_space(3)

############################### Plots #################################

# defining three columns for plots 

row2_col1, row2_col2, row2_col3  = st. columns([0.7,1,1])

# Erster Plot 
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
row2_col2.subheader("Dichteverteilung der Variable *{}*".format(variable))
row2_col2.pyplot(fig2)



data_proba = data.drop(columns="Revenue").copy()
probability = pd.DataFrame(model.predict_proba(data_proba))
data_proba["Revenue Probability"] = probability.iloc[:,1]
#data_proba[["Probability 0"],["Probability"]] = model.predict_proba(data_proba)

# Dritter Plot
row2_col3.subheader("Wahrscheinlichkeit Revenue in Abhängigkeit der Variable *{}*".format(variable))

fig3, ax = plt.subplots(figsize=(10,7.5))
ax.scatter(data_proba[variable], data_proba["Revenue Probability"], edgecolor='#4d4d4d', label=variable, alpha=0.8)
ax.set_xlabel(variable, fontsize=15)
ax.set_ylabel("Wahrscheinlichkeit einer Transaktion in Prozent", fontsize=15)
ax.grid()
ax.legend().set_title("Variable")
ax.set_facecolor("#f5f5fa")
row2_col3.pyplot(fig3)

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
row3_col1.write("Wähle eine Person aus und entscheide, basierend auf den drei wichtigsten Werten \
                in der Tabelle auf der rechten Seite, ob eine Transaktion stattfindet oder nicht")
with row3_col1.form(key="sample_form"):
    sample = st.selectbox("Wähle eine Person aus:", 
                          test_samples.index)
    guess = st.radio("Entscheide, ob die ausgewöhlte Person nach dem besuch der Shopping-Website \
                     eine Transaktion durchführt oder nicht",
                     ('Transaktion', 'Keine Transaktion'))
    submit = st.form_submit_button("Submit")
    if submit:
        sample_rev = test_frac.loc[test_frac.index == sample, "Revenue"].item()
        sample_pred = test_frac.loc[test_frac.index == sample, "Prediction"].item()
        #st.write(test_samples.loc[test_samples.index == sample,])
        
        
        if ((sample_rev == 1) and (guess == "Transaktion")) or((sample_rev == 0) and (guess == "Keine Transaktion")):
            st.write("Gratulation, deine Vorhersage ist **korrekt**")
        elif ~((sample_rev == 0) and (guess == "Keine Transaktion")) or ~((sample_rev == 1) and (guess == "Transaktion")):
            st.write("Leider ist deine Vorhersage **falsch**")
        if sample_rev == 1:
            st.write("In diesem Fall findet **eine** Transaktion statt")
        if sample_rev == 0:
            st.write("In diesem Fall findet **keine** Transaktion statt")
        if ((sample_pred == 0) and (guess == "Keine Transaktion")) or ((sample_pred == 1) and (guess == "Transaktion")):
            st.write("Die App hat **dieselbe** Vorhersage wie Du getroffen")
        elif ~((sample_pred == 0) and (guess == "Keine Transaktion")) or ~((sample_pred == 1) and (guess == "Transaktion")):
            st.write("Die App hat eine **andere** Vorhersage als Du getroffen")
        else: 
            st.write("Bitte überprüfe deine Eingabe nocheinmal")

### Display the table with the values for the guessing game        

if row3_col2.checkbox("Klicke hier um die Werte für jede Person zu sehen"):

    row3_col2.write("Diese Tabelle zeigt für jede Person die drei wichtigsten Werte für die Vorhersage der \
                    Zielvariable *Revenue*, also ob eine Transaktion stattfindet oder nicht")
    table_samples = test_samples.copy()
    table_samples.rename(columns={"PageValues": "Page-Value in US-Dollar", "Month":"Monat",
                                  "VisitorType_Returning_Visitor": "Wiederkehrender Kunde"}, inplace=True)
    table_samples["Monat"].replace({2:'Februar',3:"März",5:"Mai",6:"Juni",7:"Juli",8:"August",9:"September",10:"Oktober",11:"November",12:"Dezember"}, inplace=True)
    table_samples["Wiederkehrender Kunde"].replace({1:"Ja",0:"Nein"}, inplace=True)
    table_samples.index = table_samples.index.rename("Person")
    
    row3_col2.write(table_samples.to_html(), unsafe_allow_html=True)

############################# Data Upload and Prediction #################################
add_space(5)

# predict revenue for uploaded data
st.header("Upload eigener Daten")

uploaded_data = st.file_uploader("Wähle eine csv-Datei mit Kundendaten aus, um vorherzusagen, ob eine Transaktion stattfindet oder nicht")

# only make predictions if data is uploaded
if uploaded_data is not None:
    new_customers = pd.read_csv(uploaded_data)
    new_customers = pd.get_dummies(new_customers, drop_first=True)
    new_customers["predictions"] = model.predict(new_customers)
    st.download_button(label="Download vorhergesagte Kunden-Daten",
                       data=new_customers.to_csv().encode("utf-8"),
                       file_name="scored_new_customers.csv")

# display dataset with predictions
    if st.checkbox("Klicke hier, wenn Du die vorhergesagten Daten sehen willst"):
        st.write(new_customers)
       
    
    
    
add_space(5)
    
st.write("Die Daten sind von folgender Quelle: Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Real-time prediction of online shoppers’ \
         purchasing intention using multilayer perceptron and LSTM recurrent neural networks. \
        Neural Comput & Applic 31, 6893–6908 (2019). https://doi.org/10.1007/s00521-018-3523-0")
    

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
'<b><a href="#upload-eigener-daten" style="color: black;text-decoration: none;">Upload eigener Daten</a></b><br/><br/>'

, unsafe_allow_html=True)












