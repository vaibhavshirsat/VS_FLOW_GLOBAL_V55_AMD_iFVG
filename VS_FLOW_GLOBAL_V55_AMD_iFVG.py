import re
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st

try:
    import yfinance as yf
except Exception:
    yf = None

APP = "VS FLOW GLOBAL"
VERSION = "V55"
BASE = Path(__file__).resolve().parent
LOGO = BASE / "vs_flow_logo.png"

st.set_page_config(
    page_title="VS FLOW GLOBAL V55",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# THEME — same V55 architecture
# =========================
st.markdown("""
<style>
:root{
 --bg:#030914; --bg2:#061321; --panel:#081a2b; --panel2:#0b2136;
 --line:#164461; --cyan:#11dfff; --blue:#4d8dff; --violet:#9b5cff;
 --pink:#ff3ba7; --green:#00e676; --red:#ff4058; --gold:#ffc857;
 --text:#f5f8ff; --muted:#91a8bb;
}
html,body,[class*="css"]{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}
.stApp{background:radial-gradient(circle at 80% -10%,rgba(18,90,140,.32),transparent 35%),radial-gradient(circle at 10% 0%,rgba(67,20,130,.22),transparent 28%),linear-gradient(180deg,#030914,#020711 70%,#02060d);color:var(--text)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#04101d 0%,#020812 100%);border-right:1px solid #12354b}
[data-testid="stSidebar"] > div{padding-top:.7rem}
.block-container{max-width:1750px;padding:.75rem 1rem 2rem}
.stButton button{background:linear-gradient(180deg,#0b2439,#07182a)!important;border:1px solid #1b5273!important;color:#eef8ff!important;border-radius:10px!important;font-weight:800!important}
.stButton button:hover{border-color:var(--cyan)!important;box-shadow:0 0 16px rgba(17,223,255,.15)}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div,.stTextArea textarea,.stNumberInput input{background:#04101c!important;color:#f3f8ff!important;border:1px solid #1a4662!important;border-radius:9px!important}
[data-testid="stDataFrame"]{border:1px solid #153e59;border-radius:12px;overflow:hidden}
.vs-brand{font-size:24px;font-weight:950;letter-spacing:.3px}.vs-brand .global{color:var(--cyan)}
.vs-sub{font-size:10px;color:var(--cyan);letter-spacing:2px;font-weight:800}.logo-wrap{padding:4px 2px 10px}
.logo-wrap img{border-radius:16px;border:1px solid #204c69;box-shadow:0 0 24px rgba(0,218,255,.10)}
.hero{background:linear-gradient(120deg,#071a2d 0%,#06182a 48%,#081d31 100%);border:1px solid #1c4d6a;border-radius:20px;padding:22px 25px 16px;box-shadow:0 16px 50px rgba(0,0,0,.28);margin-bottom:14px}
.hero h1{margin:0;font-size:39px;font-weight:950;line-height:1}.hero p{margin:9px 0 0;color:#8fb9d4;font-size:13px}
.gradient{height:4px;border-radius:9px;margin-top:17px;background:linear-gradient(90deg,#00e5ff,#4d8dff,#9b5cff,#ff3ba7,#ff7a18,#ffd22e)}
.section{font-size:21px;font-weight:950;margin:18px 0 10px}.section small{font-size:11px;color:var(--muted);font-weight:600;margin-left:7px}
.card{background:linear-gradient(145deg,#0a2034,#061522);border:1px solid #17425e;border-radius:14px;padding:14px;min-height:104px;box-shadow:inset 0 1px rgba(255,255,255,.025)}
.card .label{font-size:11px;color:#9bb3c7;font-weight:800}.card .value{font-size:24px;font-weight:950;margin:6px 0}.up{color:var(--green)}.down{color:var(--red)}.flat{color:#b7c7d4}
.panel{background:rgba(7,22,36,.94);border:1px solid #17415d;border-radius:15px;padding:14px;box-shadow:0 8px 28px rgba(0,0,0,.13)}
.pill{display:inline-block;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:900;border:1px solid #285675;background:#082237;color:#a8ddf2;margin-right:4px}.pill.green{border-color:#0a704c;background:#062b20;color:#54ffad}.pill.red{border-color:#6f2030;background:#2b0a13;color:#ff8a99}.pill.gold{border-color:#775b16;background:#2b2206;color:#ffd86c}
.metric{border:1px solid #17415d;border-radius:12px;background:#071a2c;padding:12px}.metric .k{font-size:10px;color:#8ea7ba;font-weight:800}.metric .v{font-size:22px;font-weight:950;margin-top:4px}
.scorebar{height:9px;border-radius:20px;background:#0b2032;overflow:hidden;border:1px solid #173c55}.scorebar > div{height:100%;background:linear-gradient(90deg,#ff4058,#ffc857,#00e676)}
.note{border-left:3px solid var(--cyan);background:#061b2d;padding:10px 12px;border-radius:8px;color:#a9c4d7;font-size:12px}.side-note{font-size:10px;line-height:1.5;color:#6f879a;border-top:1px solid #12354b;margin-top:15px;padding-top:13px}hr{border-color:#14374f!important}
.setup-card{background:linear-gradient(145deg,#091e31,#061321);border:1px solid #174c69;border-radius:14px;padding:14px 16px;margin:8px 0;box-shadow:0 8px 26px rgba(0,0,0,.18)}
.setup-top{display:flex;gap:7px;align-items:center;font-size:18px;margin-bottom:10px}.setup-top b{margin-right:auto}.setup-grid{display:grid;grid-template-columns:repeat(6,minmax(90px,1fr));gap:8px}.setup-grid div{border:1px solid #153d56;border-radius:9px;padding:8px;background:#061827}.setup-grid span,.trade-line span{display:block;color:#7691a5;font-size:9px;font-weight:800}.setup-grid b{font-size:11px}.trade-line{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid #14374f}.trade-line b{color:#f5f8ff;font-size:12px;margin-left:4px}
.regime{font-size:30px;font-weight:950;letter-spacing:.5px}.heat{border:1px solid #17415d;border-radius:11px;padding:10px;background:#071a2c;margin:4px 0}.heat .v{font-weight:900;font-size:16px}.heat .s{font-size:10px;color:#8199ac}
.action-card{background:linear-gradient(145deg,#091e31,#061321);border:1px solid #174c69;border-radius:14px;padding:14px 16px;min-height:90px}
@media(max-width:900px){.setup-grid{grid-template-columns:repeat(2,1fr)}.trade-line{grid-template-columns:repeat(2,1fr)}}
.owner-badge{position:absolute;right:18px;top:16px;background:linear-gradient(135deg,#071b2c,#0b2740);border:1px solid #1d6b8d;border-radius:999px;padding:8px 14px;color:#fff;font-size:14px;font-weight:950;letter-spacing:.3px;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.click-hint{font-size:10px;color:#6f879a;margin-top:4px}.crypto-card{border-color:#2b5b75;background:linear-gradient(145deg,#0b2136,#071827)}
</style>
""", unsafe_allow_html=True)

# =========================
# GLOBAL UNIVERSE
# =========================
GLOBAL_INDEXES = {
    "^GSPC": "S&P 500", "^NDX": "Nasdaq 100", "^DJI": "Dow Jones", "^RUT": "Russell 2000", "^VIX": "CBOE VIX",
    "^FTSE": "FTSE 100", "^GDAXI": "DAX", "^FCHI": "CAC 40", "^STOXX50E": "Euro Stoxx 50",
    "^N225": "Nikkei 225", "^HSI": "Hang Seng", "000001.SS": "Shanghai Composite", "^KS11": "KOSPI", "^STI": "Straits Times",
    "^AXJO": "ASX 200",
}

CRYPTO = {
    "BTC-USD":"Bitcoin", "ETH-USD":"Ethereum", "BNB-USD":"BNB", "SOL-USD":"Solana", "XRP-USD":"XRP",
    "ADA-USD":"Cardano", "DOGE-USD":"Dogecoin", "AVAX-USD":"Avalanche", "LINK-USD":"Chainlink",
    "TRX-USD":"TRON", "TON-USD":"Toncoin", "SUI-USD":"Sui", "DOT-USD":"Polkadot", "LTC-USD":"Litecoin",
    "BCH-USD":"Bitcoin Cash", "UNI-USD":"Uniswap", "NEAR-USD":"NEAR Protocol", "ATOM-USD":"Cosmos",
}

COMMODITIES = {
    "GC=F":"Gold Futures", "SI=F":"Silver Futures", "CL=F":"WTI Crude Oil", "BZ=F":"Brent Crude Oil",
    "NG=F":"Natural Gas", "HG=F":"Copper", "PL=F":"Platinum", "PA=F":"Palladium",
}

FX = {
    "EURUSD=X":"EUR/USD", "GBPUSD=X":"GBP/USD", "USDJPY=X":"USD/JPY", "AUDUSD=X":"AUD/USD",
    "USDCAD=X":"USD/CAD", "USDCHF=X":"USD/CHF", "NZDUSD=X":"NZD/USD", "DX-Y.NYB":"US Dollar Index",
}

RATES = {"^TNX":"US 10Y Yield", "^TYX":"US 30Y Yield", "^FVX":"US 5Y Yield", "^IRX":"US 13W T-Bill"}

GLOBAL_STOCKS = {
    "AAPL":"Apple", "MSFT":"Microsoft", "NVDA":"NVIDIA", "AMZN":"Amazon", "GOOGL":"Alphabet", "META":"Meta Platforms",
    "TSLA":"Tesla", "AVGO":"Broadcom", "AMD":"Advanced Micro Devices", "ORCL":"Oracle", "NFLX":"Netflix", "CRM":"Salesforce",
    "JPM":"JPMorgan Chase", "V":"Visa", "MA":"Mastercard", "WMT":"Walmart", "COST":"Costco", "KO":"Coca-Cola",
    "PEP":"PepsiCo", "LLY":"Eli Lilly", "JNJ":"Johnson & Johnson", "XOM":"Exxon Mobil", "CVX":"Chevron",
    "TSM":"Taiwan Semiconductor", "ASML":"ASML Holding", "NVO":"Novo Nordisk", "SAP":"SAP", "TM":"Toyota Motor",
    "SONY":"Sony Group", "BABA":"Alibaba", "MELI":"MercadoLibre", "PDD":"PDD Holdings", "RIO":"Rio Tinto",
}

ASSET_META = {}
def _add_meta(group, mapping, region):
    for ticker, name in mapping.items():
        ASSET_META[ticker] = {"symbol":ticker,"name":name,"group":group,"region":region}

_add_meta("GLOBAL INDICES", GLOBAL_INDEXES, "Global")
_add_meta("CRYPTO", CRYPTO, "24/7 Global")
_add_meta("COMMODITIES", COMMODITIES, "Global")
_add_meta("FX", FX, "Global FX")
_add_meta("RATES", RATES, "US Rates")
_add_meta("GLOBAL STOCKS", GLOBAL_STOCKS, "Global Equities")

ALL_TICKERS = list(ASSET_META)

# =========================
# MARKET DATA
# =========================
def yf_ticker(symbol, exchange="GLOBAL"):
    return str(symbol).strip().upper()

@st.cache_data(ttl=180, show_spinner=False)
def history(ticker, period="6mo", interval="1d"):
    if yf is None: return pd.DataFrame()
    try:
        d=yf.download(ticker,period=period,interval=interval,auto_adjust=False,progress=False,threads=False)
        if d is None or d.empty: return pd.DataFrame()
        if isinstance(d.columns,pd.MultiIndex): d.columns=d.columns.get_level_values(0)
        return d.dropna(how="all")
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=120, show_spinner=False)
def quote(ticker):
    d=history(ticker,"5d","1d")
    if d.empty or "Close" not in d: return None
    c=d["Close"].dropna()
    if len(c)==0: return None
    price=float(c.iloc[-1]); prev=float(c.iloc[-2]) if len(c)>1 else price
    return {"price":price,"chg":(price/prev-1)*100 if prev else 0}

