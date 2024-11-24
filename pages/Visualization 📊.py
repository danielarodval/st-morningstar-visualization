import streamlit as st
import pandas as pd # type: ignore
import os

st.title('Visualization 📊')

#df = pd.read_csv('../static_data/pct_change_df.csv', index_col=0)
df = pd.read_csv(os.path.join('static_data','pct_change_df.csv'), index_col=0)

st.write(df)