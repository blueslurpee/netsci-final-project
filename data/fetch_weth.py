from contracts import CONTRACTS

import os
import time

import pandas as pd
from tqdm import tqdm

import requests
import csv

from dotenv import load_dotenv

load_dotenv()

transactions = []
total_pages = 0

contract_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

collated_data = pd.read_csv(f"./collated/hashmasks.csv")
blocks = collated_data['blk_number'].tolist()

for block in tqdm(range()):
    print(f"In block: {block}")
    for page in range(1, 11):
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': contract_address,
            'page': page,
            'offset': 1000,
            'startblock': block,
            'endblock': block,
            'sort': 'asc',
            'apikey': os.environ['ETHERSCAN_API_KEY']
        }

        print(f"Requesting page {page} after a 0.5 second sleep")
        time.sleep(0.5)
        r = requests.get('https://api.etherscan.io/api', params=params)
        fresh_transactions = r.json()['result']

        try:
            transactions += fresh_transactions
            total_pages += 1
            trailing_block = fresh_transactions[-1]["blockNumber"]
        except IndexError:
            break

f = csv.writer(open(f"./weth/all.csv", "w+"))

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
    "value",
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
        transaction["value"],
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

print(f"Successfully streamed {len(transactions)} weth transactions from {total_pages} pages to csv.")
