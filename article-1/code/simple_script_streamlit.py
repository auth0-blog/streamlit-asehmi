import streamlit as st

actions = {'A': st.write, 'B': st.write, 'C': st.write}
choice = st.selectbox('Choose one:', ['_', 'A', 'B', 'C'])
if choice != '_':
    result = actions[choice](f'You chose {choice}')
