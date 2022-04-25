import streamlit as st

# --------------------------------------------------------------------------------

from modules import component_auth0 as declared_component
from modules.auth0_component import run_component

EVENTS  = [ 'onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError' ]
PROPS   = { 'hostname':'Hero Streamlit App',
            'initial_state': {'message': st.session_state.message},
          }

def init(event_handler):
    run_component(declared_component, EVENTS, PROPS, event_handler)
