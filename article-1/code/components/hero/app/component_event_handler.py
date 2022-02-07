import streamlit as st

# --------------------------------------------------------------------------------
def handle_event(event):
    if not event:
        # return the preserved report
        return st.session_state.report
    
    name = event.name
    data = event.data
    source = event.source

    report = []
    report.append(name)
    report.append(data)

    # action and its initial properties
    action = data.get('action', None)
    props = data.get('props', None)

    if name == 'onStatusUpdate':
        st.session_state.token = data.get('token', False)
    elif name == 'onActionRequest':
        report.append(f'onActionRequest: {action} is not yet implemented.')
    elif name == 'onError':
        report.append([f'>> ERROR! <<', f'Source: {source}', f'Data: {data}'])
    else:
        report.append(['>> WARNING! <<', f'Event {name} is not implemented.', f'Source: {source}', f'Data: {data}'])

    st.session_state.report = report
    return report
