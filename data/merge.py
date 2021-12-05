import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

hashmasks_transfers = pd.read_csv("./transfers/hashmasks.csv")
hashmasks_all = pd.read_csv("./all/hashmasks.csv")

merged_data = hashmasks_transfers.merge(hashmasks_all, how='left', on='hash', suffixes=(None, "_all"))

for (column_name, column_data) in merged_data.iteritems():
    if "_all" in column_name:
        merged_data = merged_data.drop(columns=[column_name])

drop_columns = [
    "nonce",
    "blockHash",
    "tokenName",
    "tokenSymbol",
    "tokenDecimal",
    "transactionIndex",
    "gas",
    "gasPrice",
    "gasUsed",
    "cumulativeGasUsed",
    "input",
    "confirmations",
    "isError",
    "txreceipt_status"
]

for drop_column in drop_columns:
    merged_data = merged_data.drop(drop_column, axis=1)

merged_data.to_csv('./merged/hashmasks.csv')