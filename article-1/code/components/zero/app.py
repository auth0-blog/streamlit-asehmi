import streamlit as st
from datetime import datetime

from frontend import component_zero

if 'counter' not in st.session_state:
    st.session_state.counter = 0

def main():
    def run_component(props):
        value = component_zero(key='zero', **props)
        return value
    def handle_event(value):
        st.header('Streamlit')
        st.write('Received from component: ', value)

    st.title('Component Zero Demo')
    st.session_state.counter = st.session_state.counter + 1
    props = {
        'initial_state': {'message': '' },
        'counter': st.session_state.counter,
        'datetime': str(datetime.now().strftime("%H:%M:%S, %d %b %Y"))
    }

    handle_event(run_component(props))   

if __name__ == '__main__':
    main()