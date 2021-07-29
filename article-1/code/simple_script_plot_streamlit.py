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
