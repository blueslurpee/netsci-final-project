from contracts import CONTRACTS

import os
import time

import requests
import csv

from dotenv import load_dotenv

load_dotenv()

for contract in CONTRACTS:
    transactions = []
    total_pages = 0
    trailing_block = 0
    terminus_block = 13730174

    while trailing_block != terminus_block:
        print(f"In set from block: {trailing_block}")
        start_block = trailing_block
        for page in range(1, 11):
            params = {
                'module': 'account',
                'action': 'tokennfttx',
                'contractaddress': CONTRACTS[contract],
                'page': page,
                'offset': 1000,
                'startblock': start_block,
                'endblock': terminus_block,
                'sort': 'asc',
                'apikey': os.environ['ETHERSCAN_API_KEY']
            }

            print(f"Requesting page {page} after a 0.5 second sleep")
            time.sleep(0.5)
            r = requests.get('https://api.etherscan.io/api', params=params)
            fresh_transactions = r.json()['result']

            try:
                if not fresh_transactions:
                    trailing_block = terminus_block
                    break

                transactions += fresh_transactions
                total_pages += 1
                trailing_block = fresh_transactions[-1]["blockNumber"]
            except IndexError:
                trailing_block = terminus_block
                break

    f = csv.writer(open(f"./transfers/{contract}.csv", "w+"))

    # Header row
    f.writerow([
        "blockNumber",
        "timeStamp",
        "hash",
        "nonce",
        "blockHash",
        "from",
        "contractAddress",
        "to",
        "tokenID",
        "tokenName",
        "tokenSymbol",
        "tokenDecimal",
        "transactionIndex",
        "gas",
        "gasPrice",
        "gasUsed",
        "cumulativeGasUsed",
        "input",
        "confirmations"
    ])

    for transaction in transactions:
        f.writerow([
            transaction["blockNumber"],
            transaction["timeStamp"],
            transaction["hash"],
            transaction["nonce"],
            transaction["blockHash"],
            transaction["from"],
            transaction["contractAddress"],
            transaction["to"],
            transaction["tokenID"],
            transaction["tokenName"],
            transaction["tokenSymbol"],
            transaction["tokenDecimal"],
            transaction["transactionIndex"],
            transaction["gas"],
            transaction["gasPrice"],
            transaction["gasUsed"],
            transaction["cumulativeGasUsed"],
            transaction["input"],
            transaction["confirmations"]
        ])

    print(f"Successfully streamed {len(transactions)} {contract} transactions from {total_pages} pages to csv.")
