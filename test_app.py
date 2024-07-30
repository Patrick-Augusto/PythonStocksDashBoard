import pytest
import pandas as pd
from app import build_main, build_sidebar

@pytest.fixture
def sample_data():
    tickers = ['AAPL', 'MSFT']
    prices = pd.DataFrame({
        'AAPL': [150, 152, 153],
        'MSFT': [250, 252, 253]
    })
    return tickers, prices

def test_build_sidebar():
    tickers, prices = build_sidebar()
    assert isinstance(tickers, list)
    assert isinstance(prices, pd.DataFrame)

def test_build_main(sample_data):
    tickers, prices = sample_data
    build_main(tickers, prices)
   

def test_app_title():
    import streamlit as st
    st.title('Portifolio e Analises de Ações')
    assert st._main.title == 'Portifolio e Analises de Ações'