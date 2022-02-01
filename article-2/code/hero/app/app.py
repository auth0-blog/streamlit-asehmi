import streamlit as st

import settings

try:
    import ptvsd
    ptvsd.enable_attach(address=('localhost', 6789))
    # ptvsd.wait_for_attach() # Only include this line if you always want to manually attach the debugger
except:
    # Ignore... for Heroku deployments!
    pass

from __init__ import messageboard, check_token
import component_handler

# --------------------------------------------------------------------------------

import dumb_app, dumber_app

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

# !! Appears to throw errors if initialized using messageboard.empty() !!
messageboard = st.empty()

if settings.USE_AUTHENTICATION:
    AUTH_LABEL = 'Authenticate'

    label = AUTH_LABEL
    if (check_token(st.session_state.token)):
        label = f'{st.session_state.user} ({st.session_state.email})'
    with st.beta_expander(label):
        component_handler.init()
        # force a rerun to flip the expander label
        logged_in_but_showing_login_label = (check_token(st.session_state.token) and label == AUTH_LABEL)
        logged_out_but_showing_logged_in_label = (not check_token(st.session_state.token) and label != AUTH_LABEL)
        if (logged_in_but_showing_login_label or logged_out_but_showing_logged_in_label):
            st.experimental_rerun()

# --------------------------------------------------------------------------------

def main():
    # >> MAIN APP <<
    pages = {
        'DuMMMy aPp 1': [dumb_app.main],      # DUMMY APP 1
        'DUmmmY ApP 2': [dumber_app.main],    # DUMMY APP 2
    }

    def _launch_apps():
        messageboard.empty()
        choice = st.sidebar.radio('What do you want to do?', tuple(pages.keys()))
        pages[choice][0](title=choice, *pages[choice][1:])

    if settings.USE_AUTHENTICATION:
        if (check_token(st.session_state.token)):
            _launch_apps()
        else:
            messageboard.info('Please login below...')
    else:
        _launch_apps()

    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('Streamlit app.\n\n' + \
        '(c) 2021. CloudOpti Ltd. All rights reserved.')
    st.sidebar.markdown('---')

if __name__ == '__main__':
    st.sidebar.image('./images/logo.png', output_format='png')
    main()
