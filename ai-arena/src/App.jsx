import React, { useState, useEffect } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import "./App.css";
import { oneDark } from "@codemirror/theme-one-dark";

import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

import startCode from "./start.txt";
import endCode from "./end.txt";
import baseCode from "./baseCode.txt"
import startVersusCode from "./startVersusCode.txt";
import endVersusCode from "./endVersusCode.txt";


const loadSkulpt = () => {
  return new Promise((resolve, reject) => {
    const script1 = document.createElement("script");
    const script2 = document.createElement("script");

    script1.src = "https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt.min.js";
    script2.src = "https://cdn.jsdelivr.net/npm/skulpt@1.2.0/dist/skulpt-stdlib.min.js";

    script1.onload = () => {
      script2.onload = resolve;
      document.body.appendChild(script2);
    };

    script1.onerror = reject;
    script2.onerror = reject;

    document.body.appendChild(script1);
  });
};

const App = () => {
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [pythonCode, setPythonCode] = useState("print('Hello World!')");
  const [preCode, setPreCode] = useState("")
  const [postCode, setPostCode] = useState("")
  const [preVersusCode, setPreVersusCode] = useState("");
  const [postVersusCode, setPostVersusCode] = useState("");
  const [tab, setTab] = useState("lossRate")

  useEffect(() => {
    loadSkulpt().catch(() => {
      setError("Failed to load Skulpt");
    });

    fetch(startCode)
        .then(r => r.text())
        .then(text => {
          setPreCode(text)
        });

    fetch(endCode)
    .then(r => r.text())
    .then(text => {
      setPostCode(text)
    });

    fetch(baseCode)
    .then(r => r.text())
    .then(text => {
      setPythonCode(text)
    });

    fetch(startVersusCode)
        .then(r => r.text())
        .then(text => {
          setPreVersusCode(text)
        });

    fetch(endVersusCode)
    .then(r => r.text())
    .then(text => {
      setPostVersusCode(text)
    });

  }, []);

  const runPython = (codeType) => {
    if (window.Sk) {
      const Sk = window.Sk;

      let combinedCode;
      if (codeType == "loss") combinedCode = `${preCode}\n${pythonCode}\n${postCode}`;
      if (codeType == "versus") combinedCode = `${preVersusCode}\n${pythonCode}\n${postVersusCode}`;
      
      Sk.configure({
        output: (text) => {
          console.log(text);
          setOutput(JSON.parse(text))
        
        },
        
          read: (x) => {
          if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined) {
            throw new Error(`File not found: '${x}'`);
          }
          return Sk.builtinFiles["files"][x];
        },
      });

      setOutput(""); 
      Sk.misceval
        .asyncToPromise(() => Sk.importMainWithBody("<stdin>", false, combinedCode, true))
        .catch((err) => setError(err.toString()));
    } else {
      setError("Skulpt is not loaded yet!");
    }
  };


  return (
    <div id="site-container">

      <div id="site-header">
        <div id="header-title">
          <h2>Cos 498 AI Arena</h2>
          <h5>Created by Sophie Walden</h5>
        </div>
        <div id="header-button-holder">
          <button className="versus-button header-button" onClick={() => setTab("versus") || runPython("versus")}>Versus</button>
          <button className="loss-rate-button header-button" onClick={() => setTab("lossRate") || runPython("loss")}>Test Loss Rate</button>
          <button disabled className="battle-button header-button" onClick={() => setTab("watchBattle") || runPython()}>Watch Battle</button>
        </div>
      </div>
      <div id="site-content">
        <CodeMirror
          className="codeMirror"
          value={pythonCode}
          extensions={[python()]}
          theme={oneDark}
          onChange={(value) => setPythonCode(value)}
        />
        <div className="output-container">
          <div id="versus" className={`${tab == 'versus' ? '' : "hiddenTab"}`}>
            <div className="win-rate-display">
                  <h4>Out of 100 battles, your heuristic won...</h4>
                  
                  <div className="circle-results">
                    <CircularProgressbar 
                      styles={buildStyles({
                        strokeLinecap: 'butt',
                        pathTransitionDuration: 4.5,
                        textColor: '#f88',
                        trailColor: '#AA4A44',
         
                      })}
                    value={output.playerTwoWins ? output.playerTwoWins : 0} text={`${output.playerTwoWins}`} maxValue={100} />
                  </div>
              </div>

            <div id="versus-error-display">
              
              <div className="error-rate-display"> 
                  <h4>Zero Guesser Heuristic Error</h4>
                  
                  <div className="circle-results">
                    <CircularProgressbar 
                      styles={buildStyles({
                        pathTransitionDuration: 4.5,
                      })}
                    value={output.playerOneError ? output.playerOneError : 0} text={`${Math.round(output.playerOneError*100, 2)/100}`} maxValue={1} />
                  </div>
                </div>

                <div className="error-rate-display"> 
                  <h4>Your Heuristic Error</h4>
                  
                  <div className="circle-results">
                    <CircularProgressbar 
                      styles={buildStyles({
                        pathTransitionDuration: 4.5,
                      })}
                    value={output.playerTwoError ? output.playerTwoError : 0} text={`${Math.round(output.playerTwoError*100, 2)/100}`} maxValue={1} />
                  </div>
                </div>

                </div>
          </div>
          <div id="loss-rate" className={`${tab == 'lossRate' && output.error1 ? '' : "hiddenTab"}`}>
            <h2>Results</h2>

            <div id="results-page">
                <div className="error-rate-display"> 
                  <h4>Team 1 Average Error Rate</h4>
                  
                  <div className="circle-results">
                    <CircularProgressbar 
                      styles={buildStyles({
                        pathTransitionDuration: 4.5,
                      })}
                    value={output.error1 ? output.error1 : 0} text={`${Math.round(output.error1*100, 2)/100}`} maxValue={1} />
                  </div>
                </div>

                <div className="error-rate-display"> 
                  <h4>Team 1 Average Error Rate</h4>
                  
                  <div className="circle-results">
                    <CircularProgressbar 
                      styles={buildStyles({
                        pathTransitionDuration: 4.5,
                      })}
                    value={output.error2 ? output.error2 : 0} text={`${Math.round(output.error2*100, 2)/100}`} maxValue={1} />
                  </div>
                </div>

              </div>
              {error && <p style={{ color: "red" }}>Error: {error}</p>}
            </div>
            
            
            
            <div id="watch" className={`${tab == 'watchBattle' ? '' : "hiddenTab"}`}>

            </div>
        </div>
      </div>
     
      
    </div>
  );
};

export default App;
