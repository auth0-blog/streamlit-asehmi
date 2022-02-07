import streamlit as st

import settings

# --------------------------------------------------------------------------------

# Initialize Session State variables
# (May be used by modules below so initialize before importing them!)
if 'message' not in st.session_state:
    st.session_state.message = 'None'
if 'token' not in st.session_state:
    st.session_state.token = False
if 'report' not in st.session_state:
    st.session_state.report = []

# --------------------------------------------------------------------------------

from common import messageboard, check_token
import dumb_app, dumber_app

# --------------------------------------------------------------------------------

# !! Appears to throw errors if initialized using messageboard.empty() !!
messageboard = st.empty()

# --------------------------------------------------------------------------------

def main():
    if settings.USE_AUTHENTICATION:
        with st.expander('Authenticate'):
            import component_runner
            from component_event_handler import handle_event

            component_runner.init(handle_event)

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
    st.sidebar.title('Component Hero Demo')
    st.sidebar.markdown('---')
    st.sidebar.info('(c) 2022. CloudOpti Ltd. All rights reserved.')

if __name__ == '__main__':
    st.sidebar.image('./images/logo.png', output_format='png')
    main()
