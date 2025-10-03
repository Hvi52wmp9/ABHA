import streamlit as st
import pandas as pd
import requests

API_KEY = "d3eqb5pr01qh40ffhst0d3eqb5pr01qh40ffhstg"

symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "UNH"]
sharia_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # مثال فقط

def fetch_data(symbol):
    base_url = "https://finnhub.io/api/v1"
    headers = {"X-Finnhub-Token": API_KEY}

    try:
        quote = requests.get(f"{base_url}/quote?symbol={symbol}", headers=headers).json()
        rsi = requests.get(f"{base_url}/indicator?symbol={symbol}&resolution=D&indicator=rsi&timeperiod=14", headers=headers).json()
        macd = requests.get(f"{base_url}/indicator?symbol={symbol}&resolution=D&indicator=macd&fastperiod=12&slowperiod=26&signalperiod=9", headers=headers).json()

        latest_rsi = rsi.get("rsi", {}).get("values", [-1])[-1]
        latest_macd = macd.get("macd", {}).get("values", [-1])[-1]

        return {
            "الرمز": symbol,
            "السعر": quote.get("c"),
            "RSI": latest_rsi,
            "MACD": latest_macd
        }
    except:
        return {"الرمز": symbol, "السعر": None, "RSI": None, "MACD": None}

st.title("📊 فلترة الأسهم حسب المؤشرات الفنية والشرعية")

min_price, max_price = st.sidebar.slider("نطاق السعر", 0, 2000, (0, 2000))
rsi_min, rsi_max = st.sidebar.slider("نطاق RSI", 0, 100, (0, 100))
macd_enabled = st.sidebar.checkbox("MACD موجب فقط")
sharia_enabled = st.sidebar.checkbox("فلترة شرعية")

if st.sidebar.button("تنفيذ الفلترة"):
    st.info("📡 جاري جلب البيانات من السوق الحقيقي...")
    results = []
    for symbol in symbols:
        if sharia_enabled and symbol not in sharia_symbols:
            continue
        data = fetch_data(symbol)

        # 👇 طباعة بيانات كل سهم لفحص القيم
        st.write(f"🔍 {symbol} → السعر: {data['السعر']}, RSI: {data['RSI']}, MACD: {data['MACD']}")

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
