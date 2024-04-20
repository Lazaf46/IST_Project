from django.shortcuts import render
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View
from django.http import HttpResponse


# Responsible for - Taking the request -> Responce

def index(request):
    return render(request, 'index.html')

def results(request):
    return render(request, 'results.html')




class StockView(View):

    def get(self, request):
        stocks = [
            "GOOG", "MSFT", "AMZN", "TSLA", "NFLX", "KO", "PG", "JNJ", "V", "MA",
            "JPM", "BAC", "WMT", "HD", "PFE", "DIS", "NVDA", "VZ", "IBM", "ADBE",
            "XOM", "CVX", "MRK", "CSCO", "BA", "T", "GE", "ORCL", "CRM", "WFC",
            "GM", "PYPL", "COST", "SBUX", "MCD", "AMGN", "ABBV", "NKE", "INTC",
            "VOD", "ABT", "AIG", "QCOM", "UNH", "LLY", "UPS", "CVS", "LMT"
        ]
        return render(request, 'search.html', {'stocks': stocks})

    @method_decorator(cache_page(60*15), name='dispatch')  # Cache for 15 minutes
    def post(self, request):
        selected_stock = request.POST.get('selected_stock')
        if not selected_stock:
            return HttpResponse("Please select a stock.")

        data = self.load_data(selected_stock)
        context = {
            'selected_stock': selected_stock,
            'data': data.to_html(),
            'plot_div': self.generate_plot(data),
        }
        return render(request, 'search.html', context)

    def load_data(self, ticker):
        START = '2020-01-01'
        END = pd.Timestamp.today().strftime('%Y-%m-%d')
        data = yf.download(ticker, start=START, end=END)
        return data

    def generate_plot(self, data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['Open'], mode='lines', name='Open', line=dict(color='red')))
        fig.update_layout(title_text='Time Series Data Visualisation', xaxis_title='Date', yaxis_title='Price')
        plot_div = fig.to_html(full_html=False)
        return plot_div
