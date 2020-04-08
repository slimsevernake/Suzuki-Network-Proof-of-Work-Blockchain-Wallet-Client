import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import logo from "../assets/geo.png"
import { ROOT_PATH } from "../config.js"

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${ROOT_PATH}/wallet/info`)
      .then(res => res.json())
      .then(json => setWalletInfo(json));
  }, []) // set empty arr to prevent infinite rerender
  let {Address, Balance} = walletInfo
  return (
    <div className="App">
      <img className="logo" src={logo} alt="application-logo" />
      <h3>Welcome to the Suzuki Block Explorer</h3>
      <br />
      <Link to="/blockchain">Blockchain Explorer</Link>
      <Link to="/transact">Conduct a Transaction</Link>
      <Link to="/transactions">View Pending Transactions</Link>
      <div className="WalletInfo">
        <div>Address: {Address}</div>
        <div>Balance: {Balance}</div>
      </div>
    </div>
  );
}

export default App;
