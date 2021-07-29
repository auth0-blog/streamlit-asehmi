import streamlit as st
import settings

# --------------------------------------------------------------------------------

from modules import component_hero as declared_component
from modules.hero_component import run_component

EVENTS  = [ 'onStatusUpdate', 'onAdhocReport', 'onActionRequest', 'onError' ]
PROPS   = { 'hostname':'Hero Streamlit App',
            'initial_state': {
                'password': settings.ENCRYPT_PASSWORD,
                'message': 'Default Message',
                'action': 'Default Action'
            },
          }

def init(event_handler):
    run_component(declared_component, EVENTS, PROPS, event_handler)