def rsi(series,n=14):
    delta=series.diff(); gain=delta.clip(lower=0).ewm(alpha=1/n,adjust=False).mean(); loss=-delta.clip(upper=0).ewm(alpha=1/n,adjust=False).mean()
    rs=gain/loss.replace(0,np.nan); return 100-(100/(1+rs))

def atr(df,n=14):
    h,l,c=df["High"],df["Low"],df["Close"]
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def technical_snapshot(ticker):
    d=history(ticker,"1y","1d")
    if d.empty or len(d)<60:return None
    c=d["Close"].astype(float); v=d["Volume"].fillna(0).astype(float)
    e20=c.ewm(span=20,adjust=False).mean(); e50=c.ewm(span=50,adjust=False).mean(); e200=c.ewm(span=200,adjust=False).mean()
    rr=rsi(c).iloc[-1]; at=atr(d).iloc[-1]; price=float(c.iloc[-1]); high52=float(d["High"].tail(252).max()); low52=float(d["Low"].tail(252).min())
    vol=float(v.iloc[-1]); v20=float(v.tail(20).mean()) if v.tail(20).mean() else vol
    trend="BULLISH" if e20.iloc[-1]>e50.iloc[-1] else ("BEARISH" if e20.iloc[-1]<e50.iloc[-1] else "FLAT")
    return {"price":price,"ema20":float(e20.iloc[-1]),"ema50":float(e50.iloc[-1]),"ema200":float(e200.iloc[-1]),"rsi":float(rr) if pd.notna(rr) else np.nan,"atr":float(at) if pd.notna(at) else np.nan,"high52":high52,"low52":low52,"vol_ratio":vol/v20 if v20 else 1,"trend":trend,"dist_high":(high52-price)/high52*100 if high52 else np.nan,"dist_low":(price-low52)/low52*100 if low52 else np.nan}

def selection_score(s):
    score=0; reasons=[]
    if s["trend"] in ("BULLISH","BEARISH"): score+=25; reasons.append(f"EMA20 / EMA50 {s['trend'].lower()}")
    if s["price"]>s["ema200"]: score+=15; reasons.append("Above EMA200")
    if 45<=s["rsi"]<=68: score+=15; reasons.append("Healthy RSI")
    elif s["rsi"]>70: score+=5; reasons.append("RSI hot")
    if s["vol_ratio"]>=1.5: score+=20; reasons.append("Volume expansion")
    elif s["vol_ratio"]>=1.15: score+=10; reasons.append("Volume above average")
    if s["dist_high"]<=8: score+=15; reasons.append("Near 52W high")
    return min(score,100),reasons

# =========================
# VS FLOW ENGINES — unchanged architecture
# =========================
def structure_score(d):
    if d.empty or len(d)<20:return {"score":0,"side":"WAIT","reason":"Insufficient data"}
    c=d["Close"].astype(float); h=d["High"].astype(float); ema20=c.ewm(span=20,adjust=False).mean().iloc[-1]; ema50=c.ewm(span=50,adjust=False).mean().iloc[-1] if len(c)>=50 else ema20
    price=float(c.iloc[-1]); prev20_high=float(h.iloc[-21:-1].max()) if len(h)>21 else float(h.max()); prev20_low=float(d["Low"].iloc[-21:-1].min()) if len(d)>21 else float(d["Low"].min())
    up=price>ema20>ema50; down=price<ema20<ema50; score=0; side="WAIT"; reasons=[]
    if up:score+=1;side="BUY";reasons.append("HTF bullish structure")
    if down:score+=1;side="SELL";reasons.append("HTF bearish structure")
    if price>=prev20_high:score+=1;side="BUY";reasons.append("Breakout")
    if price<=prev20_low:score+=1;side="SELL";reasons.append("Breakdown")
    vol=d["Volume"].fillna(0).astype(float); vr=float(vol.iloc[-1]/vol.tail(20).mean()) if vol.tail(20).mean() else 1
    if vr>=1.4:score+=1;reasons.append("Volume expansion")
    move=abs(price/float(c.iloc[-5])-1)*100 if len(c)>=5 else 0
    if move>=2:score+=1;reasons.append("Displacement")
    return {"score":min(score,5),"side":side,"reason":", ".join(reasons) or "No clear alignment"}

