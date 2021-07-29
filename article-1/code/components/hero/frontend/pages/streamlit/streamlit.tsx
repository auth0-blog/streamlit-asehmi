import React, { useState, useEffect } from 'react'
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from 'streamlit-component-lib'
import MyButton from '../../components/MyButton'

const FRAME_HEIGHT = 85

const StreamlitComponent = (props: ComponentProps) => {

  console.log('======== Streamlit component ========')

  // inbound
  const [hostname, setHostname] = useState('None')
  const [password, setPassword] = useState('None')

  // outbound
  const [message, setMessage] = useState('Generate a password guess to log in.')
  const [passwordGuess, setPasswordGuess] = useState('')
  const [token, setToken] = useState(false)
  const [state, setState] = useState({
    hostname: hostname, passwordGuess: null, token: token, message: message, isError: false, error: null
  })

  // Misc
  const [count, setCount] = useState(0)

  const attempts = [' \\ ','--',' / ',' | ']

  const initializeProps = async (props: ComponentProps) => {
    if ('hostname' in props.args && 'initial_state' in props.args) {
      console.log('STC initializeProps')
      setHostname(props.args.hostname)
      setPassword(props.args.initial_state['password'])
      delete props.args.hostname
      delete props.args.initial_state
    }
  }

  const sendEvent = async (name: string, data: any) => {
    if (props.args.events.includes(name)) {
      Streamlit.setComponentValue({ name: name, data: data })
    } else {
      Streamlit.setComponentValue({ name: 'onError', data: data })
    }
  }

  const updateStateAndNotifyHost = async (
    state: { hostname: string, passwordGuess: string, token: boolean, message: string, isError: boolean, error: string } = null
  ) => {
    try {
      setState(state)
      await sendEvent('onStatusUpdate', state)
    } catch (err) {
      console.log(`updateStateAndNotifyHost error: ${err}`)
    }
  }

  useEffect(() => {
    const newState = {
      hostname: hostname,
      passwordGuess: passwordGuess,
      token: token,
      message: message,
      isError: false,
      error: null,
    }
    updateStateAndNotifyHost(newState)
  }, [passwordGuess])

  // One shot initializer for props
  useEffect(() => {
    initializeProps(props)
    Streamlit.setFrameHeight(FRAME_HEIGHT)
  }, [])

  // ----------------------------------------------------

  const generatePasswordGuess = async () => {
    const index = Math.random() * password.length
    const guess = password.substring(0, index) + '_' + password.substring(index + 1)
    // force the guess to be correct "sometimes"
    if (index < password.length / 3) {
      setMessage('Success! Logged in.')
      setPasswordGuess(password)
      setToken(true)
      setCount(0)
    // otherwise make it incorrect
    } else {
      setCount(count+1)
      setMessage('Try again? (' + attempts[3 - count % 4] + ')')
      setPasswordGuess(guess)
      setToken(false)
    } 
  }

  const logout = async () => {
    setMessage('Generate a password guess to log in.')
    setPasswordGuess('')
    setToken(false)
    setCount(0)
    return passwordGuess
  }

  // ----------------------------------------------------

  return (
    <header>
      <div className="text-xs text-indigo-700">
        {hostname}{' | '}{message}
      </div>
      <div className="container my-4 ml-1 max-w-xl space-x-4">
        {!token && (<MyButton label='Generate password guess' onClickHandler={generatePasswordGuess} props={props} />)}
        {token && (<MyButton label='Logout' onClickHandler={logout} props={props} />)}
      </div>
    </header>
  )
}

export default withStreamlitConnection(StreamlitComponent)
