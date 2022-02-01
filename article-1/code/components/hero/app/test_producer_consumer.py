# Asyncio-based producer/consumer/queue pattern implementation
# https://docs.python.org/3/library/asyncio.html

import asyncio

async def event_consumer(queue, my_consumer):
    while True:
        event = await queue.get()
        try:
            # call the "event handler" to produce a result
            result = my_consumer.process(event)
        except Exception as ex:
            result = ['>> Exception in consumer event handler <<', str(ex)]
        queue.task_done()
        my_consumer.report(result)

async def event_producer(queue, my_producer):
    while True:
        event = await my_producer.next_event() # your producer should expose a `next_event()` method
        if event:
            # use a fake assignment of the next statement to prevent st
            # from auto-writing the return result as 'None'
            _ = await queue.put(event)

# will terminate only when app is closed (i.e., there's no explicit producer/consumer thread termination)
async def consumer_producer_runner(my_producer, my_consumer):
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
    # use fake assignments in these next statements to prevent st
    # from auto-writing the return results as 'None'
    _ = await asyncio.gather(producer)
    _ = await queue.join()
    consumer.cancel

# ------------------------------------------------------------------------------
# Dummy producer/consumer:

import streamlit as st
STREAMLIT = True if st._get_report_ctx() else False
messageboard = None
reporter = print
if STREAMLIT:
    messageboard = st.empty()
    reporter = messageboard.write

# Dummy producer
class MyProducer:
    def __init__(self):
        self.count = 0
    async def next_event(self):
        self.count += 1
        return await asyncio.sleep(1, result=self.count)

# Dummy consumer
class MyConsumer:
    def __init__(self):
        pass
    def process(self, event):
        return {'result': event}
    def report(self, result):
        reporter(result)

# ------------------------------------------------------------------------------
# Asynchronously run producer/consumer like so: 

if __name__ == '__main__':
    asyncio.run(consumer_producer_runner(MyProducer(), MyConsumer()))
