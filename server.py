from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()

class RequestBody(BaseModel):
    input: str  # MCP trigger sends {"input": "some text"}

@app.post("/v1/completions")
async def mcp_stock_server(request: RequestBody):
    ticker = request.input.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return {"output": f"No data found for {ticker}"}
        latest_price = data['Close'].iloc[-1]
        return {"output": f"The latest price of {ticker} is {round(latest_price, 2)}"}
    except Exception as e:
        return {"output": f"Error fetching {ticker}: {str(e)}"}
