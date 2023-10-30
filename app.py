import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Step 1: Read the downloaded and merged data
data=pd.read_csv(r"https://raw.githubusercontent.com/mangospace/ACO_DCE_21_22/main/downloaded_data_2122.csv")

# Step 2: Streamlit app
#st.markdown("<h1 style='text-align: center; color: black;'>Direct Contracting Entity (DCE) Performance</h1>", unsafe_allow_html=True)

url="https://www.cms.gov/priorities/innovation/innovation-models/gpdc-model"
st.markdown("<h1 style='text-align: center; color: black;'>Direct Contracting Entity (DCE) Performance</h1>", unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;"><a href="https://www.cms.gov/priorities/innovation/innovation-models/gpdc-model">Source: CMS GPDC Updated Oct 2023</a></h4>', unsafe_allow_html=True)

selected_dce = st.selectbox("Select DCE", data["Dcename_22"].unique())

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

st.divider()

data2=pd.read_csv("https://raw.githubusercontent.com/mangospace/ACO_DCE_21_22/main/DCE_risk_arrangement_change.csv")
data2=data2.drop(columns=['Unnamed: 0'])
st.markdown("<h2 style='text-align: center; color: black;'>DCE Entities that have changed Risk Arrangements,  joined or left in 2022</h2>", unsafe_allow_html=True)
st.dataframe(data2, hide_index=True)
st.divider()

#limited data that had beneficiary change
data3=pd.read_csv("https://raw.githubusercontent.com/mangospace/ACO_DCE_21_22/main/DCE_sig_bene_change.csv")
data3=data3.drop(columns=['Unnamed: 0'])
st.markdown("<h2 style='text-align: center; color: black;'>DCE Entities with > 10% change in beneficiaries</h2>", unsafe_allow_html=True)
st.dataframe(data3, hide_index=True)

st.divider()
#Full data that is clean
st.markdown("<h2 style='text-align: center; color: black;'>DCE Entities and their performance (2021 and 2022)</h2>", unsafe_allow_html=True)
data4=pd.read_csv("https://raw.githubusercontent.com/mangospace/ACO_DCE_21_22/main/DCE_abbrev_table.csv")
data4=data4.drop(columns=['Unnamed: 0'])
st.dataframe(data4, hide_index=True)
