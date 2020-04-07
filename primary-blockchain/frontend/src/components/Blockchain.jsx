import React, { useState, useEffect } from 'react'
import { ROOT_PATH } from "../config.js"
import Block from "./Block.jsx"

const PAGINATION_RANGE = 3;

function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLen, setBlockchainLen] = useState(0);
    
    const fetchNewPage = ({ start, end }) => {
        fetch(`${ROOT_PATH}/blockchain/range?start=${start}&end=${end}`)
            .then(res => res.json())
            .then(json => setBlockchain(json));
    }

    useEffect(() => {
        fetchNewPage({ start: 0, end: PAGINATION_RANGE });

        fetch(`${ROOT_PATH}/blockchain/length`)
            .then(res => res.json())
            .then(json => setBlockchainLen(json));
    }, []);

    const pages = [];
    for (let i=0; i < blockchainLen/PAGINATION_RANGE; i++) {
        pages.push(i)
    }
    
    return (
        <div className="Blockchain">
            <h3>Blockchain</h3>
            <div>
                {blockchain.map(block => (
                    <Block key={block.hash} block={block} />
                ))}
            </div>
            <div>
                {
                    pages.map(page => {
                        /* set cursor => every click, jumps by range 
                            e.g. page=0, start at block 0, end at 3; 
                            page=1, start at block 3, end at 6; 
                        */
                        const start = page * PAGINATION_RANGE
                        const end = (page + 1) * PAGINATION_RANGE
                        return (
                            <span key={page} onClick={() => fetchNewPage({start, end})}>
                                <button>
                                    {page+1}
                                </button>{" "}
                            </span>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Blockchain

// // view all/depaginated mode
        // fetch(`${ROOT_PATH}/blockchain`)
        //     .then(res => res.json())
        //     .then(json => setBlockchain(json));
        // fetch len of blockchain for pagination