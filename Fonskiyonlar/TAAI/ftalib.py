import pandas as pd
import pandas_ta as ta
def TA(df):
    vortex_deger = pd.DataFrame()
    df['RSI'] = ta.rsi(df["close"], kind="sma",length=14)
    df['CMF'] = ta.cmf(df['high'],df['low'],df["close"], df["volume"], length=20)
    df['MFI'] = ta.mfi(df['high'],df['low'],df['close'],df['volume'], length=14)
    df["EMA"] = ta.ema(df["close"], length=20)
    # vortex_deger = ta.vortex(df["high"],df["low"],df["close"])
    # vtxdeger = vortex_deger['VTXP_14'] - vortex_deger['VTXM_14'] 
    # df['VTX'] = vtxdeger
    return df