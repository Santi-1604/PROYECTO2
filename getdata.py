import pandas as pd
def getdata(ruta):
    df = pd.read_csv(ruta,low_memory=False)
    df = df.iloc[::-1]
    return df
ruta = 'C:\\Users\\52331\\Downloads\\Binance_BTCUSDT_1h.csv'
df = getdata(ruta)
print(df)
