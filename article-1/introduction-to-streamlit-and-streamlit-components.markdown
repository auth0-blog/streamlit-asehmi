---
layout: post
title: "Introduction to Streamlit and Streamlit Components"
description: "Streamlit is an open-source app framework for Machine Learning and Data Science teams. You can create beautiful data apps in hours. All in pure Python. Streamlit was released in October 2019 and there's huge excitement about it in the Data Science community. It's not just for Data Science though. With its component extensibility architecture you can build and integrate most kinds of web front ends into Streamlit apps. This series of articles will show you how to do this, and in particular, will describe how to implement Auth0 authentication of Streamlit apps using Streamlit Components."
date: "2021-07-09 08:30"
author:
  name: "Arvindra Sehmi"
  url: "https://www.linkedin.com/in/asehmi/"
  mail: "vin@thesehmis.com"
  avatar: "https://twitter.com/asehmi/profile_image?size=original"
related:
- 2017-11-15-an-example-of-all-possible-elements
---

# Introduction to Streamlit and Streamlit Components

**TL;DR:** Streamlit is an open-source app framework for Machine Learning and Data Science teams. You can create beautiful data apps in hours. All in pure Python. Streamlit was released in October 2019 and there's huge excitement about it in the Data Science community. It's not just for Data Science though. With its component extensibility architecture you can build and integrate most kinds of web front ends into Streamlit apps. This series of articles will show you how to build Streamlit apps and custom Streamlit Components, with the end goal of implementing Auth0 authentication of Streamlit apps using Streamlit Components.

