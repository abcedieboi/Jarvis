# Jarvis — Stock Market Intelligence Dashboard

A minimalist black & white AI-powered stock dashboard using Groq + yfinance.

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Set up your API key
Copy `.env.example` to `.env` and add your Groq API key:
cp .env.example .env

Edit `.env`:

GROQ_API_KEY=your_groq_api_key_here

### 3. Run the app
python app.py

### 4. Open in browser
Go to: http://localhost:5000

## Features
- Real-time stock prices via yfinance (AAPL, NVDA, MSFT, TSLA, GOOGL, META, AMZN, AMD)
- Market indices: S&P 500, Nasdaq, Dow Jones, VIX
- Intraday S&P 500 chart
- 7-day mini trend bars per stock
- Groq AI chat (llama-3.3-70b) for market analysis
- Quick prompt buttons for common questions
- Auto-refreshes every 60 seconds

## File Structure
GROQ/
├── app.py              # Flask backend + Groq AI + yfinance
├── requirements.txt    # Python dependencies
├── .env                # Your API Key
└── templates/
    └── index.html      # Dashboard UI

## Notes
- yfinance is free with no API key needed
- Groq free tier is generous — should handle heavy usage
- Data may be slightly delayed depending on market hours