import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Transaction from "./Transaction.jsx";
import { ROOT_PATH } from "../config.js";

const Pool = () => {
    const [tx, setTx] = useState([]);

    useEffect(() => {
        fetch(`${ROOT_PATH}/transactions`)
            .then(res => res.json())
            .then(json => setTx(json));
    }, []);

    return (
        <div className="TransactionPool">
            <Link to="/">Home</Link>
            <hr />
            <h3>Transaction Pool</h3>
            <div>
                {tx.map(transaction => (
                    <div key={transaction.id}>
                        <hr />
                        <Transaction transaction={transaction} />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Pool;