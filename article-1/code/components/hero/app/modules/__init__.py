import streamlit.components.v1 as components
import settings

# Declare component

# Running from dev server (or different port to Streamlit)
COMPONENT_URL = f'{settings.COMPONENT_BASE_URL}/streamlit'
component_hero = components.declare_component(name='component_hero', url=COMPONENT_URL)
