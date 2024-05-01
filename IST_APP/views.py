from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

def stock_dashboard(request):
    stocks = [
        "GOOG", "MSFT", "AMZN", "TSLA", "NFLX", "KO", "PG", "JNJ", "V", "MA",
        "JPM", "BAC", "WMT", "HD", "PFE", "DIS", "NVDA", "VZ", "IBM", "ADBE",
        "XOM", "CVX", "MRK", "CSCO", "BA", "T", "GE", "ORCL", "CRM", "WFC",
        "GM", "PYPL", "COST", "SBUX", "MCD", "AMGN", "ABBV", "NKE", "INTC",
        "VOD", "ABT", "AIG", "QCOM", "UNH", "LLY", "UPS", "CVS", "LMT"
    ]
    return render(request, 'search.html', {'stocks': stocks})

def get_stock_data(request):
    selected_stock = request.GET.get('selected_stock')
    investment_amount = float(request.GET.get('investment_amount'))
    investing_days = int(request.GET.get('investing_days'))
    
    if not selected_stock:
        return JsonResponse({'error': 'Please select a stock.'}, status=400)

    data = load_stock_data(selected_stock)
    plot_div = generate_plot(data)

    # Analyze the closing price of today
    analysis_result = analyze_today_closing_price(data)

    # Perform investment analysis
    investment_analysis = calculate_investment_analysis(data, investment_amount, investing_days)

    # Get only the last 5 rows of the data
    last_5_data = data.tail(5)
    html_data = last_5_data.to_html()

    return JsonResponse({'data': html_data, 'plot_div': plot_div, 'analysis_result': analysis_result, 'investment_analysis': investment_analysis})

def load_stock_data(ticker):
    START = '2020-01-01'
    END = pd.Timestamp.today().strftime('%Y-%m-%d')
    data = yf.download(ticker, start=START, end=END)
    data.reset_index(inplace=True)
    data['Ticker'] = ticker
    return data

def generate_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Open', line=dict(color='red')))
    fig.update_layout(title_text='Time Series Data Visualization Over Past 4 Years', xaxis_title='Date', yaxis_title='Price')
    plot_div = fig.to_html(full_html=False)
    return plot_div

def analyze_today_closing_price(data):
    data['Yesterday_Close'] = data['Close'].shift(1)
    data.dropna(inplace=True)

    X = data[['Yesterday_Close']]
    y = data['Close']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Linear Regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict the closing price for today
    yesterday_close = X.iloc[-1]['Yesterday_Close']
    predicted_close = model.predict([[yesterday_close]])

    # Calculate RMSE and R-squared for test set
    y_pred_test = model.predict(X_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_test = sqrt(mse_test)
    r2_test = r2_score(y_test, y_pred_test)

    return {'predicted_today_close': predicted_close[0], 'rmse_test': rmse_test, 'r2_test': r2_test}

def calculate_investment_analysis(data, investment_amount, investing_days):
    yesterday_close = data['Close'].iloc[-1]
    predicted_today_close = analyze_today_closing_price(data)['predicted_today_close']
    
    stock_price = predicted_today_close
    num_stocks = investment_amount / stock_price

    future_date = pd.Timestamp.today() + pd.Timedelta(days=investing_days)
    end_date_future = future_date.strftime('%Y-%m-%d')

    try:
        future_price_change = yf.download(data['Ticker'].iloc[-1], start=data['Date'].iloc[-1], end=end_date_future)
        if not future_price_change.empty:
            future_price = future_price_change['Close'].iloc[-1]
            potential_profit_loss = (future_price - stock_price) * num_stocks
            full_amount_with_invest = future_price * num_stocks

            return {'num_stocks': num_stocks, 'potential_profit_loss': potential_profit_loss, 'full_amount_with_invest': full_amount_with_invest}, {'predicted_dates': predicted_dates, 'predicted_prices': predicted_prices}
        else:
            return {'error': 'Failed to fetch future price data.'}
    except Exception as e:
        return {'error': str(e)}
