import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="فلترة الأسهم الأمريكية", layout="centered")
st.title("📊 فلترة 50 سهم من السوق الأمريكي")

# --- مفتاح API الخاص بك ---
API_KEY = "d3eqb5pr01qh40ffhst0d3eqb5pr01qh40ffhstg" Finnhub

# --- قائمة رموز مختارة (50 رمز) ---
symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "MA",
    "UNH", "HD", "PG", "DIS", "BAC", "KO", "PEP", "ADBE", "NFLX", "INTC",
    "CSCO", "CRM", "T", "XOM", "CVX", "WMT", "MRK", "PFE", "ABBV", "NKE",
    "ORCL", "QCOM", "TXN", "AVGO", "AMD", "HON", "COST", "MCD", "UPS", "BA",
    "IBM", "GE", "AMAT", "LMT", "CAT", "GS", "BLK", "BK", "AXP", "FDX"
]

# --- إعدادات الفلترة ---
# --- إعدادات الفلترة ---
st.sidebar.header("الفلترة")
min_price, max_price = st.sidebar.slider("نطاق السعر (دولار)", 0, 2000, (50, 300))
rsi_min, rsi_max = st.sidebar.slider("نطاق RSI", 0, 100, (30, 70))
macd_enabled = st.sidebar.checkbox("فلترة MACD موجب فقط")
sharia_enabled = st.sidebar.checkbox("فلترة شرعية (حسب الرموز الشرعية)")

# --- قائمة رموز شرعية (مثال مبدئي) ---
sharia_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # ← حدثها لاحقًا حسب قائمتك

# --- تنفيذ الفلترة ---
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


# --- دالة لجلب البيانات ---
def fetch_data(symbol):
    try:
        quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()
        price = quote["c"]

        rsi_data = requests.get(f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=rsi&timeperiod=14&token={API_KEY}").json()
        rsi = rsi_data["rsi"][-1] if "rsi" in rsi_data else None

        macd_data = requests.get(f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=macd&token={API_KEY}").json()
        macd = macd_data["macd"][-1] if "macd" in macd_data else None

        return {"الرمز": symbol, "السعر": price, "RSI": rsi, "MACD": macd}
    except:
        return {"الرمز": symbol, "السعر": None, "RSI": None, "MACD": None}

# --- تنفيذ الفلترة ---
if st.sidebar.button("تنفيذ الفلترة"):
    st.info("📡 جاري جلب البيانات من السوق الحقيقي...")
    results = []
    for symbol in symbols:
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

# --- ملاحظة ختامية ---
st.markdown("---")
st.caption("📌 البيانات لحظية من Finnhub. قد تظهر بعض الرموز بدون بيانات بسبب قيود API أو السوق.")
