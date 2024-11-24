#cd '.\Python\Selenium Morningstar Visualization\'
#python -m streamlit run .\st-morningstar_visualization.py
import streamlit as st
import requests
import base64

url = 'https://raw.githubusercontent.com/danielarodval/portfolio/main/Python/Selenium%20Morningstar%20Visualization/README.md'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    content = req.text
    st.markdown(content)
else:
    st.error('Content was not found.')