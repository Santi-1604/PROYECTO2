
import itertools

import numpy as np

from sortino import sortino
from calmar import calmar

from winrate import winrate
from Buy_sell import Buy_sell

from backtesting import  backtest

def grid_search_backtest(df, param_grid):
    def generar_senales(df, params):
        df_temp = df.copy()
        df_temp = sortino(df_temp,0.002, 20,params['bs'])
        df_temp = calmar(df_temp, 20,params['bc'])
        df_temp = winrate(df_temp, 20,params['bw'])

        df_temp = Buy_sell(df_temp)
        return df_temp

    print("🔍 Iniciando Grid Search de parámetros...")
    best_params = None
    best_result = None
    best_perf = -np.inf

    # Iterar sobre todas las combinaciones de parámetros
    for combo in itertools.product(*param_grid.values()):
        params = dict(zip(param_grid.keys(), combo))

        # Generar señales según los parámetros actuales
        df_signals = generar_senales(df, params)

        # Ejecutar el backtest
        resultados = backtest(df_signals,1000000,0.0125 ,params['sl_pct'], params['tp_pct'])

        # Tomar el rendimiento final del portafolio diario
        final_perf = resultados['metricas']['sharpe_ratio']


        # Guardar si es mejor
        if final_perf > best_perf:
            best_perf = final_perf
            best_params = params
            best_result = resultados
            best_df = generar_senales(df, best_params)

        print(f"Probar {params} → Rendimiento final: {final_perf:.4f}")

    print("\n✅ Mejores parámetros encontrados:")
    print(best_params)
    print(f"Rendimiento final: {best_perf:.4f}")

    return best_params, best_result, best_df
