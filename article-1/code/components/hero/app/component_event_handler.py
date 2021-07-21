import streamlit as st

from common import check_token
import settings

# --------------------------------------------------------------------------------
def handle_event(event):
    if not event:
        # return the preserved report
        return st.session_state.report
    
    name = event.name
    data = event.data

    report = []
    if (not name or not data):
        print('>>> WARNING! - Null name or data. <<<')
        report.append('>>> WARNING! - Null name or data. <<<')
        st.session_state.report = report
        return report

    props = data.get('props', None)
    action = data.get('action', None)

    report.append(name)
    report.append(data)

    if name == 'onActionRequest':
        report.append(f'{action} actions not supported')

    elif name == 'onStatusUpdate':
        st.session_state.token = data.get('token', False)

    st.session_state.report = report

    return report
