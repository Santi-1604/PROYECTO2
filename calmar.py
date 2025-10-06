import numpy as np

def calmar(df, window):

    if 'Close' in df.columns:
        if 'ren' not in df.columns:
            df['ren'] = np.log(df['Close'] / df['Close'].shift(1))
    df = df.dropna()  # eliminar NaN

    def max_drawdown(prices):
        roll_max = prices.cummax()
        drawdown = (prices - roll_max) / roll_max
        return drawdown.min()  # negativo

    def annualized_return(returns, window):
        mean_daily = returns[-window:].mean()
        return mean_daily * 252  # aproximación

    cr_values = []

    for i in range(len(df)):
        if i < window - 1:
            cr_values.append(np.nan)
            continue

            # Ventana de precios
        window_prices = df['Close'].iloc[i - window + 1:i + 1]
        window_rets = df['ren'].iloc[i - window + 1:i + 1]

            # Calmar
        ann_ret = annualized_return(window_rets, window)
        mdd = abs(max_drawdown(window_prices))

        if mdd == 0:
            cr_values.append(np.nan)
        else:
            cr_values.append(ann_ret / mdd)

    df['calmar'] = cr_values
    df = df.dropna()
    df['calmar_buy'] = df['calmar']>5
    df['calmar_sell'] = df['calmar']<0
    return df
