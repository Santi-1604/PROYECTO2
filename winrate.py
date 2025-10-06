import numpy as np

def winrate(df,window):
    if 'Close' in df.columns:
        if 'ren' not in df.columns:
            df['ren'] = np.log(df['Close'] / df['Close'].shift(1))
    df = df.dropna()  # eliminar NaN
    def winrate_window(ren):
        pos_ret = (ren>0).astype(int)
        return pos_ret.mean()
    df['winrate_ren'] = df['ren'].rolling(window=window).apply(winrate_window)
    df = df.dropna()
    df['winrate_buy'] = df['winrate_ren']>0.60
    df['winrate_sell'] = df['winrate_ren']<-0.4
    return df
