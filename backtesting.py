
import pandas as pd
import numpy as np
from dataclasses import dataclass
import warnings
def backtest(df, cash, com, sl, tp):
    @dataclass
    class Operation:
        t: str
        p: float
        sl: float
        tp: float
        n_shares: float
        type: str

    active_positions: list[Operation] = []
    records = []  # Para guardar el capital, portafolio y rendimiento

    initial_cash = cash

    for i, row in df.iterrows():
        # 1️⃣ Cerrar posiciones si se llega a SL o TP
        for position in active_positions.copy():
            if row.Close >= position.tp or row.Close <= position.sl: #or row.sell_signal:
                # Venta (cerrar posición)
                cash += row.Close * position.n_shares * (1 - com)
                active_positions.remove(position)

        # 2️⃣ Abrir posición si hay señal de compra
        if row.buy_signal and cash > row.Close * (1 + com):
            n_shares = cash // (row.Close * (1 + com))  # cuántas se pueden comprar
            cost = n_shares * row.Close * (1 + com)
            cash -= cost
            active_positions.append(Operation(
                t=row.Date,
                p=row.Close,
                tp=row.Close * (1 + tp),
                sl=row.Close * (1 - sl),
                n_shares=n_shares,
                type="Long"
            ))

        # 3️⃣ Calcular valor total del portafolio
        invested_value = sum([pos.n_shares * row.Close for pos in active_positions])
        total_portfolio = cash + invested_value
        rendimiento = (total_portfolio - initial_cash) / initial_cash

        # 4️⃣ Guardar los valores en una lista
        records.append({
            'Date': row.Date,
            'Capital': cash,
            'Portafolio': total_portfolio,
            'Rendimiento': rendimiento
        })

    # 5️⃣ Convertir resultados a DataFrame
    result_df = pd.DataFrame(records)
    result_df['Date'] = pd.to_datetime(result_df['Date'], format='%m/%d/%Y %H:%M', errors='coerce')

    # Eliminar filas sin fecha válida (por si acaso)

    result_df = result_df.dropna(subset=['Date'])

    # Establecer índice de tiempo
    result_df = result_df.set_index('Date')
    # 7️⃣ Métricas de performance
    trading_days = 365
    total_return = (result_df['Portafolio'].iloc[-1] / result_df['Portafolio'].iloc[0]) - 1
    annual_return = (1 + total_return) ** (trading_days / len(result_df)) - 1
    annual_volatility = result_df['Rendimiento'].std() * np.sqrt(trading_days)
    sharpe_ratio = (annual_return - 0.04) / annual_volatility if annual_volatility != 0 else np.nan  # RF = 4%
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        monthly = result_df.resample('M').mean().reset_index()  # valor promedio de cada mes
        quarterly = result_df.resample('Q').mean().reset_index()  # valor promedio cada 3 meses
        yearly = result_df.resample('Y').mean().reset_index()  # último valor del año
        result_df = result_df.reset_index()
    metrics = {
        'total_return': total_return,
        'annualized_return': annual_return,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio
    }
    return {
        'diario': result_df,
        'mensual': monthly,
        'trimestral': quarterly,
        'anual': yearly,
        'metricas' : metrics
    }
