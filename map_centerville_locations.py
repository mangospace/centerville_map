import pandas as pd
import pandas as pd
import numpy as np
import folium
import streamlit as st
from streamlit_folium import st_folium
full_data=pd.read_csv(r"D:\Data\Twitter\Centerville_location_map\allcenters.csv")


full_data=pd.read_csv('https://raw.githubusercontent.com/mangospace/OpTreat/main/oct_data.csv')
full_data.reset_index(drop=True)
statelist=full_data['STATE'].tolist()
statelist.insert(0, "US")

st.title('Opiod Treatment Centers')
st.caption("Oct 2023")
st.caption('Made by @manas8u')
st.caption('Please share your feedback and suggestions. DM @manas8u')

option1 = st.selectbox(
    'Which state would you like to explore in detail?',
    (statelist))

state_data=pd.read_csv('https://raw.githubusercontent.com/mangospace/OpTreat/main/state_center.csv', dtype={'lat':np.int32,	'lon':np.int32})
df2 = pd.DataFrame({"lat":[48],
                    "lon":[-102],
                    "STATE":["US"]})

state_data=pd.concat([state_data,df2])
state_data=state_data[state_data["STATE"]==option1]
state_data=state_data.reset_index(drop=True)
long=state_data.loc[0,'lon']
latt=state_data.loc[0,'lat']

if option1=="US":
    zoom_start_var=3
    full_data1=full_data   
else:
    zoom_start_var=6
    full_data1=full_data[full_data['STATE']==option1]
    full_data1=full_data1.reset_index(drop=True)

m = folium.Map(location=[latt, long], zoom_start=zoom_start_var)
for x in range(len(full_data1)):
    folium.Marker(
        location=[full_data1.loc[x,'lat'],full_data1.loc[x,'lon']],
        tooltip=full_data1.loc[x,'CITY'],
        popup=full_data1.loc[x,'PROVIDER NAME'],
        icon=folium.Icon(color="green"),
    ).add_to(m)
st_data = st_folium(m, width=725)
