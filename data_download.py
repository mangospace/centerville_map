import pandas as pd
import regex as re
import numpy as np
# Step 1: Download and merge data
#@st.cache_data 
def load_data():
    url_2021 = "https://www.cms.gov/priorities/innovation/media/document/gpdc-py2021-financial-results"
    url_2022 = "https://www.cms.gov/files/document/gpdc-py2022-financial-results.xlsx"

    data_2021 = pd.read_excel(url_2021, sheet_name="DCE results PY2021")
    new_name=[]
    for x in data_2021.columns:
        if x=="DCE\nID":
            new_name.append("DCEID")
        else:
            x=re.sub("\\n","_",x)
            x=re.sub("\d","",x)
            x=re.sub("\s","",x)            
            x=x.capitalize()            
            new_name.append(re.sub("$","_21",x))
    data_2021.columns = new_name
    data_2021.dtypes
    data_2021['Grosssavingsrate_21']=    100*data_2021['Grosssavingsrate_21'].round(4)
    data_2021['Netsavingsrate_21']=100*data_2021['Netsavingsrate_21'].round(4)

    data_2022 = pd.read_excel(url_2022, sheet_name="DCE-Level Results PY2022")
    new_name=[]
    for x in data_2022.columns:
        if x=="DCE\nID":
            new_name.append("DCEID")
        else:
            x=re.sub("\\n","_",x)
            x=re.sub("\d","",x)
            x=re.sub("\s","",x)
            x=x.capitalize()            
            new_name.append(re.sub("$","_22",x))
    data_2022.columns = new_name
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(", LLC.","")
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(", L.C.","")
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(", Inc.","")
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(", LLC","")
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(", Inc","")
    data_2022['Dcename_22']=data_2022['Dcename_22'].str.replace(" Inc.","")
    data_2022['Grosssavingsrate_22']=  100* data_2022['Grosssavingsrate_22'].round(4)
    data_2022['Netsavingsrate_22']=100*data_2022['Netsavingsrate_22'].round(4)
    merged_data = pd.merge(data_2021, data_2022, on="DCEID", how="outer")
    return merged_data

data = load_data()

data['Dcename_22'] = np.where(data['Dcename_22'].isnull(), data['Dcename_21'], data['Dcename_22'])
data['State_22'] = np.where(data['State_22'].isnull(), data['State_21'], data['State_22'])
data['Dcename_21'] = np.where(data['Dcename_21'].isnull(), data['Dcename_22'], data['Dcename_21'])
data['Saving per Bene 22']=data["Netsavings_(loss)_22"]/data["Totalbene-_ficiaries_22"]
data['Saving per Bene 22']=data['Saving per Bene 22'].round(2)
data['Saving per Bene 22']
#converting to rates from decimals
data.to_csv("D:\CMS_GPDC\downloaded_data_2122.csv")

data=data[["Dcename_21","State_22",
"Risk_arrangement_21", "Risk_arrangement_22",
"Totalbene-_ficiaries_21", "Totalbene-_ficiaries_22",
"Netsavingsrate_21", "Netsavingsrate_22",'Saving per Bene 22']]

#get column names ready for presentation on site
data.rename(columns={
"Dcename_21":"DCE Name",
"State_22":"State",
"Risk_arrangement_21":"Risk Arrangement 21",
"Risk_arrangement_22":"Risk Arrangement 22",
"Totalbene-_ficiaries_21":"Total Benes 21",
"Totalbene-_ficiaries_22":"Total Benes 22",
"Netsavingsrate_21":"Net Savings Rate 21 (%)",
"Netsavingsrate_22":"Net Savings Rate 22 (%)",
'Saving per Bene 22':'Saving per Bene 22 ($)'
}, inplace=True)

#limited data that had a risk arrangement change

data2=data[data["Risk Arrangement 21"]!=data["Risk Arrangement 22"]]
data2.to_csv("D:\CMS_GPDC\DCE_risk_arrangement_change.csv")

#limited data that had beneficiary change

data3=data[(1.1*data["Total Benes 21"]<=data["Total Benes 22"])| (data["Total Benes 21"] <=0.9*data["Total Benes 22"])]
data3.to_csv("D:\CMS_GPDC\DCE_sig_bene_change.csv")

#Full data that is clean

data4=data[[ "DCE Name", "State", "Total Benes 21","Total Benes 22", "Net Savings Rate 21 (%)", "Net Savings Rate 22 (%)","Saving per Bene 22 ($)"]]

data4.to_csv("D:\CMS_GPDC\DCE_abbrev_table.csv")

