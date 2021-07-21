import streamlit as st

import settings

# --------------------------------------------------------------------------------

from modules.hero_component import run_login_component

EVENTS = ['onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError']
PROPS = { 'hostname':'Hero Streamlit App',
          'initial_state': {
            'password': settings.ENCRYPT_PASSWORD
        }}

def init(event_handler):
    run_login_component(EVENTS, PROPS, event_handler)
