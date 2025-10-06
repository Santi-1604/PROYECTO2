from sortino import sortino
from calmar import calmar
from getdata import getdata
from winrate import winrate
from Buy_sell import Buy_sell


def main():
    ruta = 'C:\\Users\\52331\\Downloads\\Binance_BTCUSDT_1h.csv'
    df = getdata(ruta)
    df = sortino(df,0.002,10)
    df = calmar(df,10)
    df = winrate(df,10)
    df = Buy_sell(df)
    print(df.tail())
if __name__ == '__main__':
    main()