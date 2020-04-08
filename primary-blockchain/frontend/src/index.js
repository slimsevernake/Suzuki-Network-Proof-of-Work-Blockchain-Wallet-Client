import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import './index.css';
import App from './components/App.jsx';
import Blockchain from "./components/Blockchain.jsx"
import Transact from "./components/Transact.jsx"
import Transaction from './components/Transaction';

ReactDOM.render(
  <Router history={createBrowserHistory()}>
    <Switch>
      <Route exact path="/" component={App}/>
      <Route path="/blockchain" component={Blockchain}/>
      <Route path="/transact" component={Transaction}/>
    </Switch>
  </Router>,
  document.getElementById('root')
);
