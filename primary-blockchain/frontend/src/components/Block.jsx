import React, { useState } from 'react';
import { MILLISECONDS_PY } from "../config.js"; 
import Transaction from "./Transaction.jsx";


function TxDisplay({ block }) {
    const [displayTx, setDisplayTx] = useState(false);
    const { data } = block;

    const toggleTxDisplay = () => {
        setDisplayTx(!displayTx);
    }
    // if Tx data exists, default to display
    if (displayTx) {
        return (
            <div>
                {data.map(tx => (
                    <div key={tx.id}>
                        <hr />
                        <Transaction transaction={tx} />
                    </div>
                ))}
                <br />
                <button onClick={toggleTxDisplay}>Show Less</button>
            </div>
        )
    }
    return (
        <div>
            <br />
            <button onClick={toggleTxDisplay}>Show More</button>
        </div>
    )
    
}


function Block({ block }) {
    const { timestamp, hash } = block;
    const hash_readable = `${hash.substring(0, 15)}...`
    const timestamp_readable = new Date(timestamp / MILLISECONDS_PY).toLocaleString();

    return (
        <div className="Block">
            <div>Hash: {hash_readable}</div>
            <div>Timestamp: {timestamp_readable}</div>
            <TxDisplay block={block} />
        </div>
    )
}

export default Block 