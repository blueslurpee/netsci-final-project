import requests
import csv

CONTRACTS = {
    'hashmasks': '0xC2C747E0F7004F9E8817Db2ca4997657a7746928'
}

for contract in CONTRACTS:
    transactions = []
    page = 1

    while True:
        params = {
            'module': 'account',
            'action': 'tokennfttx',
            'contractaddress': CONTRACTS[contract],
            'page': page,
            'offset': 1000,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': API_KEY
        }

        # TODO for second phase - all transactions
        # params = {
        #     'module': 'account',
        #     'action': 'txlist',
        #     'address': CONTRACTS[contract],
        #     'page': page,
        #     'offset': 1000,
        #     'startblock': 0,
        #     'endblock': 99999999,
        #     'sort': 'asc',
        #     'apikey': 'W7CV57WIU5BB2CBNTFZB573VFP8XPGI8EV'
        # }

        r = requests.get('https://api.etherscan.io/api', params=params)
        fresh_transactions = r.json()['result']

        if fresh_transactions is not None:
            transactions += r.json()['result']
            page += 1
        else:
            break

    f = csv.writer(open(f"{contract}.csv", "w+"))

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

    print(f"Successfully streamed {len(transactions)} {contract} transactions from {page - 1} pages to csv.")
