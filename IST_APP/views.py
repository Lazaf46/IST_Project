# views.py

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

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
    if not selected_stock:
        return JsonResponse({'error': 'Please select a stock.'}, status=400)

    data = load_stock_data(selected_stock)
    plot_div = generate_plot(data)

    # Get only the last 5 rows of the data
    last_5_data = data.tail(5)
    html_data = last_5_data.to_html()
    

    return JsonResponse({'data': html_data, 'plot_div': plot_div})

def load_stock_data(ticker):
    START = '2020-01-01'
    END = pd.Timestamp.today().strftime('%Y-%m-%d')
    data = yf.download(ticker, start=START, end=END)
    data.reset_index(inplace=True)
    return data

def generate_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], mode='lines', name='Open', line=dict(color='red')))
    fig.update_layout(title_text='Time Series Data Visualization', xaxis_title='Date', yaxis_title='Price')
    plot_div = fig.to_html(full_html=False)
    return plot_div
