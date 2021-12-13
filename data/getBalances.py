import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import numpy as np
from datetime import datetime
from tqdm import tqdm
from coinbase.wallet.client import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.environ['COINBASE_KEY'], os.environ['COINBASE_SECRET'])

# pip install web3
# https://gist.github.com/mtford90/49b04506b0df6bf0720fb2ba2aaaff46# 
from web3 import Web3
w3 = Web3(Web3.WebsocketProvider(os.environ['ETH_NODE_WSS']))

# get all the account balances for a specific csv file.
def getBalances(infile, outfile):

    # if (os.path.isfile(outfile)):
    #     print("output file does already exist. skipping.")
    #     return

    # read the input file.
    data = []
    input_df = pd.read_csv(infile)

    subset = input_df.iloc[15950:30000]
    for row in tqdm(subset.itertuples()):

        # read the values from the dataframe.
        cur_row = row[1]
        from_address = row[4].strip()
        to_address = row[5].strip()
        timestamp = row[8]
        block = row[7]

        # we also store the data in the csv file.
        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        eth_usd_price = client.get_spot_price(currency_pair = 'ETH-USD', date=date)['amount']

        # lookup value of both nodes at the time of this block
        if (not from_address == '0x0000000000000000000000000000000000000000'):
            address = w3.toChecksumAddress(from_address)
            value_from = w3.eth.get_balance(address, block_identifier=block)
            eth_value_from = w3.fromWei(value_from, 'ether')
            usd_value = float(eth_value_from) * float(eth_usd_price)
            data.append([block, date, from_address, eth_value_from, usd_value])
        if (not to_address == '0x0000000000000000000000000000000000000000'):
            address = w3.toChecksumAddress(to_address)
            value_to = w3.eth.get_balance(address, block_identifier=block)
            eth_value_to = w3.fromWei(value_to, 'ether')
            usd_value = float(eth_value_to) * float(eth_usd_price)
            data.append([block, date, to_address, eth_value_to, usd_value])
    
        # write dataframe to disk every 1000 rows
        if (cur_row % 1000 == 0):
            df = pd.DataFrame(data, columns=['block', 'date', 'address', 'eth_value', 'usd_value'])
            df.index.name = 'row'
            df.to_csv(outfile, mode='a', index=True, header=False)
            data = []
            # df.to_csv(outfile, index=True)

inFile = "./collated/cryptoadz.csv"
outFile = "./balances/cryptoadz_raw.csv"
getBalances(inFile, outFile)