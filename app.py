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
