import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { PythonProvider, usePython } from 'react-py';

function App() {
  const { runPython, output } = usePython();

  const handleClick = () => {
    runPython('print("Hello from Python!")');
  };

  return (
    <PythonProvider>
     <button onClick={handleClick}>Run Python</button>
     <pre>{output}</pre>
    </PythonProvider>
  )
}

export default App