def mtf_setup(ticker):
    frames=[]
    configs=[("4H","60d","1h"),("1H","30d","1h"),("15M","30d","15m"),("5M","7d","5m")]
    for label,period,interval in configs:
        d=history(ticker,period,interval)
        if label=="4H" and not d.empty:
            d=d.copy(); d.index=pd.to_datetime(d.index); d=d.resample("4h").agg({"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}).dropna()
        if d.empty:frames.append({"tf":label,"status":"NO DATA","side":"WAIT","detail":"Provider unavailable"});continue
        x=structure_score(d);frames.append({"tf":label,"status":f'{x["score"]}/5',"side":x["side"],"detail":x["reason"]})
    valid=[x for x in frames if x["status"]!="NO DATA"];buy=sum(x["side"]=="BUY" for x in valid);sell=sum(x["side"]=="SELL" for x in valid)
    overall="BUY" if buy>=3 and buy>sell else "SELL" if sell>=3 and sell>buy else "WAIT"
    return frames,overall

def core_structure(x,n=5):
    if len(x)<n*2+3:return "WAIT"
    hi=x.High.iloc[-n-1:-1].max();lo=x.Low.iloc[-n-1:-1].min();last=x.iloc[-1]
    if last.Close>hi:return "BULL BOS"
    if last.Close<lo:return "BEAR BOS"
    return "WAIT"

def core_liquidity_sweep(x,n=5):
    if len(x)<n+3:return "WAIT"
    hi=x.High.iloc[-n-1:-1].max();lo=x.Low.iloc[-n-1:-1].min();last=x.iloc[-1]
    if last.High>hi and last.Close<hi:return "BSL SWEPT"
    if last.Low<lo and last.Close>lo:return "SSL SWEPT"
    return "WAIT"

def core_order_block(x):
    if len(x)<25:return None
    for i in range(len(x)-2,max(2,len(x)-30),-1):
        cur=x.iloc[i];prev=x.iloc[i-1];rng=max(float(cur.High-cur.Low),1e-9);body=abs(float(cur.Close-cur.Open))
        if body/rng<.55:continue
        if cur.Close>cur.Open and prev.Close<prev.Open and cur.Close>prev.High:return {"side":"BUY","type":"BULL OB","low":float(prev.Low),"high":float(prev.Open)}
        if cur.Close<cur.Open and prev.Close>prev.Open and cur.Close<prev.Low:return {"side":"SELL","type":"BEAR OB","low":float(prev.Open),"high":float(prev.High)}
    return None

def core_fvg(x):
    if len(x)<5:return None
    for i in range(len(x)-1,1,-1):
        a,b,c=x.iloc[i-2],x.iloc[i-1],x.iloc[i]
        if c.Low>a.High:return {"side":"BUY","type":"BULL FVG"}
        if c.High<a.Low:return {"side":"SELL","type":"BEAR FVG"}
    return None

def core_analyze(ticker,name=""):
    h1=history(ticker,"6mo","1h");m15=history(ticker,"60d","15m");m5=history(ticker,"30d","5m")
    base={"Symbol":ticker,"Name":name or ticker,"4H OB":"WAIT","1H Sweep":"WAIT","1H BOS":"WAIT","15M FVG":"WAIT","5M Trigger":"WAIT","Score":"0/5","Signal":"WAIT","Entry":"","SL":"","TP":"","RR":"","Chart Tally":"PENDING"}
    if h1.empty or m15.empty or m5.empty:base["Signal"]="NO DATA";return base
    h4=h1.copy();h4.index=pd.to_datetime(h4.index);h4=h4.resample("4h").agg({"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}).dropna();ob=core_order_block(h4)
    if not ob:return base
    side=ob["side"];sw=core_liquidity_sweep(h1);bos=core_structure(h1);fv=core_fvg(m15);tr=core_structure(m5)
    base.update({"4H OB":ob["type"],"1H Sweep":sw,"1H BOS":bos,"15M FVG":fv["type"] if fv else "WAIT","5M Trigger":("5M BULL BOS" if tr=="BULL BOS" else "5M BEAR BOS" if tr=="BEAR BOS" else "WAIT")})
    checks=[True,(side=="BUY" and bos=="BULL BOS") or (side=="SELL" and bos=="BEAR BOS"),(side=="BUY" and sw=="SSL SWEPT") or (side=="SELL" and sw=="BSL SWEPT"),(side=="BUY" and fv and fv["side"]=="BUY") or (side=="SELL" and fv and fv["side"]=="SELL"),(side=="BUY" and tr=="BULL BOS") or (side=="SELL" and tr=="BEAR BOS")]
    score=int(sum(bool(x) for x in checks));price=float(m5.Close.iloc[-1]);sl=ob["low"] if side=="BUY" else ob["high"];risk=price-sl if side=="BUY" else sl-price
    base["Score"]=f"{score}/5"
    if risk>0:
        base.update({"Signal":("A+ BUY" if side=="BUY" else "A+ SELL") if score==5 else ("SETUP BUY" if side=="BUY" else "SETUP SELL") if score>=4 else "WAIT","Entry":round(price,4),"SL":round(sl,4),"TP":round(price+2*risk if side=="BUY" else price-2*risk,4),"RR":"1:2","Chart Tally":"COMPLETE" if score==5 else "PENDING"})
    return base

def smc_scalp_analyze(ticker,name=""):
    h4=history(ticker,"180d","1h");m5=history(ticker,"30d","5m");
    base={"Symbol":ticker,"Name":name or ticker,"4H Direction":"WAIT","4H Zone":"WAIT","5M Sweep":"WAIT","5M MSS":"WAIT","5M FVG":"WAIT","FVG Retest":"WAIT","Score":"0/6","Signal":"WAIT","Entry":None,"SL":None,"TP":None,"RR":None}
    if h4.empty or m5.empty:return base
    h4=h4.copy();h4.index=pd.to_datetime(h4.index);h4=h4.resample("4h").agg({"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}).dropna()
    if len(h4)<30 or len(m5)<30:return base
    c=h4.Close.astype(float);e20=c.ewm(span=20,adjust=False).mean().iloc[-1];e50=c.ewm(span=50,adjust=False).mean().iloc[-1];direction="BUY" if e20>e50 else "SELL" if e20<e50 else "WAIT"
    eq=(float(h4.High.iloc[-20:].max())+float(h4.Low.iloc[-20:].min()))/2;close4=float(h4.Close.iloc[-1]);zone="DISCOUNT" if close4<eq else "PREMIUM" if close4>eq else "EQUILIBRIUM"
    sweep=core_liquidity_sweep(m5,8);mss=core_structure(m5,5);fvg=core_fvg(m5);retest="WAIT"
    if fvg and ((direction=="BUY" and fvg["side"]=="BUY") or (direction=="SELL" and fvg["side"]=="SELL")):retest="FVG RETEST WATCH"
    checks=[direction in ("BUY","SELL"),(zone=="DISCOUNT" if direction=="BUY" else zone=="PREMIUM"),(sweep==("SSL SWEPT" if direction=="BUY" else "BSL SWEPT")),(mss==("BULL BOS" if direction=="BUY" else "BEAR BOS")),bool(fvg and fvg["side"]==("BUY" if direction=="BUY" else "SELL")),retest!="WAIT"]
    score=sum(checks);price=float(m5.Close.iloc[-1]);entry=price;sl=float(m5.Low.iloc[-1]) if direction=="BUY" else float(m5.High.iloc[-1]);risk=entry-sl if direction=="BUY" else sl-entry;tp=entry+2*risk if direction=="BUY" else entry-2*risk
    signal=("A+ BUY" if direction=="BUY" else "A+ SELL") if score>=5 else ("WATCH BUY" if direction=="BUY" else "WATCH SELL") if score>=4 else "WAIT"
    base.update({"4H Direction":direction,"4H Zone":zone,"5M Sweep":sweep,"5M MSS":mss,"5M FVG":fvg["type"] if fvg else "WAIT","FVG Retest":retest,"Score":f"{score}/6","Signal":signal,"Entry":round(entry,6),"SL":round(sl,6),"TP":round(tp,6) if risk>0 else None,"RR":"1:2" if risk>0 else None})
    return base


# =========================
# AMD + iFVG ENGINE — additive module
# =========================
def atr14(x):
    """Return 14-period Average True Range as a scalar."""
    if x is None or len(x) < 15:
        return 0.0
    h=x.High.astype(float); l=x.Low.astype(float); c=x.Close.astype(float)
    prev=c.shift(1)
    tr=pd.concat([(h-l),(h-prev).abs(),(l-prev).abs()],axis=1).max(axis=1)
    value=tr.rolling(14).mean().iloc[-1]
    return float(value) if pd.notna(value) else 0.0

def amd_phase_global(x, lookback=20):
    """Conservative Accumulation → Manipulation → Distribution detector."""
    if x is None or len(x) < lookback + 8:
        return {"phase":"WAIT","side":None,"sweep":"WAIT","displacement":False}
    z=x.tail(lookback+8).copy(); base=z.iloc[:-8]; recent=z.tail(8)
    hi=float(base.High.max()); lo=float(base.Low.min())
    buy_sweep=sell_sweep=False
    for _,r in recent.iloc[:5].iterrows():
        buy_sweep = buy_sweep or (float(r.Low)<lo and float(r.Close)>lo)
        sell_sweep = sell_sweep or (float(r.High)>hi and float(r.Close)<hi)
    last=recent.iloc[-1]
    rng=max(float(last.High-last.Low),1e-9); body=abs(float(last.Close-last.Open))
    atr=atr14(z); disp=body/rng>=0.65 and (atr<=0 or rng>=atr*0.8)
    if buy_sweep and float(last.Close)>hi and disp:
        return {"phase":"DISTRIBUTION","side":"BUY","sweep":"SSL SWEPT","displacement":True}
    if sell_sweep and float(last.Close)<lo and disp:
        return {"phase":"DISTRIBUTION","side":"SELL","sweep":"BSL SWEPT","displacement":True}
    if buy_sweep:return {"phase":"MANIPULATION","side":"BUY","sweep":"SSL SWEPT","displacement":disp}
    if sell_sweep:return {"phase":"MANIPULATION","side":"SELL","sweep":"BSL SWEPT","displacement":disp}
    return {"phase":"ACCUMULATION","side":None,"sweep":"WAIT","displacement":False}

def inverse_fvg_global(x, side=None):
    """Detect an FVG that was invalidated and is now behaving as an inverse FVG."""
    if x is None or len(x)<12:return None
    for i in range(len(x)-4,1,-1):
        a,b,c=x.iloc[i-2],x.iloc[i-1],x.iloc[i]
        # Bullish FVG -> bearish iFVG after decisive loss below the gap.
        if float(c.Low)>float(a.High):
            low=float(a.High); high=float(c.Low); later=x.iloc[i+1:]
            if side in ("SELL",None) and any(float(r.Close)<low for _,r in later.iterrows()):
                last=x.iloc[-1]; retest=float(last.High)>=low and float(last.Low)<=high
                return {"side":"SELL","type":"BEAR iFVG","low":low,"high":high,"retest":retest}
        # Bearish FVG -> bullish iFVG after decisive reclaim above the gap.
        if float(c.High)<float(a.Low):
            low=float(c.High); high=float(a.Low); later=x.iloc[i+1:]
            if side in ("BUY",None) and any(float(r.Close)>high for _,r in later.iterrows()):
                last=x.iloc[-1]; retest=float(last.Low)<=high and float(last.High)>=low
                return {"side":"BUY","type":"BULL iFVG","low":low,"high":high,"retest":retest}
    return None

def amd_ifvg_analyze_global(ticker, name=""):
    d=history(ticker,"3y","1d"); h4src=history(ticker,"6mo","1h"); h1=history(ticker,"60d","1h"); m15=history(ticker,"30d","15m")
    base={"Symbol":ticker,"Name":name or ticker,"HTF Bias":"WAIT","AMD":"WAIT","Sweep":"WAIT","MSS":"WAIT","Displacement":"WAIT","iFVG":"WAIT","iFVG Retest":"WAIT","Score":"0/5","Signal":"WAIT"}
    if min(len(d),len(h4src),len(h1),len(m15))<30:return base
    h4=h4src.copy(); h4.index=pd.to_datetime(h4.index); h4=h4.resample("4h").agg({"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}).dropna()
    if len(h4)<30:return base
    def bias(x):
        c=x.Close.astype(float); e20=c.ewm(span=20,adjust=False).mean().iloc[-1]; e50=c.ewm(span=50,adjust=False).mean().iloc[-1]; last=float(c.iloc[-1])
        return "BULLISH" if last>e20>e50 else "BEARISH" if last<e20<e50 else "MIXED"
    hb=bias(h4); amd=amd_phase_global(h1); side=amd["side"]
    if not side:return base|{"HTF Bias":hb,"AMD":amd["phase"],"Sweep":amd["sweep"]}
    mss=core_structure(h1); mss_ok=(side=="BUY" and mss=="BULL BOS") or (side=="SELL" and mss=="BEAR BOS")
    ifvg=inverse_fvg_global(m15,side); disp=amd["displacement"]
    htf_ok=(side=="BUY" and hb=="BULLISH") or (side=="SELL" and hb=="BEARISH")
    ifvg_ok=bool(ifvg and ifvg["side"]==side and ifvg["retest"])
    score=int(sum([htf_ok,amd["phase"]=="DISTRIBUTION",mss_ok,disp,ifvg_ok]))
    signal=("AMD+iFVG BUY" if side=="BUY" else "AMD+iFVG SELL") if score>=4 else ("WATCH BUY" if side=="BUY" else "WATCH SELL")
    base.update({"HTF Bias":hb,"AMD":amd["phase"],"Sweep":amd["sweep"],"MSS":mss,"Displacement":"YES" if disp else "WAIT","iFVG":ifvg["type"] if ifvg and ifvg["side"]==side else "WAIT","iFVG Retest":"YES" if ifvg_ok else "WAIT","Score":f"{score}/5","Signal":signal})
    return base

def classic_analyze(ticker,name=""):
    d=history(ticker,"6mo","1d");base={"Symbol":ticker,"Name":name or ticker,"Key Level":"WAIT","Trendline":"WAIT","Breakout/Breakdown":"WAIT","Price Action":"WAIT","Candle Close":"WAIT","Score":"0/5","Signal":"WAIT","Entry":None,"SL":None,"TP":None,"RR":None}
    if d.empty or len(d)<30:return base
    last=d.iloc[-1];c=d.Close.astype(float);recent_hi=float(d.High.iloc[-21:-1].max());recent_lo=float(d.Low.iloc[-21:-1].min());body=abs(float(last.Close-last.Open));rng=max(float(last.High-last.Low),1e-9);upper=float(last.High-max(last.Open,last.Close));lower=float(min(last.Open,last.Close)-last.Low)
    bias="BUY" if float(last.Close)>recent_hi else "SELL" if float(last.Close)<recent_lo else "WAIT";key="BREAKOUT" if bias=="BUY" else "BREAKDOWN" if bias=="SELL" else "INSIDE RANGE";trend="UP" if c.ewm(span=20,adjust=False).mean().iloc[-1]>c.ewm(span=50,adjust=False).mean().iloc[-1] else "DOWN"
    pa="BULLISH REJECTION" if lower>body*1.5 and float(last.Close)>float(last.Open) else "BEARISH REJECTION" if upper>body*1.5 and float(last.Close)<float(last.Open) else "NEUTRAL";close="CONFIRMED" if bias in ("BUY","SELL") else "WAIT"
    checks=[bias in ("BUY","SELL"),trend==("UP" if bias=="BUY" else "DOWN") if bias in ("BUY","SELL") else False,(bias=="BUY" and pa.startswith("BULL")) or (bias=="SELL" and pa.startswith("BEAR")),close=="CONFIRMED",abs(float(last.Close)- (recent_hi if bias=="BUY" else recent_lo if bias=="SELL" else float(last.Close)))/max(abs(float(last.Close)),1e-9)<.03]
    score=sum(checks);entry=float(last.Close);sl=float(last.Low) if bias=="BUY" else float(last.High);risk=entry-sl if bias=="BUY" else sl-entry
    base.update({"Key Level":key,"Trendline":trend,"Breakout/Breakdown":key,"Price Action":pa,"Candle Close":close,"Score":f"{score}/5","Signal":("BUY" if bias=="BUY" else "SELL" if bias=="SELL" else "WAIT") if score>=3 else "WAIT","Entry":round(entry,6),"SL":round(sl,6),"TP":round(entry+2*risk if bias=="BUY" else entry-2*risk,6) if risk>0 else None,"RR":"1:2" if risk>0 else None})
    return base

# Strategy lab
def _strategy_daily(ticker): return history(ticker,"1y","1d")
def strategy_smc(d):
    x=structure_score(d);return {"score":x["score"],"bias":x["side"],"reason":x["reason"]}
def strategy_price_action(d):
    if d.empty:return {"score":0,"bias":"WAIT","reason":"No data"}
    last=d.iloc[-1];rng=max(float(last.High-last.Low),1e-9);body=abs(float(last.Close-last.Open));upper=float(last.High-max(last.Open,last.Close));lower=float(min(last.Open,last.Close)-last.Low);recent_hi=float(d.High.iloc[-21:-1].max());recent_lo=float(d.Low.iloc[-21:-1].min());score=0;bias="WAIT";reasons=[]
    if float(last.Close)>recent_hi:score+=2;bias="BUY";reasons.append("Key-high acceptance")
    elif float(last.Close)<recent_lo:score+=2;bias="SELL";reasons.append("Key-low acceptance")
    elif lower>body*1.5 and float(last.Close)>float(last.Open):score+=2;bias="BUY";reasons.append("Bullish rejection")
    elif upper>body*1.5 and float(last.Close)<float(last.Open):score+=2;bias="SELL";reasons.append("Bearish rejection")
    if bias=="BUY" and abs(float(last.Close)-recent_hi)/max(recent_hi,1e-9)<.01:score+=1;reasons.append("Near prior high")
    if bias=="SELL" and abs(float(last.Close)-recent_lo)/max(recent_lo,1e-9)<.01:score+=1;reasons.append("Near prior low")
    return {"score":min(score,4),"bias":bias,"reason":", ".join(reasons) or "No clear price action"}
def strategy_breakout_retest(d):
    if d.empty:return {"score":0,"bias":"WAIT","reason":"No data"}
    c=d.Close.astype(float);hi=d.High.iloc[-21:-1].max();lo=d.Low.iloc[-21:-1].min();last=float(c.iloc[-1]);score=0;bias="WAIT";reasons=[]
    if last>hi:score=3;bias="BUY";reasons.append("Range breakout")
    elif last<lo:score=3;bias="SELL";reasons.append("Range breakdown")
    return {"score":score,"bias":bias,"reason":", ".join(reasons) or "No breakout"}
def strategy_fibonacci(d):
    if d.empty:return {"score":0,"bias":"WAIT","reason":"No data"}
    hi=float(d.High.tail(60).max());lo=float(d.Low.tail(60).min());price=float(d.Close.iloc[-1]);r=hi-lo;levels=[hi-r*.382,hi-r*.5,hi-r*.618];dist=min(abs(price-x) for x in levels)/max(price,1e-9)
    return {"score":3 if dist<.01 else 1,"bias":"BUY" if price>levels[1] else "SELL","reason":"Near Fibonacci retracement" if dist<.01 else "Fibonacci context"}
def strategy_momentum(d):
    if d.empty:return {"score":0,"bias":"WAIT","reason":"No data"}
    c=d.Close.astype(float);e20=c.ewm(span=20,adjust=False).mean();e50=c.ewm(span=50,adjust=False).mean();rr=float(rsi(c).iloc[-1]);vr=float(d.Volume.iloc[-1]/d.Volume.tail(20).mean()) if d.Volume.tail(20).mean() else 1;score=0;bias="WAIT";reasons=[]
    if e20.iloc[-1]>e50.iloc[-1]>c.ewm(span=200,adjust=False).mean().iloc[-1]:bias="BUY";score+=2;reasons.append("EMA alignment")
    elif e20.iloc[-1]<e50.iloc[-1]<c.ewm(span=200,adjust=False).mean().iloc[-1]:bias="SELL";score+=2;reasons.append("EMA alignment")
    if bias=="BUY" and 50<=rr<=68:score+=1;reasons.append("RSI momentum")
    if bias=="SELL" and 32<=rr<=50:score+=1;reasons.append("RSI momentum")
    if vr>=1.3:score+=1;reasons.append("Volume expansion")
    return {"score":min(score,4),"bias":bias if score>=2 else "WAIT","reason":", ".join(reasons) or "No clean momentum alignment"}
def strategy_suite(ticker):
    d=_strategy_daily(ticker)
    if d.empty:return pd.DataFrame(),{"overall":"NO DATA","confidence":0}
    funcs=[("SMC",strategy_smc,5),("PRICE ACTION",strategy_price_action,4),("BREAKOUT + RETEST",strategy_breakout_retest,3),("FIBONACCI",strategy_fibonacci,3),("MOMENTUM",strategy_momentum,4)];rows=[]
    for name,fn,maxs in funcs:
        r=fn(d);rows.append({"Strategy":name,"Score":f"{r['score']}/{maxs}","Bias":r["bias"],"Reason":r["reason"]})
    buy=sum(r["Bias"]=="BUY" for r in rows);sell=sum(r["Bias"]=="SELL" for r in rows);overall="BUY" if buy>=3 else "SELL" if sell>=3 else "MIXED / WAIT";conf=int(min(95,50+max(buy,sell)*9-(5 if buy==sell else 0)))
    return pd.DataFrame(rows),{"overall":overall,"confidence":conf,"buy":buy,"sell":sell}

# =========================
# GLOBAL OPTIONS — yfinance instead of exchange-specific chain
# =========================
def option_chain(symbol, expiry):
    if yf is None:return pd.DataFrame()
    try:
        oc=yf.Ticker(symbol).option_chain(expiry)
        ce=oc.calls.copy();pe=oc.puts.copy()
        ce=ce[[c for c in ["strike","openInterest","change","volume","impliedVolatility","lastPrice","bid","ask"] if c in ce]].rename(columns={"openInterest":"CE_OI","change":"CE_CHG","volume":"CE_VOL","impliedVolatility":"CE_IV","lastPrice":"CE_LTP","bid":"CE_BID","ask":"CE_ASK"})
        pe=pe[[c for c in ["strike","openInterest","change","volume","impliedVolatility","lastPrice","bid","ask"] if c in pe]].rename(columns={"openInterest":"PE_OI","change":"PE_CHG","volume":"PE_VOL","impliedVolatility":"PE_IV","lastPrice":"PE_LTP","bid":"PE_BID","ask":"PE_ASK"})
        out=pd.merge(ce,pe,on="strike",how="outer").rename(columns={"strike":"STRIKE"}).fillna(0)
        # yfinance exposes change in premium, not change-OI; retain explicit columns for UI compatibility.
        out["CE_CHG_OI"]=0;out["PE_CHG_OI"]=0
        return out
    except Exception:return pd.DataFrame()

def option_expiries(symbol):
    if yf is None:return []
    try:return list(yf.Ticker(symbol).options or [])
    except Exception:return []

def max_pain(df):
    if df.empty:return np.nan
    strikes=df.STRIKE.astype(float).dropna().unique();best=None
    for k in strikes:
        call=(np.maximum(k-df.STRIKE.astype(float),0)*df.CE_OI.fillna(0)).sum();put=(np.maximum(df.STRIKE.astype(float)-k,0)*df.PE_OI.fillna(0)).sum();pain=call+put
        if best is None or pain<best[0]:best=(pain,k)
    return float(best[1]) if best else np.nan

def option_analysis(df,spot):
    if df.empty:return {}
    d=df.copy().sort_values("STRIKE");spot=float(spot) if spot is not None and pd.notna(spot) else float(d.STRIKE.median());atm=float(d.iloc[(d.STRIKE.astype(float)-spot).abs().argsort()[:1]].STRIKE.iloc[0]);call_oi=float(d.CE_OI.sum());put_oi=float(d.PE_OI.sum());pcr=put_oi/call_oi if call_oi else np.nan;call_wall=float(d.loc[d.CE_OI.idxmax(),"STRIKE"]) if d.CE_OI.sum()>0 else np.nan;put_wall=float(d.loc[d.PE_OI.idxmax(),"STRIKE"]) if d.PE_OI.sum()>0 else np.nan
    if pcr>=1.15:bias="BULLISH"
    elif pcr<=.8:bias="BEARISH"
    else:bias="NEUTRAL"
    confidence=int(min(95,max(45,55+abs(pcr-1)*35)))
    return {"spot":spot,"atm":atm,"call_oi":call_oi,"put_oi":put_oi,"pcr":pcr,"call_wall":call_wall,"put_wall":put_wall,"max_pain":max_pain(d),"bias":bias,"confidence":confidence}

def trade_plan(df,ana):
    if df.empty or not ana:return {}
    atm=ana["atm"];bias=ana["bias"]
    if bias=="BULLISH":row=df[df.STRIKE>=atm].sort_values("STRIKE").head(1);side="CALL";premium=float(row.CE_LTP.iloc[0]) if not row.empty else 0;strike=float(row.STRIKE.iloc[0]) if not row.empty else 0
    elif bias=="BEARISH":row=df[df.STRIKE<=atm].sort_values("STRIKE",ascending=False).head(1);side="PUT";premium=float(row.PE_LTP.iloc[0]) if not row.empty else 0;strike=float(row.STRIKE.iloc[0]) if not row.empty else 0
    else:return {"side":"WAIT","reason":"Neutral option structure"}
    if premium<=0:return {"side":"WAIT","reason":"No valid premium"}
    return {"side":side,"strike":strike,"option":f"{strike:g} {side}","entry":premium,"sl":premium*.70,"tp1":premium*1.5,"tp2":premium*2,"rr":"1:1.67 / 1:3.33","reason":"PCR structure supports directional bias","class":"GLOBAL OPTIONS"}

def hero_zero_candidates(df,ana):
    if df.empty or not ana:return pd.DataFrame()
    spot=float(ana["spot"]);atm=float(ana["atm"]);bias=ana["bias"];rows=[]
    for _,r in df.iterrows():
        k=float(r.STRIKE);dist=abs(k-spot)/spot*100 if spot else 999
        if dist<.25 or dist>3:continue
        side="CALL" if bias=="BULLISH" else "PUT" if bias=="BEARISH" else ("CALL" if k>spot else "PUT");ltp=float(r.CE_LTP if side=="CALL" else r.PE_LTP);oi=float(r.CE_OI if side=="CALL" else r.PE_OI);vol=float(r.CE_VOL if side=="CALL" else r.PE_VOL);iv=float(r.CE_IV if side=="CALL" else r.PE_IV)
        if ltp<=0 or oi<=0 or vol<=0:continue
        atmrow=df.iloc[(df.STRIKE.astype(float)-atm).abs().argsort()[:1]].iloc[0];atm_prem=float(atmrow.CE_LTP if side=="CALL" else atmrow.PE_LTP)
        if atm_prem>0 and ltp>atm_prem*.55:continue
        score=40+min(20,(vol/max(1,oi))*200)+10 if .5<=dist<=2 else 40+min(20,(vol/max(1,oi))*200);score+=10 if iv<=.35 else 0;score=int(min(95,round(score)))
        rows.append({"Side":side,"Strike":k,"Premium":round(ltp,4),"Distance %":round(dist,2),"OI":int(oi),"Volume":int(vol),"IV %":round(iv*100,2),"Score":score,"Entry":round(ltp,4),"SL":round(ltp*.55,4),"TP1":round(ltp*1.8,4),"TP2":round(ltp*2.5,4),"RR":"1:1.78 / 1:3.33"})
    out=pd.DataFrame(rows);return out.sort_values(["Score","Volume"],ascending=False).head(10) if not out.empty else out

# =========================
# DASHBOARD HELPERS
# =========================
def market_regime():
    rows=[]
    for t,n in list(GLOBAL_INDEXES.items())[:8]:
        d=history(t,"6mo","1d")
        if d.empty or len(d)<50:continue
        c=d.Close.astype(float);e20=c.ewm(span=20,adjust=False).mean().iloc[-1];e50=c.ewm(span=50,adjust=False).mean().iloc[-1];rows.append((n,"BULLISH" if e20>e50 else "BEARISH" if e20<e50 else "RANGE"))
    bull=sum(x[1]=="BULLISH" for x in rows);bear=sum(x[1]=="BEARISH" for x in rows);return ("BULLISH" if bull>=5 else "BEARISH" if bear>=5 else "MIXED / RANGE"),rows

def setup_cards(df):
    if df.empty:return
    for _,r in df.iterrows():
        sig=str(r.get("Signal","WAIT"));score=str(r.get("Score","0/5"));cls="green" if "BUY" in sig else "red" if "SELL" in sig else "gold"
        st.markdown(f'''<div class="setup-card"><div class="setup-top"><b>{r.get("Symbol","")}</b><span class="pill {cls}">{sig}</span><span class="pill">{score}</span></div><div class="setup-grid"><div><span>4H</span><b>{r.get("4H OB","")}</b></div><div><span>1H SWEEP</span><b>{r.get("1H Sweep","")}</b></div><div><span>1H BOS</span><b>{r.get("1H BOS","")}</b></div><div><span>15M FVG</span><b>{r.get("15M FVG","")}</b></div><div><span>5M</span><b>{r.get("5M Trigger","")}</b></div><div><span>RR</span><b>{r.get("RR","")}</b></div></div><div class="trade-line"><span>ENTRY <b>{r.get("Entry","")}</b></span><span>SL <b>{r.get("SL","")}</b></span><span>TP <b>{r.get("TP","")}</b></span><span>TALLY <b>{r.get("Chart Tally","")}</b></span></div></div>''',unsafe_allow_html=True)

def open_asset(ticker):
    st.session_state.selected=ticker;st.session_state.page="ASSET DETAIL";st.rerun()

# =========================
# NAVIGATION
# =========================
if "page" not in st.session_state:st.session_state.page="HOME"
if "selected" not in st.session_state:st.session_state.selected="BTC-USD"
if "amd_ifvg_scan" not in st.session_state:st.session_state.amd_ifvg_scan=pd.DataFrame()

with st.sidebar:
    if LOGO.exists():st.image(str(LOGO),use_container_width=True)
    st.markdown('<div class="vs-brand">⚡ VS FLOW <span class="global">GLOBAL 🌍</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="vs-sub">SCAN • ANALYSE • TRADE • GLOBAL</div>',unsafe_allow_html=True)
    st.markdown("")
    nav=[("🏠","HOME"),("🌍","GLOBAL ASSETS"),("🎯","SMART GLOBAL FINDER"),("📊","GLOBAL INDICES"),("₿","CRYPTO MARKET"),("🔥","VS FLOW SETUP"),("🧠","AMD + iFVG SCANNER"),("⛓️","OPTIONS ANALYSIS"),("💀","HERO-ZERO"),("🧠","STRATEGY LAB"),("⚡","SMC 4H→5M SCALP"),("📐","CLASSIC PRICE ACTION"),("🧮","RISK CALCULATOR")]
    for icon,label in nav:
        if st.button(f"{icon}  {label}",key="nav_"+label,use_container_width=True):st.session_state.page=label;st.rerun()
    st.markdown("### ⚡ Quick Global Asset")
    custom=st.text_input("Yahoo ticker",placeholder="e.g. SPY, QQQ, BTC-USD, GC=F",key="custom_ticker")
    if st.button("OPEN CUSTOM",use_container_width=True,key="open_custom") and custom.strip():
        st.session_state.selected=custom.strip().upper();st.session_state.page="ASSET DETAIL";st.rerun()
    st.markdown('<div class="side-note"><b>Global Universe</b><br>Global indices • US/International equities • FX • commodities • rates • major crypto.<br><br><b>Data</b><br>Yahoo Finance via yfinance; quotes/charts are cached and loaded on demand.<br><br><b>Owner</b><br>vaibhav shirsat</div>',unsafe_allow_html=True)

# Global fast search
search=st.text_input("",placeholder="🔎 Search global asset, index, crypto, FX or commodity — e.g. BTC, NVIDIA, GOLD, NASDAQ",label_visibility="collapsed")
if search.strip():
    q=search.strip().lower();matches=[m for t,m in ASSET_META.items() if q in t.lower() or q in m["name"].lower() or q in m["group"].lower()][:20]
    if matches:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        for i,m in enumerate(matches):
            c1,c2,c3=st.columns([1.5,5,1]);c1.markdown(f"**{m['symbol']}**");c2.write(f"{m['name']} • {m['group']} • {m['region']}")
            if c3.button("OPEN",key=f"search_open_{i}_{m['symbol']}"):open_asset(m["symbol"])
        st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="hero" style="position:relative"><div class="owner-badge">vaibhav shirsat</div><h1>VS FLOW GLOBAL 🌍</h1><p>Global Indices • Global Equities • FX • Commodities • Rates • Major Crypto • Core Setup • SMC 4H→5M • Classic • Options • Hero-Zero • Strategy Lab</p><div class="gradient"></div></div>',unsafe_allow_html=True)
page=st.session_state.page

# =========================
# HOME — GLOBAL COMMAND CENTER
# =========================
if page=="HOME":
    st.markdown('<div class="section">🌐 GLOBAL MARKET COMMAND CENTER <small>decision-first global dashboard</small></div>',unsafe_allow_html=True)
    regime,regime_rows=market_regime();rc1,rc2,rc3=st.columns([1.1,2.2,2.2])
    with rc1:
        cls="green" if regime=="BULLISH" else "red" if regime=="BEARISH" else "gold";st.markdown(f'<div class="panel"><span class="pill {cls}">GLOBAL REGIME</span><div class="regime">{regime}</div><small>EMA20 / EMA50 benchmark breadth</small></div>',unsafe_allow_html=True)
    with rc2:
        st.markdown('<div class="panel"><b>GLOBAL BENCHMARK BREADTH</b><br><br>'+" &nbsp; ".join([f'<span class="pill {"green" if s=="BULLISH" else "red" if s=="BEARISH" else "gold"}">{n}: {s}</span>' for n,s in regime_rows])+'</div>',unsafe_allow_html=True)
    with rc3:
        st.markdown(f'<div class="panel"><span class="pill green">GLOBAL ASSETS</span><div class="regime">{len(ALL_TICKERS):,}</div><small>Curated global market universe</small></div>',unsafe_allow_html=True)
    a1,a2,a3=st.columns(3)
    with a1:
        if st.button("OPEN GLOBAL INDICES",key="open_regime",use_container_width=True):st.session_state.page="GLOBAL INDICES";st.rerun()
    with a2:
        if st.button("OPEN CRYPTO MARKET",key="open_crypto",use_container_width=True):st.session_state.page="CRYPTO MARKET";st.rerun()
    with a3:
        if st.button("OPEN GLOBAL UNIVERSE",key="open_universe",use_container_width=True):st.session_state.page="GLOBAL ASSETS";st.rerun()

    st.markdown('<div class="section">📊 GLOBAL BENCHMARKS <small>click OPEN for full asset detail</small></div>',unsafe_allow_html=True)
    pulse=list(GLOBAL_INDEXES.items())[:8];cols=st.columns(4)
    for i,(t,n) in enumerate(pulse):
        r=quote(t)
        with cols[i%4]:
            if r:
                cls="up" if r["chg"]>0 else "down" if r["chg"]<0 else "flat";st.markdown(f'<div class="card"><div class="label">{n}</div><div class="value">{r["price"]:,.2f}</div><div class="{cls}">{r["chg"]:+.2f}%</div><div class="click-hint">Chart + technicals + MTF + setup</div></div>',unsafe_allow_html=True)
            else:st.markdown(f'<div class="card"><div class="label">{n}</div><div class="value">—</div><div class="flat">Unavailable</div></div>',unsafe_allow_html=True)
            if st.button("OPEN",key=f"home_idx_open_{i}",use_container_width=True):open_asset(t)

    st.markdown('<div class="section">₿ MAJOR CRYPTO MARKET <small>24/7 • clickable • full VS FLOW analysis</small></div>',unsafe_allow_html=True)
    crypto_items=list(CRYPTO.items())[:10];cols=st.columns(5)
    for i,(t,n) in enumerate(crypto_items):
        r=quote(t)
        with cols[i%5]:
            if r:
                cls="up" if r["chg"]>0 else "down" if r["chg"]<0 else "flat";st.markdown(f'<div class="card crypto-card"><div class="label">₿ {n}</div><div class="value">{r["price"]:,.4f}</div><div class="{cls}">{r["chg"]:+.2f}%</div></div>',unsafe_allow_html=True)
            else:st.markdown(f'<div class="card crypto-card"><div class="label">₿ {n}</div><div class="value">—</div><div class="flat">Unavailable</div></div>',unsafe_allow_html=True)
            if st.button("OPEN",key=f"crypto_open_{i}",use_container_width=True):open_asset(t)

    st.markdown('<div class="section">🌍 GLOBAL MARKET PULSE <small>cross-asset context</small></div>',unsafe_allow_html=True)
    groups=[("COMMODITIES",COMMODITIES),("FX",FX),("RATES",RATES)]
    for group,mapping in groups:
        st.markdown(f"**{group}**")
        cols=st.columns(min(4,len(mapping)))
        for i,(t,n) in enumerate(list(mapping.items())[:4]):
            r=quote(t)
            with cols[i]:
                if r: st.markdown(f'<div class="heat"><div class="v">{n}</div><div class="s">{r["price"]:,.4f} • {r["chg"]:+.2f}%</div></div>',unsafe_allow_html=True)
                if st.button("OPEN",key=f"pulse_{group}_{i}",use_container_width=True):open_asset(t)

    st.markdown('<div class="section">🎯 TODAY\'S BEST CORE SETUPS <small>4/5+ from latest scan</small></div>',unsafe_allow_html=True)
    cs=st.session_state.get("core_scan",pd.DataFrame())
    if not cs.empty:
        hits=cs[cs.Score.astype(str).str.startswith(("4/5","5/5"))].copy();hits["_rank"]=hits.Score.map({"5/5":5,"4/5":4}).fillna(0);hits=hits.sort_values("_rank",ascending=False).head(6)
        if not hits.empty:setup_cards(hits)
        if st.button("🔥 OPEN FULL CORE SETUP",use_container_width=True,key="home_open_core"):st.session_state.page="VS FLOW SETUP";st.rerun()
    else:
        st.markdown('<div class="panel"><b>No Core scan loaded.</b><br>Run the Global Core scan once. The latest 4/5 and 5/5 candidates will appear here.</div>',unsafe_allow_html=True)
        if st.button("🚀 RUN GLOBAL CORE SETUP",use_container_width=True,key="home_run_core"):st.session_state.page="VS FLOW SETUP";st.rerun()

    st.markdown('<div class="section">⚡ QUICK ACTIONS</div>',unsafe_allow_html=True)
    qcols=st.columns(5);actions=[("🎯 SMART FINDER","SMART GLOBAL FINDER"),("🔥 CORE SETUP","VS FLOW SETUP"),("⚡ SMC 4H→5M","SMC 4H→5M SCALP"),("⛓️ OPTIONS","OPTIONS ANALYSIS"),("💀 HERO-ZERO","HERO-ZERO")]
    for box,(label,target) in zip(qcols,actions):
        if box.button(label,use_container_width=True,key="quick_"+target):st.session_state.page=target;st.rerun()
    st.markdown('<div class="note">Professional workflow: Global Regime → Cross-Asset Context → Smart Global Finder → 4H/1H/15M/5M Core Setup → Options/OI where available → manual chart confirmation → execution.</div>',unsafe_allow_html=True)

# =========================
# GLOBAL ASSETS
# =========================
elif page=="GLOBAL ASSETS":
    st.markdown('<div class="section">🌍 GLOBAL ASSET UNIVERSE <small>all major categories • searchable • clickable</small></div>',unsafe_allow_html=True)
    f1,f2=st.columns([2,1])
    with f1:q=st.text_input("Search asset / symbol",placeholder="BTC, NVIDIA, GOLD, EUR/USD...")
    with f2:group=st.selectbox("Category",["ALL"]+sorted({m["group"] for m in ASSET_META.values()}))
    rows=[]
    for t,m in ASSET_META.items():
        if group!="ALL" and m["group"]!=group:continue
        if q.strip().lower() not in (t+" "+m["name"]+" "+m["group"]).lower():continue
        rows.append(m)
    st.markdown(f'<div class="panel"><span class="pill green">{len(rows):,} MATCHES</span><span class="pill">LIVE DATA ON OPEN</span><span class="pill gold">GLOBAL ONLY</span></div>',unsafe_allow_html=True)
    for start in range(0,len(rows),12):
        cols=st.columns(4)
        for j,m in enumerate(rows[start:start+12]):
            with cols[j%4]:
                r=quote(m["symbol"]);txt=f'{r["price"]:,.4f} • {r["chg"]:+.2f}%' if r else "Data unavailable"
                st.markdown(f'<div class="card"><div class="label">{m["group"]}</div><div class="value" style="font-size:18px">{m["name"]}</div><div class="flat">{m["symbol"]}</div><div class="click-hint">{txt}</div></div>',unsafe_allow_html=True)
                if st.button("OPEN DETAIL",key=f"asset_open_{start}_{j}_{m['symbol']}",use_container_width=True):open_asset(m["symbol"])

# =========================
# SMART GLOBAL FINDER
# =========================
elif page=="SMART GLOBAL FINDER":
    st.markdown('<div class="section">🎯 SMART GLOBAL FINDER <small>rank global assets before opening charts</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="note">Transparent research score: trend + EMA200 + RSI + volume expansion + 52W location. This is a shortlist engine, not a guaranteed signal.</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:fg=st.selectbox("Category",["ALL"]+sorted({m["group"] for m in ASSET_META.values()}),key="fg_group")
    with c2:direction=st.selectbox("Direction",["BOTH","BULLISH","BEARISH"],key="fg_dir")
    with c3:min_score=st.slider("Minimum score",0,100,60,5,key="fg_score")
    q=st.text_input("Optional filter",placeholder="e.g. crypto, tech, gold",key="fg_q")
    base=[m for m in ASSET_META.values() if fg=="ALL" or m["group"]==fg]
    if q.strip():base=[m for m in base if q.lower() in (m["symbol"]+" "+m["name"]+" "+m["group"]).lower()]
    if st.button("🎯 FIND BEST GLOBAL ASSETS NOW",use_container_width=True,key="finder_run"):
        rows=[];bar=st.progress(0)
        for i,m in enumerate(base[:100]):
            snap=technical_snapshot(m["symbol"])
            if snap:
                score,reasons=selection_score(snap)
                if score>=min_score and (direction=="BOTH" or (direction=="BULLISH" and snap["trend"]=="BULLISH") or (direction=="BEARISH" and snap["trend"]=="BEARISH")):
                    rows.append({"Symbol":m["symbol"],"Name":m["name"],"Category":m["group"],"Price":snap["price"],"Change Context":snap["trend"],"RSI":round(snap["rsi"],1),"Volume x":round(snap["vol_ratio"],2),"Score":score,"Reasons":"; ".join(reasons)})
            bar.progress((i+1)/max(1,min(100,len(base))))
        bar.empty();st.session_state.finder_results=pd.DataFrame(rows).sort_values("Score",ascending=False) if rows else pd.DataFrame()
    out=st.session_state.get("finder_results",pd.DataFrame())
    if not out.empty:
        st.success(f"{len(out)} global assets matched.");st.dataframe(out,use_container_width=True,hide_index=True)
        opts=out.Symbol.tolist();pick=st.selectbox("Open candidate",opts,key="finder_pick")
        if st.button("⚡ OPEN CANDIDATE DETAIL",use_container_width=True,key="finder_open"):open_asset(pick)
    elif "finder_results" in st.session_state:st.info("No asset matched the current filters. Relax the score or direction filter.")

# =========================
# GLOBAL INDICES
# =========================
elif page=="GLOBAL INDICES":
    st.markdown('<div class="section">📊 GLOBAL INDICES <small>US • Europe • Asia-Pacific • volatility</small></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(t,n) in enumerate(GLOBAL_INDEXES.items()):
        r=quote(t)
        with cols[i%4]:
            if r:
                cls="up" if r["chg"]>0 else "down" if r["chg"]<0 else "flat";st.markdown(f'<div class="card"><div class="label">{n}</div><div class="value">{r["price"]:,.2f}</div><div class="{cls}">{r["chg"]:+.2f}%</div></div>',unsafe_allow_html=True)
            else:st.markdown(f'<div class="card"><div class="label">{n}</div><div class="value">—</div><div class="flat">Unavailable</div></div>',unsafe_allow_html=True)
            if st.button("OPEN",key=f"global_idx_{i}",use_container_width=True):open_asset(t)

# =========================
# CRYPTO MARKET
# =========================
elif page=="CRYPTO MARKET":
    st.markdown('<div class="section">₿ MAJOR CRYPTO MARKET <small>24/7 global • clickable • VS FLOW ready</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="note">Major crypto assets are displayed as a dedicated global-market board. Open any coin for price, chart, RSI/EMA/ATR, MTF structure, Core Setup, SMC scalp and Strategy Lab.</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(t,n) in enumerate(CRYPTO.items()):
        r=quote(t)
        with cols[i%4]:
            if r:
                cls="up" if r["chg"]>0 else "down" if r["chg"]<0 else "flat";st.markdown(f'<div class="card crypto-card"><div class="label">₿ {n}</div><div class="value">{r["price"]:,.6f}</div><div class="{cls}">{r["chg"]:+.2f}%</div></div>',unsafe_allow_html=True)
            else:st.markdown(f'<div class="card crypto-card"><div class="label">₿ {n}</div><div class="value">—</div><div class="flat">Unavailable</div></div>',unsafe_allow_html=True)
            if st.button("OPEN DETAIL",key=f"crypto_page_{i}",use_container_width=True):open_asset(t)

# =========================
# ASSET DETAIL
# =========================
elif page=="ASSET DETAIL":
    sym=st.session_state.get("selected","BTC-USD");meta=ASSET_META.get(sym,{"symbol":sym,"name":sym,"group":"CUSTOM","region":"Global"})
    st.markdown(f'<div class="section">📌 {meta["name"]} <small>{sym} • {meta["group"]} • {meta["region"]}</small></div>',unsafe_allow_html=True)
    if st.button("← BACK TO GLOBAL ASSETS",key="back_assets"):st.session_state.page="GLOBAL ASSETS";st.rerun()
    q=quote(sym);snap=technical_snapshot(sym)
    if q:
        m=st.columns(5);vals=[("PRICE",q["price"]),("DAY %",f'{q["chg"]:+.2f}%'),("CATEGORY",meta["group"]),("REGION",meta["region"]),("DATA", "LIVE/CACHED")]
        for col,(k,v) in zip(m,vals):col.markdown(f'<div class="metric"><div class="k">{k}</div><div class="v" style="font-size:16px">{v}</div></div>',unsafe_allow_html=True)
    d=history(sym,"1y","1d")
    if not d.empty:
        st.markdown('<div class="section">📈 PRICE CHART <small>1Y daily</small></div>',unsafe_allow_html=True);st.line_chart(d["Close"],height=360,use_container_width=True)
    if snap:
        score,reasons=selection_score(snap);cls="green" if snap["trend"]=="BULLISH" else "red" if snap["trend"]=="BEARISH" else "gold";st.markdown(f'<div class="panel"><span class="pill {cls}">TREND: {snap["trend"]}</span><span class="pill">Research Score {score}/100</span><br><br><b>EMA20:</b> {snap["ema20"]:,.6f} &nbsp; <b>EMA50:</b> {snap["ema50"]:,.6f} &nbsp; <b>EMA200:</b> {snap["ema200"]:,.6f} &nbsp; <b>RSI:</b> {snap["rsi"]:.2f} &nbsp; <b>ATR:</b> {snap["atr"]:.6f}<br><br><b>52W High:</b> {snap["high52"]:,.6f} &nbsp; <b>52W Low:</b> {snap["low52"]:,.6f} &nbsp; <b>Volume x20D:</b> {snap["vol_ratio"]:.2f}</div>',unsafe_allow_html=True)
        st.markdown("**Selection factors**");[st.write("✅ "+x) for x in reasons]
    st.markdown('<div class="section">🔥 VS FLOW MULTI-TIMEFRAME</div>',unsafe_allow_html=True)
    if st.button("RUN 4H → 1H → 15M → 5M",use_container_width=True,key="asset_mtf"):
        st.session_state.asset_mtf=mtf_setup(sym)
    if "asset_mtf" in st.session_state:
        frames,overall=st.session_state.asset_mtf;cls="green" if overall=="BUY" else "red" if overall=="SELL" else "gold";st.markdown(f'<div class="panel"><span class="pill {cls}">OVERALL: {overall}</span></div>',unsafe_allow_html=True);st.dataframe(pd.DataFrame(frames),use_container_width=True,hide_index=True)
    st.markdown('<div class="section">🎯 ONE-CLICK DESKS</div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    if a.button("🔥 CORE SETUP",use_container_width=True):st.session_state.page="VS FLOW SETUP";st.rerun()
    if b.button("⚡ SMC 4H→5M",use_container_width=True):st.session_state.page="SMC 4H→5M SCALP";st.rerun()
    if c.button("🧠 STRATEGY LAB",use_container_width=True):st.session_state.page="STRATEGY LAB";st.rerun()
    if d.button("📐 CLASSIC",use_container_width=True):st.session_state.page="CLASSIC PRICE ACTION";st.rerun()
    st.markdown('<div class="note">This asset page is the central clickable information hub. It keeps the V55 analysis architecture while the universe remains global-only.</div>',unsafe_allow_html=True)

# =========================
# STRATEGY / SMC / CLASSIC
# =========================
elif page=="STRATEGY LAB":
    st.markdown('<div class="section">🧠 STRATEGY LAB <small>five complementary global-market lenses</small></div>',unsafe_allow_html=True)
    opts=ALL_TICKERS;default=st.session_state.get("selected","BTC-USD");sym=st.selectbox("Global asset",opts,index=opts.index(default) if default in opts else 0,format_func=lambda x:f'{x} — {ASSET_META[x]["name"]}',key="strategy_asset")
    if st.button("🧠 ANALYSE 5 STRATEGIES",use_container_width=True,key="strategy_run"):
        sdf,summary=strategy_suite(sym);st.session_state.strategy_result=(sym,sdf,summary)
    if "strategy_result" in st.session_state:
        sym,sdf,summary=st.session_state.strategy_result
        if not sdf.empty:
            cls="green" if summary["overall"]=="BUY" else "red" if summary["overall"]=="SELL" else "gold";st.markdown(f'<div class="panel"><span class="pill {cls}">COMBINED BIAS: {summary["overall"]}</span><span class="pill">Confidence {summary["confidence"]}%</span><span class="pill green">BUY {summary["buy"]}</span><span class="pill red">SELL {summary["sell"]}</span></div>',unsafe_allow_html=True);st.dataframe(sdf,use_container_width=True,hide_index=True)
            st.markdown('<div class="panel"><b>Hierarchy:</b> SMC → Price Action → Breakout/Retest + Fibonacci → Momentum filter. Prefer confluence; if signals conflict, WAIT.</div>',unsafe_allow_html=True)

elif page=="SMC 4H→5M SCALP":
    st.markdown('<div class="section">⚡ SMC 4H→5M SCALP <small>global asset execution model</small></div>',unsafe_allow_html=True)
    opts=ALL_TICKERS;default=st.session_state.get("selected","BTC-USD");sym=st.selectbox("Global asset",opts,index=opts.index(default) if default in opts else 0,format_func=lambda x:f'{x} — {ASSET_META[x]["name"]}',key="smc_asset")
    if st.button("⚡ ANALYSE SMC 4H→5M",use_container_width=True,key="smc_run"):st.session_state.smc_result=smc_scalp_analyze(sym,ASSET_META[sym]["name"])
    r=st.session_state.get("smc_result")
    if r:
        side="BUY" if "BUY" in r["Signal"] else "SELL" if "SELL" in r["Signal"] else "WAIT";color="green" if side=="BUY" else "red" if side=="SELL" else "gold";st.markdown(f'<div class="panel"><span class="pill {color}">{r["Signal"]}</span><span class="pill">Score {r["Score"]}</span><br><br><b>{r["Symbol"]}</b> • {r["Name"]}<br><br><b>Entry:</b> {r["Entry"] or "—"} &nbsp; <b>SL:</b> {r["SL"] or "—"} &nbsp; <b>TP:</b> {r["TP"] or "—"} &nbsp; <b>RR:</b> {r["RR"] or "—"}</div>',unsafe_allow_html=True);st.dataframe(pd.DataFrame([{k:r.get(k,"") for k in ["4H Direction","4H Zone","5M Sweep","5M MSS","5M FVG","FVG Retest","Score","Signal","Entry","SL","TP","RR"]}]),use_container_width=True,hide_index=True)

elif page=="CLASSIC PRICE ACTION":
    st.markdown('<div class="section">📐 CLASSIC PRICE ACTION DESK <small>global key levels • trend • breakout • candle close</small></div>',unsafe_allow_html=True)
    opts=ALL_TICKERS;default=st.session_state.get("selected","BTC-USD");sym=st.selectbox("Global asset",opts,index=opts.index(default) if default in opts else 0,format_func=lambda x:f'{x} — {ASSET_META[x]["name"]}',key="classic_asset")
    if st.button("📐 ANALYSE CLASSIC SETUP",use_container_width=True):st.session_state.classic_result=classic_analyze(sym,ASSET_META[sym]["name"])
    r=st.session_state.get("classic_result")
    if r:
        side="BUY" if r["Signal"]=="BUY" else "SELL" if r["Signal"]=="SELL" else "WAIT";color="green" if side=="BUY" else "red" if side=="SELL" else "gold";st.markdown(f'<div class="panel"><span class="pill {color}">{r["Signal"]}</span><span class="pill">Score {r["Score"]}</span><br><br><b>{r["Symbol"]}</b> • {r["Name"]}<br><br><b>Entry:</b> {r["Entry"] or "—"} &nbsp; <b>SL:</b> {r["SL"] or "—"} &nbsp; <b>TP:</b> {r["TP"] or "—"} &nbsp; <b>RR:</b> {r["RR"] or "—"}</div>',unsafe_allow_html=True);st.dataframe(pd.DataFrame([{k:r.get(k,"") for k in ["Key Level","Trendline","Breakout/Breakdown","Price Action","Candle Close","Score","Signal","Entry","SL","TP","RR"]}]),use_container_width=True,hide_index=True)

# =========================
# GLOBAL CORE SETUP
# =========================
elif page=="VS FLOW SETUP":
    st.markdown('<div class="section">🔥 VS FLOW CORE SETUP <small>strict 4H → 1H → 15M → 5M • 4/5 actionable • 5/5 A+</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="note">4H Order Block → 1H Liquidity Sweep/BOS → 15M FVG → 5M Trigger. The 5th point is liquidity alignment for A+.</div>',unsafe_allow_html=True)
    mode=st.radio("Universe",["My symbols","Top 100 Global","Crypto only"],horizontal=True,key="core_mode")
    if mode=="My symbols":
        raw=st.text_area("Symbols (one per line / comma separated)","BTC-USD\nETH-USD\nNVDA\nAAPL\nGC=F")
        syms=[x for x in re.split(r"[\n,; ]+",raw.upper()) if x]
        syms=[x for x in syms if x in ASSET_META]
    elif mode=="Crypto only":syms=list(CRYPTO)
    else:syms=ALL_TICKERS[:100]
    limit=st.slider("Core scan limit",5,min(100,max(10,len(syms))),min(25,len(syms)),key="core_limit")
    if st.button("🚀 SCAN GLOBAL MARKET NOW",use_container_width=True,key="core_scan_run"):
        rows=[];bar=st.progress(0);chosen=syms[:limit]
        for i,sym in enumerate(chosen):
            rows.append(core_analyze(sym,ASSET_META[sym]["name"]));bar.progress((i+1)/max(1,len(chosen)))
        bar.empty();st.session_state.core_scan=pd.DataFrame(rows)
    df=st.session_state.get("core_scan",pd.DataFrame())
    if not df.empty:
        hits=df[df.Score.astype(str).str.startswith(("4/5","5/5"))].copy();a5=int((hits.Score=="5/5").sum());st.success(f"Scan complete • {len(df)} assets • {len(hits)} setup(s) • {a5} A+ result(s)")
        if not hits.empty:
            st.dataframe(hits[["Symbol","Name","4H OB","1H Sweep","1H BOS","15M FVG","5M Trigger","Score","Signal","Entry","SL","TP","RR","Chart Tally"]],use_container_width=True,hide_index=True);setup_cards(hits.head(6))
            picks=hits.Symbol.tolist();pick=st.selectbox("Open setup asset",picks,key="core_pick")
            if st.button("OPEN ASSET DETAIL",use_container_width=True,key="core_open_asset"):open_asset(pick)
        else:st.warning("No 4/5+ Core Setup in the latest global scan.")
        with st.expander("Show all scanned assets"):st.dataframe(df,use_container_width=True,hide_index=True)

# =========================
# GLOBAL OPTIONS + HERO ZERO
# =========================
elif page=="AMD + iFVG SCANNER":
    st.markdown('<div class="section">🧠 AMD + iFVG SCANNER <small>Global Stocks • Indices • FX • Commodities • Crypto</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="note"><b>Sequence:</b> HTF Bias → AMD Accumulation/Manipulation → Liquidity Sweep → MSS/BOS → Displacement → iFVG → Retest. This is an additive research scanner; existing V55 Core/SMC logic remains unchanged.</div>',unsafe_allow_html=True)
    groups=["ALL"]+sorted({m["group"] for m in ASSET_META.values()})
    c1,c2,c3=st.columns(3)
    with c1: group=st.selectbox("Universe",groups,key="amd_ifvg_group")
    with c2: limit=st.slider("Scan limit",5,min(150,max(10,len(ALL_TICKERS))),min(50,len(ALL_TICKERS)),key="amd_ifvg_limit")
    with c3: side_filter=st.selectbox("Signal filter",["ALL","BUY","SELL","WATCH"],key="amd_ifvg_filter")
    if group=="ALL": selected=ALL_TICKERS[:limit]
    else: selected=[t for t in ALL_TICKERS if ASSET_META.get(t,{}).get("group")==group][:limit]
    if st.button("🚀 RUN AMD + iFVG GLOBAL SCAN",type="primary",use_container_width=True,key="amd_ifvg_run"):
        rows=[]; bar=st.progress(0,text="Starting AMD + iFVG scan...")
        for i,t in enumerate(selected,1):
            rows.append(amd_ifvg_analyze_global(t,ASSET_META.get(t,{}).get("name",t)))
            bar.progress(i/len(selected),text=f"Scanning {i}/{len(selected)} • {t}")
        bar.empty(); st.session_state.amd_ifvg_scan=pd.DataFrame(rows)
    df=st.session_state.get("amd_ifvg_scan",pd.DataFrame())
    if not df.empty:
        view=df.copy()
        if side_filter=="BUY": view=view[view["Signal"].astype(str).str.contains("BUY",na=False)]
        elif side_filter=="SELL": view=view[view["Signal"].astype(str).str.contains("SELL",na=False)]
        elif side_filter=="WATCH": view=view[view["Signal"].astype(str).str.startswith("WATCH",na=False)]
        st.success(f"Showing {len(view)} AMD + iFVG candidate(s).")
        st.dataframe(view,use_container_width=True,hide_index=True)
        st.download_button("⬇️ DOWNLOAD AMD + iFVG CSV",view.to_csv(index=False).encode(),file_name="VS_FLOW_GLOBAL_AMD_iFVG.csv",mime="text/csv",use_container_width=True)
        st.markdown('<div class="note"><b>Interpretation:</b> 4/5+ = strong chart-review candidate. It is not an automatic trade signal. Manually confirm 1M, 1W, 1D, 4H, 1H, 15M and 5M before execution.</div>',unsafe_allow_html=True)
    else:
        st.info("Select a universe and click RUN AMD + iFVG GLOBAL SCAN.")

elif page=="OPTIONS ANALYSIS":
    st.markdown('<div class="section">⛓️ GLOBAL OPTIONS ANALYSIS <small>OI • PCR • Max Pain • Call/Put decision</small></div>',unsafe_allow_html=True)
    optionable=[x for x in ["AAPL","MSFT","NVDA","AMZN","META","TSLA","SPY","QQQ","IWM","GLD","SLV","USO"]]
    sym=st.selectbox("Underlying",optionable,index=optionable.index(st.session_state.get("selected")) if st.session_state.get("selected") in optionable else 0,key="oc_symbol")
    exps=option_expiries(sym);expiry=st.selectbox("Expiry",exps,key="oc_exp") if exps else None
    if st.button("⚡ FETCH GLOBAL OPTION CHAIN",use_container_width=True,key="oc_fetch") and expiry:
        df=option_chain(sym,expiry);st.session_state.oc=(df,quote(sym)["price"] if quote(sym) else None)
    if "oc" in st.session_state:
        df,spot=st.session_state.oc
        if not df.empty:
            ana=option_analysis(df,spot);plan=trade_plan(df,ana);m=st.columns(6)
            for col,(k,v) in zip(m,[("SPOT",ana["spot"]),("ATM",ana["atm"]),("PCR",f'{ana["pcr"]:.2f}'),("CALL OI",f'{ana["call_oi"]:,.0f}'),("PUT OI",f'{ana["put_oi"]:,.0f}'),("BIAS",ana["bias"])]):col.markdown(f'<div class="metric"><div class="k">{k}</div><div class="v">{v}</div></div>',unsafe_allow_html=True)
            st.dataframe(df,use_container_width=True,hide_index=True)
            if plan.get("side")!="WAIT":st.markdown(f'<div class="panel"><span class="pill {"green" if plan["side"]=="CALL" else "red"}">{plan["side"]} • {plan["option"]}</span><span class="pill">Confidence {ana["confidence"]}%</span><br><br><b>Entry:</b> {plan["entry"]:.4f} &nbsp; <b>SL:</b> {plan["sl"]:.4f} &nbsp; <b>TP1:</b> {plan["tp1"]:.4f} &nbsp; <b>TP2:</b> {plan["tp2"]:.4f}<br><br>Max Pain: {ana["max_pain"]:,.2f} • Call Wall: {ana["call_wall"]:,.2f} • Put Wall: {ana["put_wall"]:,.2f}</div>',unsafe_allow_html=True)
        else:st.warning("Option chain unavailable for this symbol/expiry.")
    st.markdown('<div class="note">Global options availability depends on Yahoo Finance coverage. Option-chain outputs are research aids; verify contract specifications, liquidity, spreads and expiry before any execution.</div>',unsafe_allow_html=True)

elif page=="HERO-ZERO":
    st.markdown('<div class="section">💀 HERO-ZERO GLOBAL OPTIONS DESK <small>separate high-risk OTM scanner</small></div>',unsafe_allow_html=True)
    optionable=["AAPL","MSFT","NVDA","AMZN","META","TSLA","SPY","QQQ","IWM","GLD","SLV","USO"]
    sym=st.selectbox("Underlying",optionable,key="hz_symbol_global");exps=option_expiries(sym);expiry=st.selectbox("Expiry",exps,key="hz_exp_global") if exps else None
    if st.button("💀 SCAN HERO-ZERO",use_container_width=True,key="hz_fetch_global") and expiry:
        df=option_chain(sym,expiry);q=quote(sym);spot=q["price"] if q else None;ana=option_analysis(df,spot);st.session_state.hz=(df,ana)
    if "hz" in st.session_state:
        df,ana=st.session_state.hz
        if not df.empty and ana:
            cand=hero_zero_candidates(df,ana);m=st.columns(5)
            for col,(k,v) in zip(m,[("SPOT",ana["spot"]),("ATM",ana["atm"]),("PCR",f'{ana["pcr"]:.2f}'),("BIAS",ana["bias"]),("CONF",f'{ana["confidence"]}%')]):col.markdown(f'<div class="metric"><div class="k">{k}</div><div class="v">{v}</div></div>',unsafe_allow_html=True)
            if not cand.empty:st.dataframe(cand,use_container_width=True,hide_index=True)
            else:st.warning("No Hero-Zero candidate passed the filters.")
    st.markdown('<div class="note"><b>Risk:</b> Hero-Zero options can lose most/all premium rapidly due to theta, IV and gamma. Low premium is not low risk. Confirm the underlying Core/SMC setup first.</div>',unsafe_allow_html=True)

elif page=="RISK CALCULATOR":
    st.markdown('<div class="section">🧮 GLOBAL RISK CALCULATOR <small>position sizing • defined risk • RR planning</small></div>',unsafe_allow_html=True)
    st.markdown('<div class="note">Use the same execution discipline across crypto, equities, FX and commodities: define account risk first, then derive position size from entry and stop distance.</div>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1:account=st.number_input("Account size",min_value=0.0,value=10000.0,step=100.0,key="risk_account")
    with c2:risk_pct=st.number_input("Risk %",min_value=0.1,max_value=10.0,value=1.0,step=0.1,key="risk_pct")
    with c3:entry=st.number_input("Entry",min_value=0.0,value=100.0,step=0.1,key="risk_entry")
    with c4:stop=st.number_input("Stop",min_value=0.0,value=98.0,step=0.1,key="risk_stop")
    c5,c6=st.columns(2)
    with c5:target=st.number_input("Target",min_value=0.0,value=104.0,step=0.1,key="risk_target")
    with c6:contract=st.number_input("Units per contract",min_value=0.000001,value=1.0,step=1.0,key="risk_contract")
    if entry>0 and stop>=0:
        risk_cash=account*risk_pct/100;stop_dist=abs(entry-stop);units=risk_cash/stop_dist if stop_dist>0 else 0;contracts=units/contract if contract>0 else 0;reward=abs(target-entry);rr=reward/stop_dist if stop_dist>0 else 0
        m=st.columns(5)
        vals=[("MAX LOSS",risk_cash),("STOP DIST",stop_dist),("UNITS",units),("CONTRACTS",contracts),("RR",f"1:{rr:.2f}")]
        for col,(k,v) in zip(m,vals):col.markdown(f'<div class="metric"><div class="k">{k}</div><div class="v">{v:,.4f}</div></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="panel"><b>Risk rule:</b> risk {risk_pct:.2f}% = {risk_cash:,.2f} account currency. At entry {entry:,.4f} and stop {stop:,.4f}, theoretical size = {units:,.4f} units. For derivatives, verify contract multiplier, tick value, margin and liquidity before execution.</div>',unsafe_allow_html=True)

st.markdown('<div style="margin-top:30px;border-top:1px solid #14384f;padding-top:12px;color:#668096;font-size:10px">VS FLOW GLOBAL V55 • Global Indices + Global Equities + FX + Commodities + Rates + Major Crypto + Core + SMC 4H→5M + Classic + Options + Hero-Zero + Strategy Lab • Built for vaibhav shirsat • Educational / research use only</div>',unsafe_allow_html=True)
