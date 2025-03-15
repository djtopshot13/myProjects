import React from 'react';
import logo from './logo.svg';
import './App.css';
import Button from './components/button';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Button style={{backgroundColor:'blue', fontSize:20, color:'white'}} children='Click Me'></Button>
    </div>
  );
}

export default App;
