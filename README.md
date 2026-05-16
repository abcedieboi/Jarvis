# Jarvis — Stock Market Intelligence Dashboard

A minimalist black-and-white stock market dashboard powered by AI using Groq and yfinance.

This project started as a personal hobby and a way to explore how AI agents work in real-world applications. It’s mainly driven by curiosity around how powerful modern AI has become and what can be built with it using simple tools and experimentation.

The project is still ongoing and continuously evolving as I learn more about AI, automation, and dashboard development. A lot of this was vibe-coded, so don’t expect everything to be perfect or production-ready yet. I'm still experimenting, improving the architecture, and thinking of new features to add over time.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your API key

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the app

```bash
python app.py
```

### 4. Open in browser

Go to:

```txt
http://localhost:5000
```

## Features

* Real-time stock prices via yfinance
  (AAPL, NVDA, MSFT, TSLA, GOOGL, META, AMZN, AMD)

* Market indices:

  * S&P 500
  * Nasdaq
  * Dow Jones
  * VIX

* Intraday S&P 500 chart

* 7-day mini trend bars per stock

* Groq AI chat (`llama-3.3-70b`) for market analysis

* Quick prompt buttons for common questions

* Auto-refresh every 60 seconds

## Notes

* yfinance is free and does not require an API key
* Groq’s free tier is generous and works well for experimentation
* Market data may have slight delays depending on trading hours
