


from getdata import getdata
from gridsearch import grid_search_backtest
import matplotlib.pyplot as plt
from regime_markets_conditions import run_adaptive_grid_windows
def main():
    ruta = 'Binance_BTCUSDT_1h.csv'
    print('Alistando data frame')
    df = getdata(ruta)
    print(df.tail())
    param_grid = {'bs': [0.6, 0.8],
                  'bc': [2, 5],
                  'bw': [0.55, 0.65],
                  'sl_pct': [0.02, 0.03],
                  'tp_pct': [0.03, 0.05]
                }
    best_params, best_result , best_df= grid_search_backtest(df,param_grid)
    print(best_params)
    print(best_result['metricas'])
    d = best_result['diario']
    m = best_result['mensual']
    t = best_result['trimestral']
    a = best_result['anual']
    print(best_result['mensual'])

    plt.plot(m['Date'],m['Rendimiento'])
    plt.title("Mensual")
    plt.show()
    print(best_result['trimestral'])
    plt.plot(t['Date'],t['Rendimiento'])
    plt.title("Trimestral")
    plt.show()
    print(best_result['anual'])
    plt.plot(a['Date'],a['Rendimiento'])
    plt.title("Anual")
    plt.show()
    print('\nEjecutando grid search adaptativo...')

    best_result = run_adaptive_grid_windows(
        best_df,
        windows=[10, 20],
        cash=1000000,
        com=0.00125,
        sl=best_params['sl_pct'],
        tp=best_params['tp_pct'],
    )
    d = best_result['diario']
    m = best_result['mensual']
    t = best_result['trimestral']
    a = best_result['anual']
    print(best_result['mensual'])

    plt.plot(m['Date'], m['Rendimiento'])
    plt.title("Mensual")
    plt.show()
    print(best_result['trimestral'])
    plt.plot(t['Date'], t['Rendimiento'])
    plt.title("Trimestral")
    plt.show()
    print(best_result['anual'])
    plt.plot(a['Date'], a['Rendimiento'])
    plt.title("Anual")
    plt.show()
    print('\nEjecutando grid search adaptativo...')


if __name__ == '__main__':
    main()
