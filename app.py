import streamlit as st
import requests
import pandas as pd

API_KEY = "ضع مفتاحك هنا"  # ← الصق مفتاحك هنا
symbol = "AAPL"

# --- جلب السعر الحالي ---
quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
quote_response = requests.get(quote_url).json()
price = quote_response["c"]

# --- جلب RSI ---
rsi_url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=rsi&timeperiod=14&token={API_KEY}"
rsi_response = requests.get(rsi_url).json()
rsi = rsi_response["rsi"][-1] if "rsi" in rsi_response else "غير متوفر"

# --- جلب MACD ---
macd_url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=macd&token={API_KEY}"
macd_response = requests.get(macd_url).json()
macd = macd_response["macd"][-1] if "macd" in macd_response else "غير متوفر"

# --- عرض النتائج ---
st.title("📈 بيانات سهم AAPL من السوق الحقيقي")
df = pd.DataFrame([{
    "الرمز": symbol,
    "السعر": price,
    "RSI": rsi,
    "MACD": macd
}])
st.dataframe(df)
