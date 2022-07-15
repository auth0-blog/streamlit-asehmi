from datetime import datetime
import json
import asyncio

import settings

# --------------------------------------------------------------------------------

DEFAULT_EVENTS = ['onStatusUpdate', 'onActionRequest', 'onError']

# --------------------------------------------------------------------------------
class ComponentHost():
    """Wrapper component for component_hero.

    A generic remote component host, e.g. React app authenticating with Auth0 identity provider.

    All props are forwarded to the component. Methods are not supported.

    Parameters
    ----------
    key : str, optional
        Unique value to isolate multiple components in an app from each other.
    events : list, optional
        Events the host app subscribes to

    Returns
    -------
    ComponentHost object
    """
    
    declared_component = None   # low level declared component host
    key = None
    events = []
    props = {}
 
    class ComponentEvent():
        '''
        Object holding an event name (obj.name), data (obj.data), event source (obj.source).
        name and data can be set to `None`.
        '''
        name = None
        data = None
        source = None

        def __init__(self, host, event):
            e = {}
            if isinstance(event, str):
                e = json.loads(event)
            elif isinstance(event, dict):
                e = event

            event_name = e.get('name', None)
            event_data = e.get('data', None)

            # All events are named

            # Filter by allowed events
            if event_name in host.events:
                self.name = event_name
                self.data = event_data
            else: # report error for unknown and null named events
                self.name = 'onError'
                self.data = {'message': f'Component event {event_name} is not allowed. (Data: {event_data})'}

            self.source = host


    def __init__(self, declared_component, key=None, events=DEFAULT_EVENTS, **props):

        self.declared_component = declared_component
        self.key = key
        self.events = events

        # Allowed props
        self.props = {prop: value for prop, value in props.items() if prop in [
            'hostname', 'initial_state'
        ]}
        # Default prop value
        self.props.setdefault('hostname', 'Default Host')
        self.props.setdefault('initial_state', {'message': 'Default Message', 'action': 'Default Action'})
        self.props.setdefault('events', DEFAULT_EVENTS)
        self.props.setdefault("width", "100%") # built-in prop, height is set in the component itself

        print('### Component Host Ready ###')
        print(f'Event queue: {settings.USE_COMPONENT_EVENT_QUEUE}')
        print(f'Props: {json.dumps(self.props)}')

    def next_event(self):
        # Run declared component
        event = self.declared_component(key=self.key, **(self.props))
        return self.ComponentEvent(host=self, event=event)

    def send_event(self, event):
        '''
        Functionality to send events/data to a component is not supported
        by Streamlit, except when the component is initially mounted :(

        On the other hand, the component can pass events to Streamlit as
        and when it needs to.

        Options to address this issue:

        - (simplest) Wait for Streamlit to support this natively 
        - (complicated) Build a static component and load it using component.declare_component's
          'path' attribute, which would enable you to use browser local storage
          as a data exchange mailbox (since the static component will be served
          by Streamlit's server and hence will share domain and local storage)
        - (complex) Use WebRTC
        - (overkill) Use a cloud database, such as Firestore or Airtable
        '''
        pass

# --------------------------------------------------------------------------------

def run_component(declared_component, events, props, event_handler):
    try:
        if settings.USE_COMPONENT_EVENT_QUEUE:
            run_component_async(declared_component, events, props, event_handler)
        else:
            run_component_sync(declared_component, events, props, event_handler)
    except Exception as ex:
        print('>> Exception running component <<')
        print(str(ex))

# --------------------------------------------------------------------------------
# ASYNC QUEUE-BASED VERSION

async def event_consumer(queue, my_consumer):
    while True:
        event = await queue.get()
        try:
            report = my_consumer(event)
        except Exception as ex:
            print('>> (event_consumer) Exception in event handler <<', str(ex))
            report = ['>> (event_consumer) Exception in event handler <<', str(ex)]
        queue.task_done()
        print_report(report)

async def event_producer(queue, my_producer):
    event = my_producer.next_event()
    if event:
        await queue.put(event)

async def consumer_producer_runner(my_consumer, my_producer):
    # In Streamlit context there might not be an event loop
    # present, so need to create one. (loop, consumers, producers, queue
    # must all be set up in the same awaitable thread!)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    queue = asyncio.Queue()

    consumer = asyncio.create_task(event_consumer(queue, my_consumer))
    producer = asyncio.create_task(event_producer(queue, my_producer))
    await asyncio.gather(producer)
    await queue.join()
    consumer.cancel

# will terminate only when app is closed (i.e., there's no explicit producer/consumer thread termination)
def run_component_async(declared_component, events, props, event_handler):
    component_host = ComponentHost(declared_component, key='login', events=events, **props)
    asyncio.run(consumer_producer_runner(event_handler, component_host))

# --------------------------------------------------------------------------------
# SYNCHRONOUS VERSION

def run_component_sync(declared_component, events, props, event_handler):
    component_host = ComponentHost(declared_component, key='login', events=events, **props)
    event =  component_host.next_event()
    if event:
        try:
            report = event_handler(event)
        except Exception as ex:
            print('>> (run_component_sync) Exception in event handler <<', str(ex))
            report = ['>> (run_component_sync) Exception in event handler <<', str(ex)]
        print_report(report)

# --------------------------------------------------------------------------------
def print_report(report):
    print()
    print(f'### [{datetime.now()}] Component event handler report ####')
    print(report)

