import pandas as pd
def getdata(ruta):
    df = pd.read_csv(ruta,low_memory=False)
    return df
ruta = 'C:\\Users\\52331\\Downloads\\Binance_BTCUSDT_1h.csv'
