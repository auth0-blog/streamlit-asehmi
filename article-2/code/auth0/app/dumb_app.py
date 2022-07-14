import streamlit as st
import requests
import json

import settings
from common import messageboard, check_token

def main(title):
    st.sidebar.header('Settings')

    capabilities = {'Do Nothing 😦': 'nothing', 'Call Public API 😄': 'something', 'Call Secure API 😎': 'everything'}
    capability = st.sidebar.radio('Select app capability', capabilities.keys())
    action = capabilities[capability]

    st.title(title)
    st.write(f'## Welcome to the app that does {action}! {capability[-1]}')

    response = None
    base_url = settings.REMOTE_API_BASE_URL

    # Example public API call
    if capabilities[capability] == 'something':
        response = requests.get(base_url + '/api/ping')

    # Example protected API call
    if capabilities[capability] == 'everything':
        if check_token(st.session_state.token):
            headers = {"Authorization": f"Bearer {st.session_state.token['value']}", "accesstoken": f"{st.session_state.token['value']}"}
        else:
            messageboard.error('Something went wrong! Authentication token not available.')

        response = requests.get(base_url + '/api/pong', headers=headers)

    json_ = None
    if response and response.ok:
        json_ = json.loads(response.text)
        data = json_['data']
        st.info(data)
    elif response:
        st.error(f'ERROR: {response.text}')
