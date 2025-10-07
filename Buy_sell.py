def Buy_sell(df):
    buy = []

    if 'winrate_buy' in df.columns and 'sortino_buy' in df.columns and 'calmar_buy' in df.columns:
     for i in range(len(df)):
        b = 0

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
    df['buy_signal'] = buy

    return df