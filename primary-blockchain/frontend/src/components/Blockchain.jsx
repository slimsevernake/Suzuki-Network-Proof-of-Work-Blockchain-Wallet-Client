import React, { useState, useEffect } from 'react'
import { ROOT_PATH } from "../config.js"

function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);

    useEffect(() => {
        fetch(`${ROOT_PATH}/blockchain`)
            .then(res => res.json())
            .then(json => setBlockchain(json))
            
    }, []);

    return (
        <div className="Blockchain">
            <h3>Blockchain</h3>
            <div>
                {
                    blockchain.map(block => (
                        <div key={block.hash}>{JSON.stringify(block)}</div>
                    ))
                }
            </div>
        </div>
    )
}

export default Blockchain