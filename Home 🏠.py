#cd '.\Python\Selenium Morningstar Visualization\'
#python -m streamlit run .\st-morningstar_visualization.py
import streamlit as st
import requests
import base64

url = 'https://github.com/danielarodval/st-morningstar-visualization/blob/main/README.md'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    content = req.text
    st.markdown(content)
else:
    st.error('Content was not found.')