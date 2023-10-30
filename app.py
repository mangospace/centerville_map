import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
# Step 1: Read the downloaded and merged data

data=pd.read_csv("D:\CMS_GPDC\downloaded_data_2122.csv")
data["Dcename_22"]=np.where(data["Dcename_22"]=="FREEDOM PHYSICIANS CORPORATION", "Freedom Physicians Corporation", data["Dcename_22"])
data["Dcename_22"]=np.where(data["Dcename_22"]=="ADVANCED VALUE CARE  II", "Advanced Value Care II", data["Dcename_22"])
data["Dcename_21"]=np.where(data["Dcename_21"]=="FREEDOM PHYSICIANS CORPORATION", "Freedom Physicians Corporation", data["Dcename_21"])
data["Dcename_21"]=np.where(data["Dcename_21"]=="ADVANCED VALUE CARE  II", "Advanced Value Care II", data["Dcename_21"])

# Step 2: Streamlit app
st.title("DCE Performance Comparison")
st.header("Select DCE Name")
selected_dce = st.selectbox("Choose DCE Name", data["Dcename_22"].unique())
#selected_dce="Iora Health NE DCE, LLC"
# Step 3: Filter data based on selected DCE Name
df=pd.melt(data, id_vars='Dcename_22', value_vars=["Netsavingsrate_21","Netsavingsrate_22"], var_name='year', value_name='Netsavingsrate',)

df['year'] = np.where(df['year']=="Netsavingsrate_21", "2021", "2022")
df['year']=df['year'].astype('category')
filtered_data = df[df["Dcename_22"] != selected_dce]
# Step 4: Plotting
fig = go.Figure()
for x in filtered_data["Dcename_22"]:
    df1 = df[df["Dcename_22"] == x]
    fig.add_trace(go.Scatter(x=df1["year"], y=df1["Netsavingsrate"], mode='lines',  line=dict(color="lightgrey")))
    fig.update_traces(selector=dict(type='scatter',mode='lines+markers'))
    fig.update_traces(marker=dict(size=12))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickvals=[2021, 2022])

# Highlight selected DCE's performance in red
highlighted_data = df[df["Dcename_22"] == selected_dce]
fig =    fig.add_trace(go.Scatter(x=highlighted_data["year"], y=highlighted_data["Netsavingsrate"], mode='lines', name=selected_dce, line=dict(color="blue")))
fig.update_traces(selector=dict(type='scatter',mode='lines+markers'))
fig.update_traces(marker=dict(size=12))
fig.update_xaxes(tickvals=[2021, 2022])
#fig.update_xaxes(showticklabels=False)
#fig.show()

# Display the chart
st.plotly_chart(fig)
data=data[["Dcename_21","State_22",
"Risk_arrangement_21", "Risk_arrangement_22",
"Totalbene-_ficiaries_21", "Totalbene-_ficiaries_22",
"Netsavingsrate_21", "Netsavingsrate_22"]]

data.rename(columns={
"Dcename_21":"DCE Name",
"State_22":"State",
"Risk_arrangement_21":"Risk Arrangement 21",
"Risk_arrangement_22":"Risk Arrangement 22",
"Totalbene-_ficiaries_21":"Total Benes 21",
"Totalbene-_ficiaries_22":"Total Benes 22",
"Netsavingsrate_21":"Net Savings Rate 21",
"Netsavingsrate_22":"Net Savings Rate 22"
}, inplace=True)

st.write("DCE Entities that have changed Risk Arrangements,  joined or left in 2022")
data2=data[data["Risk Arrangement 21"]!=data["Risk Arrangement 22"]]
st.dataframe(data2)

st.write("DCE Entities with > 10% change in beneficiaries")
data3=data[(1.1*data["Totalbenes 21"]<=data["Totalbenes 22"])| (data["Totalbenes 21"] <=0.9*data["Totalbenes 22"])]
st.dataframe(data3)

data4=data[[ "DCE Name", "State", "Total Benes 21","Total Benes 22", "Net Savings Rate 21", "Net Savings Rate 22"]]

st.write("2021 and 2022 data of DCE Entities and their performance")
st.dataframe(data4)
