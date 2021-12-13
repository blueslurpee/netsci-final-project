import pandas as pd
import os
import numpy as np

# get all the account balances for a specific csv file.
def cleanBalances(infile, outfile):

    # read the input file.
    input_df = pd.read_csv(infile)
    
    # remove duplicate rows. We only need one entry per address and block
    input_df.drop_duplicates(subset=['block', 'address'], inplace=True)
    
    # drop the old index that is not continous
    input_df.drop('row' , axis='columns', inplace=True)
    input_df.reset_index(drop=True, inplace=True)

    # store the dataframe
    input_df.index.name = 'row'
    input_df.to_csv(outfile, index=True)

inFile = "./balances/coolcats_raw.csv"
outFile = "./balances/coolcats.csv"
cleanBalances(inFile, outFile)