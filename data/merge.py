import os
import pandas as pd

from decimal import Decimal
from tqdm import tqdm

from web3 import Web3
from dotenv import load_dotenv
from contracts import CONTRACTS

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.environ['ALCHEMY_RPC_URL']))

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

contract = os.environ['MERGE_CONTRACT_SELECTION']

transfers = pd.read_csv(f"./transfers/{contract}.csv")
transfers['value'] = ""

transaction_values = {}
print(f"Fetching values for {contract}")

for i, row in tqdm(transfers.iterrows(), total=transfers.shape[0]):
    transaction_hash = row['hash']

    # Memoization to spare API calls
    if transaction_hash in transaction_values:
        value = transaction_values[transaction_hash]
    else:
        value = str(Decimal(w3.eth.get_transaction(row['hash'])['value']) / (Decimal(10) ** 18))
        transaction_values[transaction_hash] = value

    transfers.at[i, 'value'] = value

transfers.to_csv(f'./merged/{contract}.csv')