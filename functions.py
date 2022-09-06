import pandas as pd
import numpy as np
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

def pasiva():
    # Data
    enero_2020 = pd.read_csv('files/NAFTRAC_20200131.csv')
    enero_2020 = enero_2020.dropna()
    # W y $
    tick_w = enero_2020[["Ticker", "Peso (%)"]]
    tick_w["Dinero"] = tick_w["Peso (%)"] * 10000
    # Descarga precios
    data = {}
    for i in range(len(tick_w)):
        data[tick_w.iloc[i,0]] = yf.download(tickers = tick_w.iloc[i,0],  
                                             interval="1mo", start='2020-01-31',
                                             end='2022-07-29', progress=False).dropna()
    # Comisiones
    tick_w["Titulos"] = [round(tick_w["Dinero"][i] / (data[tick_w["Ticker"][i]]["Adj Close"][0] * 1.00125),0) 
                         for i in range(len(data))]
    # Back-test
    llave = list(data.keys())
    portafolio = []
    for i in range(len(data[llave[0]])):
        precios = []
        for j in llave:
            precios.append(data[j]["Adj Close"][i])
        portafolio.append(np.dot(tick_w['Titulos'], precios))
    # Capital, rendimiento
    df_pasiva = pd.DataFrame(index = data[llave[0]].index, columns=['capital', 'rend', 'rend_acum'])
    df_pasiva['capital'] = portafolio
    df_pasiva['rend'] = df_pasiva['capital'].pct_change()
    df_pasiva['rend_acum'] = ((df_pasiva['rend']+1).cumprod())-1
    return df_pasiva