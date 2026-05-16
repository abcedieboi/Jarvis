from flask import Flask, render_template, jsonify, request
from groq import Groq
from dotenv import load_dotenv
import yfinance as yf
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

WATCHLIST = ["AAPL", "NVDA", "MSFT", "TSLA", "GOOGL", "META", "AMZN", "AMD"]
INDICES = ["^GSPC", "^IXIC", "^DJI", "^VIX"]
INDEX_NAMES = {"^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^DJI": "Dow Jones", "^VIX": "VIX"}

chat_history = []


def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="7d", interval="1d")
        info = stock.fast_info

        if hist.empty:
            return None

        current = round(info.last_price, 2)
        prev_close = round(info.previous_close, 2)
        change = round(current - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2)
        volume = info.three_month_average_volume

        closes = [round(c, 2) for c in hist["Close"].tolist()]

        return {
            "ticker": ticker,
            "price": current,
            "change": change,
            "change_pct": change_pct,
            "volume": volume,
            "history": closes,
            "up": change >= 0,
        }
    except Exception as e:
        return None


def get_index_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        current = round(info.last_price, 2)
        prev = round(info.previous_close, 2)
        change_pct = round(((current - prev) / prev) * 100, 2)
        return {
            "name": INDEX_NAMES.get(symbol, symbol),
            "value": current,
            "change_pct": change_pct,
            "up": change_pct >= 0,
        }
    except:
        return None


def get_intraday(symbol="^GSPC"):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="30m")
        labels = [t.strftime("%H:%M") for t in hist.index]
        prices = [round(p, 2) for p in hist["Close"].tolist()]
        return {"labels": labels, "prices": prices}
    except:
        return {"labels": [], "prices": []}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stocks")
def stocks():
    data = []
    for ticker in WATCHLIST:
        s = get_stock_data(ticker)
        if s:
            data.append(s)
    return jsonify(data)


@app.route("/api/indices")
def indices():
    data = []
    for symbol in INDICES:
        d = get_index_data(symbol)
        if d:
            data.append(d)
    return jsonify(data)


@app.route("/api/intraday")
def intraday():
    return jsonify(get_intraday())


@app.route("/api/chat", methods=["POST"])
def chat():
    global chat_history
    user_message = request.json.get("message", "")

    # Build market context for Jarvis
    stock_context = []
    for ticker in WATCHLIST[:4]:
        s = get_stock_data(ticker)
        if s:
            stock_context.append(
                f"{s['ticker']}: ${s['price']} ({'+' if s['up'] else ''}{s['change_pct']}%)"
            )

    system_prompt = f"""You are Jarvis, a sharp and confident AI stock market assistant. 
You speak concisely and intelligently — like a financial advisor who gets straight to the point.
Use bullet points for lists. Keep responses under 150 words unless asked for detail.
Never use excessive disclaimers. Be direct with analysis.

Current market snapshot:
{chr(10).join(stock_context)}

Today's date context: markets are currently active."""

    chat_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + chat_history[-10:],
        max_tokens=300,
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    global chat_history
    chat_history = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
