import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ROOT_PATH } from "../config.js" 

function Transact() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState("");

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
            </div>
        </div>
    )
}
export default Transact


