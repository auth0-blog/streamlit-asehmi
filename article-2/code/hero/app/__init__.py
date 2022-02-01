import streamlit as st
from datetime import datetime

# --------------------------------------------------------------------------------

messageboard = st.empty()

# --------------------------------------------------------------------------------

# Initialize Session State variables:
if 'message' not in st.session_state:
    st.session_state.message='To use this application, please login...'
if 'token' not in st.session_state:
    st.session_state.token={'value': None, 'expiry': None}
if 'user' not in st.session_state:
    st.session_state.user=None
if 'email' not in st.session_state:
    st.session_state.email=None
if 'report' not in st.session_state:
    st.session_state.report=[]

# --------------------------------------------------------------------------------
def check_token(token):
    token_value = token['value']
    if token_value:
        token_expiry = datetime.fromtimestamp(int(token['expiry']))

        tnow = datetime.now()
        expired = tnow >= token_expiry

        if not expired:
            return True
        else:
            st.session_state.token['value'] = None
            return False
