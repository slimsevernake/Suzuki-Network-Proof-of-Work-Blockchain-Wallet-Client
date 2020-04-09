import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Transaction from "./Transaction.jsx";
import { ROOT_PATH, SECONDS_JS } from "../config.js";
import history from "../history.js";

const POLL_INTERVAL = 10 * SECONDS_JS;

const Pool = () => {
    const [tx, setTx] = useState([]);
    const fetchTx = () => {
        fetch(`${ROOT_PATH}/transactions`)
            .then(res => res.json())
            .then(json => setTx(json));
    }

    useEffect(() => {
        fetchTx();
        // poll to keep pool updated, clear 
        const poll = setInterval(fetchTx, POLL_INTERVAL);
        // clear when unmount so interval isn't trying to set unmounted state
        return () => clearInterval(poll)
    }, []);

    const mineBlock = () => {
        fetch(`${ROOT_PATH}/blockchain/mine`)
            .then(() => {
                alert("Success.");

                history.push("/blockchain");
            })
    }

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
            <hr />
            <button className="btn btn-primary" onClick={mineBlock}>
                Mine a block.
            </button>
        </div>
    )
}

export default Pool;