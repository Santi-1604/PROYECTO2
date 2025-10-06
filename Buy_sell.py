def Buy_sell(df):
    buy = []
    sell = []
    if 'winrate_buy' in df.columns and 'sortino_buy' in df.columns and 'calmar_buy' in df.columns:
     for i in range(len(df)):
        b = 0
        s = 0
        if df['winrate_buy'].iloc[i] == True:
            b +=1
        if df['sortino_buy'].iloc[i] == True:
            b+=1
        if df['calmar_buy'].iloc[i] == True:
            b+=1
        if b >= 2:
            buy.append('True')
        else:
            buy.append('False')
        if df['winrate_sell'].iloc[i] == True:
            s +=1
        if df['sortino_sell'].iloc[i] == True:
            s +=1
        if df['calmar_sell'].iloc[i] == True:
            s +=1
        if s >= 2:
            sell.append('True')
        else:
            sell.append('False')
    df['buy_signal'] = buy
    df['sell_signal'] = sell
    return df