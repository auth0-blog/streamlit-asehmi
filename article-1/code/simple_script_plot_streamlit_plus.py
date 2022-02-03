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
    c1, c2 = st.columns(2)
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
