import streamlit.components.v1 as components
import settings

COMPONENT_URL = f'{settings.COMPONENT_BASE_URL}/streamlit'
# Declare component
component_host = components.declare_component(name='ComponentHost', url=COMPONENT_URL)
