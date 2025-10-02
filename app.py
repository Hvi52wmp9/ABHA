import streamlit as st

st.set_page_config(page_title="فلتر الأسهم السعودية", layout="centered")

st.title("📊 فلترة الأسهم السعودية")
st.markdown("مرحباً بك في منصة الفلترة الفنية والشرعية للأسهم السعودية.")

# --- الفلترة الأساسية ---
st.sidebar.header("الفلترة الأساسية")

sector = st.sidebar.selectbox("اختر القطاع", [
    "الكل", "الطاقة", "المواد الأساسية", "السلع الرأسمالية",
    "الخدمات التجارية والمهنية", "النقل", "الإعلام والترفيه",
    "السلع طويلة الأجل", "الخدمات الإستهلاكية", "تجزئة السلع الكمالية",
    "تجزئة الأغذية", "البنوك", "التأمين", "الرعاية الصحية", "التقنية"
])

price_range = st.sidebar.slider("نطاق السعر (ريال)", 0, 1000, (50, 300))

# --- المؤشرات الفنية ---
st.sidebar.header("المؤشرات الفنية")

rsi_enabled = st.sidebar.checkbox("RSI (مؤشر القوة النسبية)")
macd_enabled = st.sidebar.checkbox("MACD (تقارب وتباعد المتوسطات)")
sma_enabled = st.sidebar.checkbox("SMA (المتوسط المتحرك البسيط)")
ema_enabled = st.sidebar.checkbox("EMA (المتوسط المتحرك الأسي)")
bb_enabled = st.sidebar.checkbox("Bollinger Bands (الانحراف المعياري)")

# --- الفلترة الشرعية ---
st.sidebar.header("الفلترة الشرعية")
sharia_filter = st.sidebar.checkbox("تفعيل الفلترة الشرعية")

if sharia_filter:
    st.sidebar.info("✅ سيتم استبعاد الشركات ذات الأنشطة الربوية أو نسب ديون مرتفعة.")

# --- زر تنفيذ الفلترة ---
if st.sidebar.button("تنفيذ الفلترة"):
    st.success("✅ تم تطبيق الفلاتر بنجاح")
    st.write("### تفاصيل الفلترة:")
    st.write(f"🔹 القطاع المختار: `{sector}`")
    st.write(f"🔹 نطاق السعر: من `{price_range[0]}` إلى `{price_range[1]}` ريال")
    
    st.write("🔹 المؤشرات الفنية المفعّلة:")
    indicators = []
    if rsi_enabled: indicators.append("RSI")
    if macd_enabled: indicators.append("MACD")
    if sma_enabled: indicators.append("SMA")
    if ema_enabled: indicators.append("EMA")
    if bb_enabled: indicators.append("Bollinger Bands")
    st.write(indicators if indicators else "لا توجد مؤشرات مفعّلة")

    if sharia_filter:
        st.write("🔹 الفلترة الشرعية: مفعّلة ✅")

# --- ملاحظة ختامية ---
st.markdown("---")
st.caption("📌 هذه نسخة أولية قابلة للتوسيع مستقبلاً لربط مباشر ببيانات السوق عبر API.")
