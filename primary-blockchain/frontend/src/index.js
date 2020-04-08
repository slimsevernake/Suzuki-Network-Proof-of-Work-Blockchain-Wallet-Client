import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom';
import './index.css';
import history from "./history.js"  
import App from './components/App.jsx';
import Blockchain from "./components/Blockchain.jsx"
import Transact from "./components/Transact.jsx"
import Pool from './components/Pool.jsx';

ReactDOM.render(
  <Router history={history}>
    <Switch>
      <Route exact path="/" component={App}/>
      <Route path="/blockchain" component={Blockchain}/>
      <Route path="/transact" component={Transact}/>
      <Route path="/transactions" component={Pool}/>
    </Switch>
  </Router>,
  document.getElementById('root')
);
