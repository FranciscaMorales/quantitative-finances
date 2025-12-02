import pandas as pd
import numpy as np
import scipy.stats as stats
from.backend import market_prices

def portafolio_volatility(
    df:pd.DataFrame,
    vector_w:np.array
    ) -> float:

    '''
        "documentacion de string"
        Calculo de la volatilidad de un portafolio de inversiones

        df
            DataFrame del retorno del portafolio
            "precio modificado "
        vector_w 
            Vector de pesos de los instrumentos del portafoio
        
        Return: decimal (float) de la volatilidad

    '''
    #matriz de var-cov
    mcov = df.cov()

    #vector traspuesto
    vector_w_t = np.array([vector_w])

    #varianza
    vector_cov = np.dot(mcov, vector_w)
    varianza = np.dot(vector_w_t, vector_cov)

    #volatilidad
    vol = np.sqrt(varianza)

    return vol [0]

def portfolio_returns (
    tickers: list,
    start: str,
    end:str,
    ) -> pd.DataFrame:

    ''' doc string
    Descarga desde la bbdd los precios de los instrumentos
    indicados en el rango de fechas.

    tickers (list)
        Es una lista de nemos de instrumentos que componen un portafolio
    
    start (str)
        Es la fecha de inicio de precios
    
    end (str)
        Es la fecha de termino de precios

    Retorno (pd.DataFrame)
        dataframe de retornos diarios
    '''
    #descargar precios
    df = market_prices(
        start_date=start,
        end_date=end,
        tickers=tickers)
    
    #pivot retornos
    df_pivot = pd.pivot_table(
        data=df,
        index='FECHA', 
        columns='TICKER',
        values='PRECIO_CIERRE',
            aggfunc='max'
      )
    
    #retornos
    df_pivot = df_pivot.pct_change().dropna()

    return df_pivot

def VaR(sigma:float, confidence:float) -> float:
    '''
    Calculo del Value at Risk al nivel de confianza indicado
    Con supuesto de media cero.
    '''
    #estadistico Z al nivel de confianza
    z_score = stats.norm.ppf(confidence)
    
    #VaR
    var= z_score * sigma

    return var
