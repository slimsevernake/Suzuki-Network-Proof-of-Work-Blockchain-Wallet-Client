import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { ROOT_PATH } from "../config.js";
import history from "../history.js";

function Transact() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState("");
    const [knownAddresses, setKnownAddresses] = useState([]);

    useEffect(() => {
        fetch(`${ROOT_PATH}/known-addresses`)
            .then(res => res.json())
            .then(json => setKnownAddresses(json))
    }, []);
    
    const updateRecipient = event => {
        setRecipient(event.target.value)
    }

    const updateAmount = event => {
        setAmount(Number(event.target.value))
    }

    const submitTransaction = () => {
        fetch(`${ROOT_PATH}/wallet/transact`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipient, amount })
        }).then(res => res.json()).then(json => {
            console.log("here", json);
            alert("Success");

            history.push("/transactions");
        })
    }

    return (
        <div className="ConductTransaction">
            <Link to="/">Home</Link>
            <hr />
            <h3>Conduct a Transaction</h3>
            <br />
            <div>
                <div>
                    <div className="form-group">
                        <input type="text" placeholder="recipient" value={recipient} onChange={updateRecipient} className="form-control"/>
                        <small className="text-muted form-text">Ensure the recipient address is correct.</small>
                    </div>

                    <div className="form-group">
                        <input type="number" placeholder="amount" value={amount} onChange={updateAmount}  className="form-control"/>
                    </div>
                    <button type="submit" className="btn btn-primary" onClick={submitTransaction}>
                        Submit
                    </button>
                    
                </div>
                <br />
                <h4>Known Addresses</h4>
                <div>
                {
                    knownAddresses.map((address, i) => (
                        <span key={address}>
                        <u>{address}</u>{(i !== address.length - 1) ? ", " : ""}
                        </span>
                    )
                    
                    )
                }
                    
                </div>
            </div>
        </div>
    )
}
export default Transact


