import streamlit as st

def main(title):
    st.sidebar.header('Settings')

    actions = {'nothing': ':frowning:', 'something': ':smile:', 'everything': ':sunglasses:'}
    options = ['Average', 'Good', 'Excellent']
    competence = st.sidebar.select_slider('Select competence level', options=options, value='Good')
    action = list(actions.keys())[options.index(competence)]

    st.title(title)
    st.write(f'## Welcome to another app that does {action}! {actions[action]}')
