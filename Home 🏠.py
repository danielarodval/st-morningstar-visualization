#cd '.\Python\Selenium Morningstar Visualization\'
#python -m streamlit run .\st-morningstar_visualization.py
import streamlit as st
import requests

url = 'https://raw.githubusercontent.com/danielarodval/st-morningstar-visualization/main/README.md'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    content = req.text
    st.markdown(content)
else:
    st.error('Content was not found.')