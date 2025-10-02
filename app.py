import streamlit as st

st.set_page_config(page_title="فلتر الأسهم الأمريكية", layout="centered")

st.title("📊 فلتر الأسهم الأمريكية")
st.markdown("مرحباً عبدالله 👋، هذا النموذج يتيح لك فلترة الأسهم بناءً على مؤشرات فنية وفلترة شرعية.")

# اختيار القطاع
sector = st.selectbox("اختر القطاع", ["الطاقة", "الصحة", "التقنية", "المالية", "الاستهلاك", "الصناعة"])

# اختيار الفاصل الزمني
timeframe = st.selectbox("اختر الفاصل الزمني", ["يومي", "أسبوعي", "شهري"])

# نطاق السعر
price_range = st.slider("نطاق السعر", 0, 1000, (50, 300))

# مؤشرات فنية
st.subheader("المؤشرات الفنية")
rsi = st.checkbox("RSI (مؤشر القوة النسبية)")
macd = st.checkbox("MACD (تقارب وتباعد المتوسطات)")
sma = st.checkbox("SMA (المتوسط المتحرك البسيط)")
ema = st.checkbox("EMA (المتوسط المتحرك الأسي)")
bollinger = st.checkbox("Bollinger Bands (الانحراف المعياري)")

# فلترة شرعية
st.subheader("الفلترة الشرعية")
sharia_filter = st.checkbox("تفعيل الفلترة الشرعية")
if sharia_filter:
    st.write("✅ سيتم استبعاد الشركات ذات الأنشطة الربوية أو نسب ديون مرتفعة.")

# زر تنفيذ الفلترة
if st.button("تنفيذ الفلترة"):
    st.success("تم تطبيق الفلاتر بنجاح ✅")
    st.write(f"القطاع المختار: {sector}")
    st.write(f"الفاصل الزمني: {timeframe}")
    st.write(f"نطاق السعر: من {price_range[0]} إلى {price_range[1]}")
    st.write("المؤشرات الفنية المفعّلة:")
    indicators = []
    if rsi: indicators.append("RSI")
    if macd: indicators.append("MACD")
    if sma: indicators.append("SMA")
    if ema: indicators.append("EMA")
    if bollinger: indicators.append("Bollinger Bands")
    st.write(indicators if indicators else "لا توجد مؤشرات مفعّلة")
    if sharia_filter:
        st.write("✅ الفلترة الشرعية مفعّلة")

# ملاحظة ختامية
st.markdown("---")
st.caption("تمهيد لتكامل البيانات الحية من API وربط مباشر بالأسواق المالية.")
