import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

contract = os.environ['COLLATE_CONTRACT_SELECTION']

merged_data = pd.read_csv(f"./merged/{contract}.csv")

merged_data.drop(labels=['nonce',
                         'blockHash',
                         'tokenName',
                         'tokenSymbol',
                         'tokenDecimal',
                         'transactionIndex',
                         'gas',
                         'gasPrice',
                         'gasUsed',
                         'cumulativeGasUsed',
                         'input',
                         'confirmations'],
                 axis=1,
                 inplace=True)

merged_data.rename(
    columns={
        'Unnamed: 0': 'row',
        'blockNumber': 'blk_number',
        'timeStamp': 'blk_timestamp',
        'hash': 'tx_hash',
        'value': 'eth_value',
        'contractAddress': 'token_address',
        'from': 'from_address',
        'to': 'to_address',
        'tokenID': 'token_id',
    },
    inplace=True)

merged_data = merged_data[[
    'row',
    'tx_hash',
    'token_address',
    'from_address',
    'to_address',
    'token_id',
    'blk_number',
    'blk_timestamp',
    'eth_value']]

merged_data.to_csv(f'./collated/{contract}.csv', index=False)