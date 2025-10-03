import streamlit as st
import requests
import pandas as pd

API_KEY = "d3eqb5pr01qh40ffhst0d3eqb5pr01qh40ffhstg"

symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK.B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "DIS", "BAC", "XOM", "KO", "PFE",
    "PEP", "CVX", "ABBV", "TMO", "AVGO", "ACN", "MCD", "COST", "WMT", "ADBE",
    "CSCO", "NFLX", "INTC", "CRM", "TXN", "AMD", "QCOM", "HON", "LIN", "NEE",
    "LOW", "AMAT", "SBUX", "ISRG", "MDT", "INTU", "BKNG", "BLK", "SPGI", "ZTS"
]

sharia_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "PEP", "COST", "WMT", "ADBE"]

def fetch_data(symbol):
    try:
        quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()
        rsi_data = requests.get(f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=rsi&token={API_KEY}").json()
        macd_data = requests.get(f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=macd&token={API_KEY}").json()

        price = quote.get("c")
        rsi = rsi_data.get("rsi")[-1] if rsi_data.get("rsi") else None
        macd = macd_data.get("macd")[-1] if macd_data.get("macd") else None

        return {
            "الرمز": symbol,
            "السعر": price,
            "RSI": round(rsi, 2) if rsi else None,
            "MACD": round(macd, 2) if macd else None
        }
    except:
        return {"الرمز": symbol, "السعر": None, "RSI": None, "MACD": None}

st.set_page_config(page_title="فلترة الأسهم", layout="wide")
st.title("📊 فلترة الأسهم الأمريكية حسب المؤشرات الفنية")

st.sidebar.header("إعدادات الفلترة")
min_price, max_price = st.sidebar.slider("نطاق السعر (دولار)", 0, 2000, (50, 300))
rsi_min, rsi_max = st.sidebar.slider("نطاق RSI", 0, 100, (30, 70))
macd_enabled = st.sidebar.checkbox("فلترة MACD موجب فقط")
sharia_enabled = st.sidebar.checkbox("فلترة شرعية (حسب الرموز الشرعية)")

if st.sidebar.button("تنفيذ الفلترة"):
    st.info("📡 جاري جلب البيانات من السوق الحقيقي...")
    results = []
    for symbol in symbols:
        if sharia_enabled and symbol not in sharia_symbols:
            continue
        data = fetch_data(symbol)
        if data["السعر"] is None or data["RSI"] is None:
            continue
        if not (min_price <= data["السعر"] <= max_price):
            continue
        if not (rsi_min <= data["RSI"] <= rsi_max):
            continue
        if macd_enabled and (data["MACD"] is None or data["MACD"] < 0):
            continue
        results.append(data)

    df = pd.DataFrame(results)
    st.success(f"✅ تم عرض {len(df)} سهم اجتاز الفلترة")
    st.dataframe(df)