Here is the [GitHub repository](https://github.com/asehmi/guest-writer/tree/master/articles) for this series of articles.

Let me put it out there, I'm a big fan of [Streamlit](https://www.streamlit.io/) and use it a lot at work and play. In my role as an NLP/ML/Data Engineer I use [Python](https://www.python.org/) along with several excellent Python frameworks such as [scikit-learn](https://scikit-learn.org/stable/), [spaCy](https://spacy.io/), [Pandas](https://pandas.pydata.org/), and [Altair Vizualization](https://altair-viz.github.io/). All these technologies work seamlessly with Streamlit. My experience with Streamlit can be verified on the official page of [Streamlit Creators](https://streamlit.io/creators).

After developing several in-house apps I needed to share some of them externally with clients and colleagues, so adding security and authentication features was imperative. I also wanted to support different kinds of communication patterns between a Streamlit host application and call both public and protected data APIs instead of using local file system resources, whilst keeping the number of moving parts and different technologies used to a minimum. This was a challenge worth pursuing to align with the productivity mantra of Streamlit which is "The fastest way to build and share data apps". As you'll see in this series of articles Streamlit's embedded components extensibility architecture and native session state management will help realize these objectives.

## What does Streamlit aim to achieve?

* There are a lot of barriers for data scientists (and engineering professional in general) to implement decent front-ends which would make their _cool stuff_ understandable and useful to others.
* Front-end engineering is hard! It's a super-power that people probably wish they had, but can't spend time investing in the skills... not to mention the technologies and frameworks change so fast - they're wired today, and tired tomorrow!
* Streamlit's starting point was to look at the machine learning engineering workflow, and asked the question:

> "_How can we make a machine learning script and convert it into an app as simply as possible, so that it basically feels like a scripting exercise?_"

## Streamlit focuses on simplicity

* A single package that you can install through `pip`, which gives you a bunch of functions which:
    * Can be _interleaved_ into an existing _ML code script_
    * Essentially making the ML code _parameterizable_
    * Does a little bit of _layout_, and
    * _Magically_ turns your ML code into a _beautiful app_
* Inspiration is drawn from Jupyter, ipywidgets, R-Shiny, Voila, React, etc., but more as a guiding light than a software architecture. There is a significant technical difference in the implementation of Streamlit. Existing frameworks (like Shiny, ipywidgets) are based on _wiring callbacks_ which, if you have enough of them, leads to an untestable mess. Streamlit instead is based on a [_declarative data flow model_](https://en.wikipedia.org/wiki/Dataflow_programming).

> The inventor of Streamlit, Adrien Treuille (PhD) says: "_We have a multi-threaded server that starts in the background, there’s WebSockets shuttling information back and forth to the browser, there’s a whole browser app that’s interpreting this and creating what you see on the screen... But all of that kind of goes away from the user’s perspective, and you just get really a couple dozen magical Python commands that transform a machine learning script or a data science script into an app that you can use and share with others._"

## Many use cases

* Every single data analysis team needs to create apps. They're a focal point - like the bonfire of the team. It’s where team members get together and communicate.
* Apps are a really crucial part of the ML (data analysis) workflow, especially in a non-trivial project.
* Not just for internal apps. Machine learning and data scientists need to build apps for external consumption too. Other teams need to consume models in various different ways, and it ought to much easier to build the required, but different, application layers to do that.

> "_These tools require constant new features, so it’s really empowering to be able to create them yourself easily and beautifully, and then directly iterate on them and directly serve them to your users, be they other members of your team or other people in the company. So that’s really the power of being able to write apps quickly and easily, and in a flow that you might expect, and I think that’s why the community has been so receptive._", Adrien Treuille.

# Getting started

The core Streamlit documentation, discussion forum, and examples gallery are very good. This article will by no means replace them, but will serve as an alternative place you can start learning about Streamlit with the specific aim of integrating with Auth0. To get a broader appreciation of Streamlit check out these links: [API Docs](https://docs.streamlit.io/index.html) **|** [Discussion Forum](https://discuss.streamlit.io/) **|** [Gallery](https://streamlit.io/gallery) **|** [GitHub](https://github.com/streamlit/streamlit).

## Installation

**Note**: to use `Streamlit` you’ll need Python 3.5 or above. I use the [Anconda Python distribution](https://docs.anaconda.com/anaconda/install/index.html), Visual Studio Code IDE with [Python extensions](https://code.visualstudio.com/docs/languages/python), which works well with conda environments.

* Open a `conda console` window
* If necessary, run `conda activate` for the env in which you want to install package requirements. See [managing conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

### Newbie install

`pip install streamlit`

`pip install --upgrade streamlit`

### Pro install

* Put package dependencies in `requirements.txt` and include with your app distro

`pip install -r requirements.txt`

* Alternatively, provide an `environment.yml` for use with `conda env create` and include with your app distro

`conda env create -f environment.yml`

* Include a `setup.py` script with your app if any special installation actions need to be performed

`python setup.py`

* Useful Streamlit CLI commands:

`streamlit config show`

`streamlit cache clear`

## Running your app locally

* Create a file `<your app>.py` (typically named, `app.py`)
* Add `import streamlit as st`
* Write some `python code`, and save
* In the `conda console`, from `<your app> directory`, type:

`streamlit run [--server.port <port number>] <your app>.py`

* If you don't specify a server port, `<your app>` will open a bowser window with the default port: [http://localhost:8765/](http://localhost:8765/).
* Yes... it's as simple as that!

## Running your app on a server

When running you app on a server you should run it in _headless_ mode. There are a few ways to do this:

1. Create a `config.toml` file in `.streamlit` sub-folder of your app folder, and add:

```
[server]
headless = true
```

2. Or, set the environment variable `STREAMLIT_SERVER_HEADLESS=true`
3. Or, when running your app from the command line, pass the `--server.headless true` parameter like:

`streamlit run --server.headless true <your_app>.py `

# Let's see some code?

Imagine a really simple Python program (script) which performs an action based your selection choice, something like this:

**`simple_script.py`**

```python
actions = {'A': print, 'B': print, 'C': print}
choice = None
while not choice in actions.keys():
    choice = input('Choose one of [A, B, C] > ').upper()
result = actions[choice](f'You chose {choice}')
```

You execute this program from the command line by typing `python simple_script.py` and it will prompt you to choose one of the options and echo it back to you.

```
$ python simple_script.py
Choose one of [A, B, C] > A
You chose A
```

So what would this script look like written as an interactive Streamlit web application? As hinted earlier, you should be able to transform the script simply be adding some "_magical Python commands_". Here it is:

**`simple_script_streamlit.py`**

```python
import streamlit as st

actions = {'A': st.write, 'B': st.write, 'C': st.write}
choice = st.selectbox('Choose one:', ['_', 'A', 'B', 'C'])
if choice != '_':
    result = actions[choice](f'You chose {choice}')
```

All I did is:

1. Import the `streamlit` package (as `st` by convention)
2. Replace the `print` action functions with Streamlit's magic `st.write` function
3. Replace the read input loop with a Streamlit's selection box widget, `st.selectbox`

Everything else is much the same. You can execute this program from the command line by typing `streamlit run simple_script_streamlit.py`. This will start a Streamlit server on the default port and render the web app in a new browser window. You should see something like this:

![simple-script-streamlit](./images/simple-script-streamlit.png)

The power of adding some magic dust to an existing Python script isn't so obvious in such a trivial example. Let's take a look at something more convincing with console data and charting capabilities from the command line.

**`simple_script_plot.py`**

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# pip install drawilleplot
# pip install windows-curses
matplotlib.use('module://drawilleplot')

def f1(t):
    return np.exp(-t) * np.cos(2*np.pi*t)
def f2(t):
    return np.cos(2*np.pi*t)
t = np.arange(0.0, 5.0, 0.1)

def table():
    print([x for x in zip(t,f1(t))])
    print([x for x in zip(t,f2(t))])

def plot():
    plt.figure()
    plt.subplot(2, 1, 1) # nrows, ncols, index
    plt.plot(t, f1(t), 'bo', t, f1(t), 'k')

    plt.subplot(212)
    plt.plot(t, f2(t), 'r--')
    plt.show()

    plt.close()

actions = {'T': table, 'P': plot}
choice = None
while not choice in actions.keys():
    choice = input('Choose one of [T (tabulate), P (plot)] > ').upper()
result = actions[choice]()
```

You execute this program from the command line by typing `python simple_script_plot.py` and, as before, it will prompt you to choose one of the options and performs the appropriate action.

Option 'T' displays coordinates of a couple of data series:

```
$ python simple_script_plot.py
Choose one of [T (tabulate), P (plot)] > t
[(0.0, 1.0), (0.1, 0.7320288483374399), (0.2, 0.2530017165184952), ..., (4.9, 0.006024412254402584)]
[(0.0, 1.0), (0.1, 0.8090169943749475), (0.2, 0.30901699437494745), ..., (4.9, 0.8090169943749488)]
```

Option 'P' displays ASCII charts of these data series:

```
$ python simple_script_plot.py
Choose one of [T (tabulate), P (plot)] > P
```

![simple-script-plot](./images/simple-script-plot.png)

Now, let's convert this console plotting script into an interactive Streamlit web application. It's much simpler than you may imagine:

**`simple_script_plot_streamlit.py`**

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def f1(t):
    return np.exp(-t) * np.cos(2*np.pi*t)
def f2(t):
    return np.cos(2*np.pi*t)
t = np.arange(0.0, 5.0, 0.1)

def table():
    st.write([x for x in zip(t,f1(t))])
    st.write([x for x in zip(t,f2(t))])

def plot():
    plt.figure()
    plt.subplot(2, 1, 1) # nrows, ncols, index
    plt.plot(t, f1(t), 'bo', t, f1(t), 'k')

    plt.subplot(212)
    plt.plot(t, f2(t), 'r--')

    st.pyplot(plt)

actions = {'Tabulate': table, 'Plot': plot}
choice = st.selectbox('Choose one:', ['_', 'Tabulate', 'Plot'])
if choice != '_':
    result = actions[choice]()
```

The key Streamlit function I used to draw a Matplotlib chart is `st.pyplot`.

As you can see the Streamlit script is quite similar to the plain script you saw earlier, but incredibly you now have a proper web app which can be deployed on a server and shared with others!

Execute this program from the command line by typing `streamlit run simple_script_plot_streamlit.py`, and you should see something like this:

![simple-script-plot-streamlit](./images/simple-script-plot-streamlit.png)

I'll implement a few small changes to the Streamlit script to make the web app look much nicer. Let's add a title and headings, a sidebar for multi-task selection, and render our data tables neatly over two columns. I'll also take advantage of Streamlit's initimate understanding of how to render Pandas `DataFrame` objects.

**`simple_script_plot_streamlit_plus.py`**

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def f1(t):
    return np.exp(-t) * np.cos(2*np.pi*t)
def f2(t):
    return np.cos(2*np.pi*t)
t = np.arange(0.0, 5.0, 0.1)

def table():
    st.header('Tables')
    c1, c2 = st.beta_columns(2)
    c1.write(pd.DataFrame([x for x in zip(t,f1(t))]))
    c2.write(pd.DataFrame([x for x in zip(t,f2(t))]))

def plot():
    plt.figure()
    plt.subplot(2, 1, 1) # nrows, ncols, index
    plt.plot(t, f1(t), 'bo', t, f1(t), 'k')

    plt.subplot(212)
    plt.plot(t, f2(t), 'r--')

    st.header('Charts')
    st.pyplot(plt)

st.title('Data Explorer')
st.sidebar.header('Settings')

actions = {'Tabulate': table, 'Plot': plot}
choices = st.sidebar.multiselect('Choose task:', ['Tabulate', 'Plot'])
for choice in choices:
    result = actions[choice]()
```

The key Streamlit functional changes I made used `st.multiselect`, `st.title`, `st.header`, `st.beta_columns`. The functions beginning with `st.sidebar.*` cause Streamlit to render widgets in a collapsible sidebar.

Execute this program from the command line by typing `streamlit run simple_script_plot_streamlit_plus.py`, and you should see something like this:

![simple-script-plot-streamlit-plus](./images/simple-script-plot-streamlit-plus.png)

Hopefully, you'll agree this is a big improvement in user experience over the original Python command line script. I achieved this using concise declarative statements that don't unnecessarily clutter the code with distracting procedural UI code, and the code was written entirely in Python.

# Debugging in VS Code

Before you start using more advanced Streamlit features, it's useful to learn how to debug Python programs, especially Python programs that are executed _remotely_, as they are in Streamlit's client-server architecture.

## Basic

* Use a Python unit testing framework. I use `unittest`. See [unittest docs](https://docs.python.org/2/library/unittest.html).
* **Or**... add an environment DEBUG flag to your project's VS Code `launch.json` file (in `.vscode` folder), like this, which you can use like a DEBUG switch:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"DEBUG": "true"}
        }
    ]
}
```

* **Or..** to be [12factor](https://12factor.net/) compliant, it's a good idea to `pip install django-environ`, and `import settings`. Read [the docs](https://django-environ.readthedocs.io/en/latest/).
* Always `import logging` and use `logging.info()`, `logging.debug()`, `logging.error()` to report to the console (as `print()` doesn't work in Streamlit unless run from the console).

## Advanced

See this article for details: [How to use Streamlit with VS Code](https://awesome-streamlit.readthedocs.io/en/latest/vscode.html)

**Note**, `debugpy` has replaced `ptvsd`

Essentially, follow these steps:

1. `pip install debugpy`
2. Add the following snippet in your `<your-app_name>.py` file.

```python
try:
    import debugpy
    debugpy.listen(("localhost", 5678))
    # debugpy.wait_for_client() # Only include this line if you always want to manually attach the debugger
except:
    # Ignore... for Heroku deployments!
    pass
```

3. Then start your Streamlit app

`streamlit run <your-app_name>.py`

4. From the VS Code Debug sidebar menu configure `Python: Remote Attach` debug server and update your `launch.json` file with the details below.

```json
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "port": 5678,
    "host": "localhost",
    "justMyCode": true,
    "redirectOutput": true,
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "."
        }
    ]
}
```

5. Make sure you manually insert the `redirectOutput` setting.
6. By default you will be debugging your own code only. If you want to debug into streamlit code, then change `justMyCode` setting from `true` to `false`.
7. Finally, attach the debugger by clicking the debugger play button.

## Profiling your app

Since Streamlit apps are stateless and executed top-down in full at every change, you need to be wary of performance issues. At some point you'll hit some unacceptable limits. Good server app design principles still apply with Streamlit apps. So, when `@st.cache()` just isn't enough, profile your code, and consider using well-understood server design techniques such as using a database, search index, or microservices.

```python
import contextlib
import time
import pandas as pd
import streamlit as st

@contextlib.contextmanager
def profile(name):
    start_time = time.time()
    yield  # <-- your code will execute here
    total_time = time.time() - start_time
    print('%s: %.4f ms' % (name, total_time * 1000.0))

with profile('load_data'):
    df = pd.read_excel('very_large_file.xlsx',nrows=1000000)
```

---
See this video by Dan Taylor: [Get Productive with Python in Visual Studio Code](https://www.youtube.com/watch?v=6YLMWU-5H9o), for useful tips on using vscode for Python development.

## Crosstalk!

The Streamlit architecture is such that each connected user has her own session object in the server, and her own separate thread where the app’s source file is executed. While the source file executes, the Streamlit library in that thread can only write to that specific session object (because that’s the only session it has a reference to).

Then, the Streamlit server periodically loops through its _websocket-to-session_ dict and writes any outstanding messages from each session into its corresponding websocket.

In theory, there should be no crosstalk between sessions! Issues have been reported when running on Google Compute Engine in a Docker container. If the app is behind a proxy, it might make all users appear to be visiting from the same IP address.

Ensure you have the latest Streamlit version installed as [this issue](https://discuss.streamlit.io/t/crosstalk-between-streamlit-sessions-with-multiple-users/319/3) was being actively addressed by the developers, who are very responsive and receptive to bug reports. Please use the discussion forum to report issues.

# Streamlit Components

Whilst the core functionality of Streamlit is rich and has high utility out-of-the-box, there are always cases where custom extensibility is desired. Streamlit Components let you expand the functionality provided in the base Streamlit package by enabling you to write JavaScript and HTML _components_ that can be rendered in Streamlit apps. Streamlit Components can receive data from Streamlit Python scripts, and send data to them when initially loaded. Streamlit _bi-directional_ Components have two parts:

1. A _front end_, which is implemented in any web technology you prefer (JavaScript, React, Vue, etc.), and gets rendered in Streamlit apps via an `iframe` tag.
2. A _Python API_, which Streamlit apps use to instantiate and communicate with that front end.

**Note**, basic static web components which are not intended to communicate with Streamlit can also be implemented. They use Streamlit's `components.html` and `components.iframe` APIs. In this article you will learn how to implement components that can communicate, using Streamlit's `components.declare_component` API. If you need more details on these concepts, please read the [Streamlit component docs](https://docs.streamlit.io/en/stable/develop_streamlit_components.html), otherwise what you'll study below is more than enough to progress from basic to advanced level Streamlit component development.

Components can be packaged and published to [PyPI](https://pypi.org/) just like any Python package, making distribution very easy.

## Creating components

In this section on creating bi-directional components I will cover two design approaches, namely:

1. **Component Zero**: This is a basic component design implementation which doesn't use any front end tooling, but has just enough structure to make it useful, and
2. **Component Hero**: This is a more sophisticated component design which wraps the core Streamlit components API to add support for _eventing_ and, by using Next.js web framework, opens the door to more advanced user experiences, server-side rendering of static web pages, hosted APIs, and more.

For each of these designs I'll show some code and diagrams with increasing detail, covering:

* System capabilities
* System architecture
* Application start up sequence

You will have enough detail to replicate and make changes to each design implementation yourself.

## Component Zero: a basic component implementation

The Component Zero application is akin to the "_hello world_" app of Streamlit components. The component takes a text input and sends it to the Streamlit application to display it.

I find it's helpful to see things stripped down to their bare essentials to understand them. So, here I will implement a simple component in a single HTML/JavaScript file, and include just enough structure to make it generally useful. I won't use a front end framework like React, Next.js, Babel, Webpack, etc. Minimal bi-directional communication will be supported between the component and Streamlit.

### Capabilities

The diagram below depicts what will be implemented. The main takeaway is that _the Streamlit app server and front end web server are not separate_, because the component doesn't require it. The component implementation is in a plain HTML/JavaScript file, loaded and executed directly by the Streamlit server.

![capabilities-zero-app](./images/capabilities-zero-app.png)

### Architecture

The architecture view captures the relationships betwen the capabilities, shedding light on how the application works.

![structure-zero-app](./images/structure-zero-app.png)

### Application start up sequence

The sequence diagram explains in more detail exactly how the interactions between the capabilities take place.

![startup-sequence-zero-app](./images/startup-sequence-zero-app.png)

### Component Zero implementation details

Let's take a look at Component Zero's front end implementation in the `./frontend/` folder. There are two files here, `__init__.py` and `index.html`.

**`./frontend/__init__.py`**

This code (the presence of `__init__.py` makes it a Python module, actually) simply declares the component using Streamlit's `components.declare_component` API and exports a handle to it. This handle is `component_zero`. You can see the `path` to the component is the same folder. When Streamlit loads the component it will serve the default `index.html` file from this location.

```python
import streamlit.components.v1 as components
component_zero = components.declare_component(
    name='component_zero',
    path='./frontend'
)
```

**`./frontend/index.html`**

This self-contained file does the following:

1. Draws a simple HTML user interface
2. Loads JavaScript which implements core Streamlit component life cycle actions, namely the ability to:
- Inform Streamlit client that the component is ready, using `streamlit:componentReady` message type.
- Calculate or get it's own visible screen height, and inform Streamlit client, using `streamlit:setFrameHeight` message type.
- Handle inbound `message` events from the Streamlit client; with `streamlit:render` event type being critical.
- Send values (i.e., objects) to the Streamlit client application, using `streamlit:setComponentValue` message type.

In this basic component, notice `_sendMessage()` function uses `window.parent.postMessage()`, which is as fundamental as it gets. The value objects you send to the Streamlit client application must be any JSON serializable object. Conceptually they can be viewed as data or events carrying a data payload. Inbound message values received on `streamlit:render` events, are automatically de-serialized to JavaScript objects.

It's only illustrative, but I have also implemented a simple pipeline of inbound message handlers and a dispatcher. I show this being used to initialize component data values, update the user interface, and to log output to the console. See `*_Handler` functions, `pipleline`, `initialize()` function.

```javascript
<style>
    <!-- removed for brevity (see GitHub repo) --> 
</style>

<html>
<body>

  <!-- Set up your HTML here -->
  <h1>Component</h1>
  <div>
    <input id="text_input" value="" placeholder="Enter some text"/>
  </div>
  <div id="message_div">
    <br/><span id="message_label">__</span>
  </div>

  <script>
    // ----------------------------------------------------
    // Use these functions as is to perform required Streamlit 
    // component lifecycle actions:
    //
    // 1. Signal Streamlit client that component is ready
    // 2. Signal Streamlit client to set visible height of the component
    //    (this is optional, in case Streamlit doesn't correctly auto-set it)
    // 3. Pass values from component to Streamlit client
    //

    // Helper function to send type and data messages to Streamlit client

    const SET_COMPONENT_VALUE = "streamlit:setComponentValue"
    const RENDER = "streamlit:render"
    const COMPONENT_READY = "streamlit:componentReady"
    const SET_FRAME_HEIGHT = "streamlit:setFrameHeight"

    function _sendMessage(type, data) {
      // copy data into object
      var outData = Object.assign({
        isStreamlitMessage: true,
        type: type,
      }, data)

      if (type == SET_COMPONENT_VALUE) {
        console.log("_sendMessage data: " + JSON.stringify(data))
        console.log("_sendMessage outData: " + JSON.stringify(outData))
      }
      
      window.parent.postMessage(outData, "*")
    }

    function initialize(pipeline) {

      // Hook Streamlit's message events into a simple dispatcher of pipeline handlers
      window.addEventListener("message", (event) => {
        if (event.data.type == RENDER) {
          // The event.data.args dict holds any JSON-serializable value
          // sent from the Streamlit client. It is already deserialized.
          pipeline.forEach(handler => {
            handler(event.data.args)
          })
        }
      })

      _sendMessage(COMPONENT_READY, {apiVersion: 1});

      // Component should be mounted by Streamlit in an iframe, so try to autoset the iframe height.
      window.addEventListener("load", () => {
        window.setTimeout(function() {
          setFrameHeight(document.documentElement.clientHeight)
        }, 0)
      })

      // Optionally, if auto-height computation fails, you can manually set it
      // (uncomment below)
      //setFrameHeight(200)
    }

    function setFrameHeight(height) {
      _sendMessage(SET_FRAME_HEIGHT, {height: height})
    }

    // The `data` argument can be any JSON-serializable value.
    function sendData(data) {
      _sendMessage(SET_COMPONENT_VALUE, data)
    }

    // ----------------------------------------------------
    // Now implement the the custom functionality of the component:

    let textInput = document.getElementById("text_input")
    textInput.addEventListener("change", () => {
      sendData({
        value: textInput.value,
        dataType: "json",
      })
    })

    let msgLabel = document.getElementById("message_label")

    // ----------------------------------------------------
    // Define a pipeline of inbound property handlers

    // Set initial value sent from Streamlit!
    function initializeProps_Handler(props) {
      if (textInput.value == "") {
        textInput.value = props.initial_state.message
      }
    }
    // Access values sent from Streamlit!
    function dataUpdate_Handler(props) {
        msgLabel.innerText = `Update [${props.counter}] at ${props.datetime}`
    }
    // Simply log received data dictionary
    function log_Handler(props) {
      console.log("Received from Streamlit: " + JSON.stringify(props))
    }

    let pipeline = [initializeProps_Handler, dataUpdate_Handler, log_Handler]

    // ----------------------------------------------------
    // Finally, initialize component passing in pipeline

    initialize(pipeline)

  </script>
</body>
</html>
```

The counterpart to the front end is the Streamlit application. It's entry point is in `app.py`. The `frontend` module is imported and the component handle, `component_zero`, is used to create an instance of it. Interactions in the front end which give rise to value notifications will be received in the Streamlit client, which can be acted upon as required. I've provided simple design abstractions to make running of the component and handling its return values more explicit. They are `run_component()` and `handle_event()` respectively. This _wrapping_ makes the implementation neater and it'll be conceptually easier to understand the implementation of Component Hero which we will discuss in the next section.

**`app.py`**

```python
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
        'initial_state': {'message': 'Hello! Enter some text' },
        'counter': st.session_state.counter,
        'datetime': str(datetime.now().strftime("%H:%M:%S, %d %b %Y"))
    }

    handle_event(run_component(props))   

if __name__ == '__main__':
    main()
```

### Running Component Zero

Component Zero is run in the same way as any Streamlit app.

- Open a console window and change directory to the root folder, where `app.py` is. If you've cloned the GitHub repo, then this will be in `./components/zero`.
- Now run the Streamlit server with this app.

```
$ streamlit run app.py
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8765
  Network URL: http://192.168.1.100:8765
```

- The app should start on the default port (8765) and launch a browser window to display the following page:

![component-zero-screenshot](./images/component-zero-screenshot.png)

## Component Hero: a more sophisticated component

The Component Hero application takes the Zero component's design to the next level. The design includes a useful wrapper for `components.declare_component` API, which I refer to as the _component host_ or _Streamlit host_. This vocabulary allows me to make the distinction between Streamlit code which specifically hosts the component and Streamlit code for the rest of the application, which I like to refer to as the _Streamlit client_.

In this application I will use React (Next.js), JavaScript and HTML to implement a component using current best practices and design patterns. The goal is to develop a component template that I can reuse and extend to integrate Auth0 authentication with Streamlit apps.

## Component Hero demo

Component Hero's use case is a password-protected multi-page Streamlit app. Instead of using Auth0 authentication just yet, I will fake the authentication with a probabilistic password guess generator, that has a high chance of generating the correct password after just a few attempts. The Streamlit client provides the multi-page app implementation and the Streamlit host plus front end component provides the (fake) authentication.

![component-hero-demo](./images/component-hero-demo.gif)

In the next article, I will improve Component Hero, with very few changes to the architecture, and integrate real authentication using Auth0's Next.js SDK. (Needless to say, it will be called _Component Auth0_!).

### Capabilities

The diagram below shows what will be implemented. The main takeaway is that _the Streamlit app server and front end web server run as two separate server-based applications_. The component implementation cannot be run in Streamlit's server, so must be executed in its own process and web server. I run Streamlit locally on port 4010 and the front end locally on port 3001. You can do the same to make it easier to reuse the code and follow the design.

![capabilities-hero-app](./images/capabilities-hero-app.png)

### Architecture

The architecture view captures the relationships betwen the capabilities, shedding light on how the application works.

![structure-hero-app](./images/structure-hero-app.png)

### Application start up sequence

The sequence diagram explains in more detail exactly how the interactions between the capabilities take place.

![startup-sequence-hero-app](./images/startup-sequence-hero-app.png)

### Component Hero implementation details

_TODO_

#### Setting up the dev environment

_TODO_

#### Frontend Next.js component implementation

_TODO_

#### Backend (Streamlit) component host implementation

_TODO_

#### Backend (Streamlit) component message handler implementation

_TODO_

#### Putting it all together

_TODO_

##### Running the front end

_TODO_

##### Running the backend

_TODO_

# End notes

## Jupyter vs Streamlit

Some of you may be wondering if you can you use Streamlit instead of Jupyter Notebooks?

### Streamlit is not a single file only approach to app development
* Single file apps are great for getting started. But as your app grows you must re-factor the project into folders/files/modules/packages. You then import whatever you need in your main app.py file.
* Hot-reloading on deeply nested modules is a bit flaky though (but will you really have deeply nested modules in a simple app?). See [issue 366](https://github.com/streamlit/streamlit/issues/366)

### The Streamlit dev workflow is much more efficient than Jupyter Notebook's
* You work in an efficient editor.
* The iterative cycle of change-run-evaluate is fast and automated in Streamlit.
* You naturally evolve towards quality code modules and a working app being the final deliverable, not a Notebook which further conversion required to build an app.
* More with less - Streamlit is much easier, efficient and productive.
* Streamlit solves all the problems of Notebooks pointed out by Joel Grus in [I don’t like notebooks](https://www.youtube.com/watch?v=7jiPeIFXb6U).
* _Jupyter Notebooks for Visual Studio Code_ addresses some of the failings of native JNs. See [this video](https://www.youtube.com/watch?v=FSdIoJdSnig) for details.

### The product produced by Streamlit is much nicer than a Notebook
* You can control the output of your code, markdown and results.
* You don’t have those clunky code cells.
* You don’t spend tons of time googling and trying out how to use nbformatter.
* Finished dashboard-like products are easy to make.

### How about the software development experience?
* You seldom want to show people the numerous intermediate code steps in a notebook. From a literate programming perspective, code cells with many lines of boiler-plate Pandas or Matplotlib code are distracting.
* With Streamlit you can show selected parts of your code (which simultaneously get executed!) using `st.echo()`.
* Running the full app during hot-reload is a great feature keeping all state aligned as expected. With notebooks it's very easy to get confused about which cells have run and in which order.
* Notebook re-runs can take forever compared to Streamlit, because of data and python compilation caching, so fast iterations come easily.
* The hassles of managing notebook kernels, Jupyter extensions etc. mean you can spend a lot of time on Google and Stack overflow looking for solutions.
* In the end you need to deploy solutions. Streamlit is yet another web app, so easy to deploy to Azure, Heroku, AWS, etc.

### In favour of Jupyter notebooks
* The larger community, larger library of widgets and export to pdf functionality.
* Notebooks still provide the best environment for ad-hoc exploratory data analysis.

## My impressions of Streamlit

* On the curve of _data-analytics-ease-of-use_, the use case for Streamlit apps lies somewhere between Power BI/Tableau on the high end and Jupyter Notebooks in the middle; with regular Python/R programming sitting towards the low end.
    * Almost everything you can do in Python is available to the developer in Streamlit.
    * It's powerful enough already to be ideal for small to medium data science-rich business solutions and experimental or exploratory analytics.
    * As with Jupyter Notebooks, literate programming (not in the true Knuth sense) is easy, because Streamlit comes with native Markdown and Latex support.
* A design principle of Streamlit is that there's just enough (and not more) UI functionality out-of-the-box to make serious, small, specific custom web apps.
    * This addresses 80% of a data science worker's needs.
    * I've used it quite a bit in small AI/ML experiments and really appreciate being able to quickly create a UI to view results and control the experiments.
    * Some say Streamlit is the _React or Shiny for Python_ - I think we're some way from that (ObservableHQ would be a closer fit). There's a decent discussion going on [here](https://github.com/streamlit/streamlit/issues/327).
* The code is developed and debugged in VS Code (with Python extensions)
    * Streamlit supports hot-reloading and native data caching, making the framework super-productive for iterative AI/ML app experiments.
    * The app state is always consistent because the code is executed from the top whenever any change event is raised. That sounds awfully slow, but it isn't in practice - remember the primary use case is supposed to be about building _simple UI_ for simple _data analysis tools_, and native data caching helps with speed a lot.
    * You can run apps normally in the console even though they contain some Streamlit UI magic in the source code.

Quote from Adrien Treuille: "We ourselves use Jupyter alongside Streamlit, _so they don’t exclude one another at all_. Jupyter, we feel, is _centered on the EDA workflow - exploratory data analysis workflow_ - and it’s a fantastic tool for that... And then it sort of branched out into making apps a little bit more, being an expository tool of various kinds... And those are all great, adjacent use cases. Streamlit was really founded on the idea of building interactive apps really easily. So we have a different workflow; I think it’s very, very _simple_, it’s very _lightweight_, it’s _super-easy to understand_, and it’s _slightly difficult to describe_. **You just have to try it**. In essence, we allow you to sprinkle these interactive widgets throughout your code, and then we sort of organize it into an app very easily. I think it’s that simplicity that the community has really responded to."

# Resources

- [Awesome Streamlit Docs](https://awesome-streamlit.readthedocs.io/en/latest/index.html)
- [Awesome Streamlit App Gallery](https://awesome-streamlit.org/)
- [Streamlit Discussion Forum](https://discuss.streamlit.io/)
- [Will Streamlit cause the extinction of Flask?](https://towardsdatascience.com/part-2-will-streamlit-cause-the-extinction-of-flask-395d282296ed)
- [CSS Hacks!](https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/23)

# Videos

- [1/4: What is Streamlit](https://www.youtube.com/watch?v=R2nr1uZ8ffc)
- [2/4: Install and play with Streamlit](https://www.youtube.com/watch?v=sxLNCDnqyFc)
- [3/4: Let's build a data app!](https://www.youtube.com/watch?v=VtrFjkSGgKM)
- [4/4 Self-driving use-case](https://www.youtube.com/watch?v=z8vgmvtgxCs)
- [Streamlit Tutorials](https://www.youtube.com/playlist?list=PLgkF0qak9G4-TC9_tKW1V4GRcJ9cdmnlx)