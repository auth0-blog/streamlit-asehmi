import streamlit.components.v1 as components
import settings

# Declare component

# Running from dev server (or different port to Streamlit)
COMPONENT_URL = f'{settings.COMPONENT_BASE_URL}/streamlit'
component_hero = components.declare_component(name='component_hero', url=COMPONENT_URL)

'''
# Running from static build (runs in Streamlit server)
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
COMPONENT_PATH = os.path.join(parent_dir,'../../',settings.COMPONENT_BASE_PATH)
# COMPONENT_PATH = os.path.join(parent_dir,'../frontend')
print(f'COMPONENT_PATH = {COMPONENT_PATH}')
component_hero = components.declare_component(name='component_hero', path=COMPONENT_PATH)
'''
