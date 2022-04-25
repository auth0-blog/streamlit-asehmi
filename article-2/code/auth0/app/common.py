import streamlit as st
from datetime import datetime

# --------------------------------------------------------------------------------

messageboard = st.empty()

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
