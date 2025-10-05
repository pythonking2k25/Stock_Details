import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Info App", page_icon="📈", layout="centered")

st.title("📊 Stock Information Dashboard")
st.markdown("Get live stock details from Yahoo Finance")

# --------------------------------------------
# Step 1: Input
# --------------------------------------------
stock_input = st.text_input("Enter Stock Symbol (e.g., INFY.NS, RELIANCE.NS, TCS.NS):", "INFY.NS")

if st.button("🔍 Fetch Stock Details"):
    try:
        # --------------------------------------------
        # Step 2: Fetch Stock Data
        # --------------------------------------------
        stock = yf.Ticker(stock_input)
        info = stock.info

        # Handle deprecated keys safely
        def safe_get(key):
            return info[key] if key in info else "N/A"

        hist = stock.history(period="1y")

        if hist.empty:
            st.warning("⚠️ No historical data found. Check the stock symbol.")
        else:
            # --------------------------------------------
            # Step 3: Extract Details
            # --------------------------------------------
            current_price = hist["Close"].iloc[-1]
            pe_ratio = safe_get("trailingPE")
            market_cap = safe_get("marketCap")
            high_52w = hist["High"].max()
            low_52w = hist["Low"].min()
            dividend_yield = safe_get("dividendYield")
            one_year_return = round(((current_price - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100, 2)

            # --------------------------------------------
            # Step 4: Display Results
            # --------------------------------------------
            st.subheader(f"📈 {stock_input} — Key Financial Metrics")
            df = pd.DataFrame({
                "Metric": [
                    "Current Price (₹)",
                    "Market Cap (₹)",
                    "P/E Ratio",
                    "52-Week High (₹)",
                    "52-Week Low (₹)",
                    "Dividend Yield (%)",
                    "1-Year Return (%)"
                ],
                "Value": [
                    round(current_price, 2),
                    f"{market_cap:,}" if market_cap != "N/A" else "N/A",
                    round(pe_ratio, 2) if pe_ratio != "N/A" else "N/A",
                    round(high_52w, 2),
                    round(low_52w, 2),
                    round(dividend_yield * 100, 2) if dividend_yield != "N/A" else "N/A",
                    one_year_return
                ]
            })
            st.table(df)

            # Optional: Plot price trend
            st.line_chart(hist["Close"], use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
