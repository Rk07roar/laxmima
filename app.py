from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Your NewsAPI key
NEWS_API_KEY = '3031c2e5709c4ead8ff45678845d6ece'

def get_stock_news(stock_symbol):
    # Construct the URL to fetch stock-related news using NewsAPI
    url = f'https://newsapi.org/v2/everything?q={stock_symbol}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        
        # Extract relevant information from the articles
        news_list = [{'title': article['title'], 'description': article['description'], 'url': article['url']} for article in articles[:5]]
        return news_list
    else:
        return [{'title': 'Error fetching news', 'description': 'Unable to fetch news at the moment.', 'url': '#'}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()

    # Function to safely get float values, defaulting to 0 if the value is empty or invalid
    def safe_float(value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    # Basic Stock Info
    todays_high = safe_float(data.get('todaysHigh', 0))
    todays_low = safe_float(data.get('todaysLow', 0))
    fifty_two_high = safe_float(data.get('fiftyTwoHigh', 0))
    fifty_two_low = safe_float(data.get('fiftyTwoLow', 0))
    open_circuit = safe_float(data.get('openCircuit', 0))
    prev_close = safe_float(data.get('prevClose', 0))
    volume = safe_float(data.get('volume', 0))
    trade_value = safe_float(data.get('tradeValue', 0))
    upper_circuit = safe_float(data.get('upperCircuit', 0))
    lower_circuit = safe_float(data.get('lowerCircuit', 0))

    # Analyst Estimates
    buy_percent = safe_float(data.get('buyPercent', 0))
    hold_percent = safe_float(data.get('holdPercent', 0))
    sell_percent = safe_float(data.get('sellPercent', 0))

    # Fundamental Data
    market_cap = safe_float(data.get('marketCap', 0))
    pe_ratio = safe_float(data.get('peRatio', 0))
    pb_ratio = safe_float(data.get('pbRatio', 0))
    industry_pe = safe_float(data.get('industryPE', 0))
    debt_equity = safe_float(data.get('debtEquity', 0))
    roe = safe_float(data.get('roe', 0))
    eps = safe_float(data.get('eps', 0))
    dividend_yield = safe_float(data.get('dividendYield', 0))
    book_value = safe_float(data.get('bookValue', 0))
    face_value = safe_float(data.get('faceValue', 0))

    # Fair value calculation
    fair_value = pe_ratio * eps
    target_price = round(fair_value * 1.15, 2)

    # Recommendation logic
    recommendation = "HOLD ⚠️"
    confidence = "🟡 Moderate"
    hold_period = "30-45 days"

    if (
        prev_close < fair_value * 0.85 and
        buy_percent > 50 and
        debt_equity < 1 and
        roe > 10 and
        pe_ratio < industry_pe
    ):
        recommendation = "BUY ✅"
        confidence = "🟢 High"
        hold_period = "60-90 days"
    elif prev_close > fair_value * 1.15 or sell_percent > 40:
        recommendation = "SELL ❌"
        confidence = "🔴 Low"
        hold_period = "Consider Exiting"

    # Return result
    return jsonify({
        "recommendation": recommendation,
        "targetSellPrice": f"₹{target_price}",
        "holdPeriod": hold_period,
        "confidence": confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
