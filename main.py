import pandas as pd
import requests

# make API call


def get_eth_addresses():
    eth_addresses = []
    url = 'https://eth.2miners.com/api/miners'

    response = requests.get(url).json()
    addresses = response['miners'].keys()
    addresses = list(addresses)

    for x in addresses:
        if x.find('0x') == 0:
            eth_addresses.append(x)
        else:
            pass

    return pd.Series(eth_addresses)


# second API call

def get_eth_per_month(eth_addresses, range_start, range_end):
    eth_2miners = 1000000000
    eth_per_month = []

    for address in eth_addresses[range_start:range_end]:
        url = 'https://eth.2miners.com/api/accounts/' + address
        response = requests.get(url)

        if response.status_code == 200:
            response = response.json()
            my_df = pd.DataFrame(response['sumrewards'])
            my_df = my_df['reward'] / eth_2miners
            eth_per_month.append(my_df.iloc[4])

        else:
            eth_per_month.append(0)

    return pd.Series(eth_per_month)


# Etherscan API call

def get_eth_current_balance(eth_addresses, API_KEY):
    eth_current_balance = pd.Series(dtype='int')
    eth_etherscan = 1000000000000000000
    x = 0
    y = 20
    z = len(eth_addresses.iloc[::20]) * 20 - 20

    if z >= 20:
        for x in range(0, z, 20):
            to_call = eth_addresses.iloc[x:y]
            x += 20
            y += 20
            url = 'https://api.etherscan.io/api?module=account&action=balancemulti&address=' + to_call.iloc[0] + ',' + \
                  to_call.iloc[1] + ',' + to_call.iloc[2] + ',' + to_call.iloc[3] + ',' + to_call.iloc[4] + ',' + \
                  to_call.iloc[5] + ',' + to_call.iloc[6] + ',' + to_call.iloc[7] + ',' + to_call.iloc[8] + ',' + \
                  to_call.iloc[9] + ',' + to_call.iloc[10] + ',' + to_call.iloc[11] + ',' + to_call.iloc[12] + ',' + \
                  to_call.iloc[13] + ',' + to_call.iloc[14] + ',' + to_call.iloc[15] + ',' + to_call.iloc[16] + ',' + \
                  to_call.iloc[17] + ',' + to_call.iloc[18] + ',' + to_call.iloc[19] + '&tag=latest&apikey=' + API_KEY

            response = requests.get(url).json()
            my_df = pd.DataFrame(response['result'])
            my_df.drop(columns='account', inplace=True)
            my_df = pd.Series(my_df['balance'])
            eth_current_balance = eth_current_balance.append(my_df)
    else:
        pass

    eth_rest_current_balance = []

    for x in range(z, len(eth_addresses)):
        url = 'https://api.etherscan.io/api?module=account&action=balance&address=' + eth_addresses.iloc[
            x] + '&tag=latest&apikey=' + API_KEY
        response = requests.get(url).json()
        eth_rest_current_balance.append(int(response['result']))

    eth_rest_current_balance = pd.Series(eth_rest_current_balance)
    eth_current_balance = pd.concat([eth_current_balance, eth_rest_current_balance], ignore_index=True)
    eth_current_balance = eth_current_balance.apply(lambda x: x/eth_etherscan)
    return eth_current_balance


def create_df(eth_addresses, eth_per_month, eth_balances):
    my_df = pd.DataFrame(columns=['ETH_address', 'ETH_mined_last_month', 'ETH_current_balance'])
    my_df['ETH_address'] = eth_addresses
    my_df['ETH_mined_las_month'] = eth_per_month
    my_df['ETH_current_balance'] = eth_balances

    my_df.to_csv('ETH_Data.csv')


if __name__ == "__main__":
    eth_addresses = get_eth_addresses()
    eth_per_month = get_eth_per_month(eth_addresses, range_start=int(input('Start: ')), range_end=int(input('End: ')))
    eth_addresses = eth_addresses.iloc[:len(eth_per_month)]
    eth_balances = get_eth_current_balance(eth_addresses, str(input('Enter your Etherscan API Key')))
    create_df(eth_addresses, eth_per_month, eth_balances)
