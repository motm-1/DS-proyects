import pymysql
import pandas as pd
from sqlalchemy import create_engine


def upload_df(df):
    connection = create_engine('mysql+pymysql://root:'+str(input('Password: '))+'@localhost:3306/eth_data')
    df.to_sql(name='eth_data', con=connection, if_exists='append', index=False)


if __name__ == "__main__":
    ETH_Data = pd.read_csv(r'C:\Users\Tomas\Desktop\ETH_Proyect\ETH_Data.csv', index_col=0)
    upload_df(ETH_Data)
