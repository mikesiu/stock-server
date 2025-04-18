from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return {"error": "No data found"}
        latest_price = data['Close'].iloc[-1]
        return {"ticker": ticker.upper(), "price": round(latest_price, 2)}
    except Exception as e:
        return {"error": str(e)}
