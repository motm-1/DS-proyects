import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests


def main():
    eth_addresses = pd.read_csv(r'C:\Users\Tomas\Downloads\ETH_PER_MONTH\eth_addresses.csv')
    eth = 1000000000
    eth_per_month = []

    for address in eth_addresses[:1]:
        url = 'https://eth.2miners.com/api/accounts/' + address

        response_2 = requests.get(url).json()

        my_df = pd.DataFrame(response_2['sumrewards'])
        my_df = my_df['reward'] / eth
        eth_per_month.append(my_df.iloc[4])

    return eth_per_month


if __name__ == "__main__":
    eth_per_month = main()
    print(eth_per_month)

