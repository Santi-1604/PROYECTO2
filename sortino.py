import numpy as np
import pandas as pd
def sortino(df, rf=0, window=10):
    import numpy as np

    if 'Close' in df.columns:
        if 'ren' not in df.columns:
            df['ren'] = np.log(df['Close'] / df['Close'].shift(1))

    df = df.dropna()  # eliminar NaN

    # Función para aplicar a cada ventana
    def sortino_window(x):
        # Retornos negativos
        neg_rets = x[x < 0]
        sigma_d = neg_rets.std()
        if sigma_d == 0:
            sigma_d = 1  # evitar división entre 0
        return (x.mean() - rf) / sigma_d

    # Aplicar rolling window
    df['sortino'] = df['ren'].rolling(window=window).apply(sortino_window, raw=False)
    df = df.dropna()
    df['sortino_buy'] = df['sortino']>0.8
    df['sortino_sell'] = df['sortino']<0
    return df
