import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
from backtesting import backtest


def compute_regime_features_single(prices, window=21):
    """Cálculo de momentum, autocorrelación, volatilidad y reversals en ventana móvil."""
    if isinstance(prices, pd.Series):
        series = prices.copy()
    else:
        series = prices.iloc[:, 0].copy()

    rets = np.log(series / series.shift(1)).dropna()
    features = []
    idxs = []
    for end in range(window, len(rets) + 1):
        r = rets.iloc[end - window:end]
        momentum = r.mean()
        vol = r.std()
        autocorr = r.autocorr(lag=1)
        sign_changes = np.sum(np.sign(r.values[1:]) != np.sign(r.values[:-1])) / (len(r) - 1)
        features.append([momentum, autocorr, vol, sign_changes])
        idxs.append(r.index[-1])

    df_feat = pd.DataFrame(features, index=idxs, columns=['momentum', 'autocorr', 'vol', 'reversals'])
    return df_feat


def cluster_and_label_single(features_df, n_clusters=3, random_state=0):
    """Agrupa y etiqueta regímenes de mercado según similitud con prototipos."""
    scaler = StandardScaler()
    X = scaler.fit_transform(features_df[['momentum', 'autocorr', 'vol', 'reversals']])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=20)
        clusters = kmeans.fit_predict(X)

    features_df = features_df.copy()
    features_df['cluster'] = clusters

    # Prototipos heurísticos (solo para 1 activo)
    prototypes = {
        'HighMomentum': np.array([+1.5, +0.5, 0.0, -1.0]),
        'MeanReverting': np.array([-0.5, -1.0, -0.3, +1.2]),
        'Crisis': np.array([-1.0, +0.7, +1.5, +0.5])
    }

    def cosine(a, b):
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return (a @ b) / denom if denom != 0 else -1

    centroid_labels = []
    for c in kmeans.cluster_centers_:
        sims = {k: cosine(c, prototypes[k]) for k in prototypes}
        label = max(sims.items(), key=lambda x: x[1])[0]
        centroid_labels.append(label)

    mapping = {i: centroid_labels[i] for i in range(len(centroid_labels))}
    features_df['regime'] = features_df['cluster'].map(mapping)
    return features_df, kmeans, scaler


def run_adaptive_grid_windows(df_prices, windows=[10, 20],
                              cash=10000, com=0.001, sl=0.02, tp=0.04):

    if 'Close' not in df_prices.columns:
        raise ValueError("Tu dataframe debe contener la columna 'Close'")

    results = []
    price_series = df_prices['Close']

    for w in windows:
        print(f"\n>>> Procesando window = {w}")
        feats = compute_regime_features_single(price_series, window=w)
        if feats.empty:
            print(f"  - no hay suficientes datos para window {w}, se salta.")
            continue

        feats_labeled, kmeans, scaler = cluster_and_label_single(feats, n_clusters=3, random_state=42)
        sma = price_series.rolling(window=w).mean()

        df = df_prices.copy()

        df['regime'] = np.nan
        df['sma'] = sma
        # asignar régimen en base al índice
        df.loc[feats_labeled.index, 'regime'] = feats_labeled['regime']

        # buy_signal según régimen

        for i in range(len(df)):
            if df['regime'].iloc[i] == 'HighMomentum':
                if df['Close'].iloc[i] < df['sma'].iloc[i]:
                    df['buy_signal'] = True
                else:
                    df['buy_signal'] = False
            if df['regime'].iloc[i] == 'MeanReverting':
                if df['Close'].iloc[i] > df['sma'].iloc[i]:
                    df['sell_signal'] = True
                else:
                    df['sell_signal'] = False



        bt_result = backtest(df, cash=cash, com=com, sl=sl, tp=tp)
        metrics = bt_result['metricas']
        metrics.update({'window': w})


        print(f"  - window={w} -> Sharpe={metrics['sharpe_ratio']:.4f}, Ret={metrics['annualized_return']:.4f}")

    print("\n=== Resumen final (por window x regime) ===")
    print(bt_result['diario'])

    return bt_result

