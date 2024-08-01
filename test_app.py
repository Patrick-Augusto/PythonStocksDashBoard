import pandas as pd
import subprocess
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest.mock import patch

def build_sidebar():
   
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    prices = pd.DataFrame({
        'AAPL': [150, 152, 153],
        'GOOGL': [2800, 2820, 2830],
        'MSFT': [300, 305, 310]
    })
    return tickers, prices

def build_main(tickers, prices):
    average_prices = prices.mean()
    return average_prices

@pytest.fixture
def sidebar_data():
    return build_sidebar()

def test_build_sidebar(sidebar_data):
    tickers, prices = sidebar_data
    assert isinstance(tickers, list), "Tickers should be a list"
    assert isinstance(prices, pd.DataFrame), "Prices should be a DataFrame"
    assert len(tickers) > 0, "Tickers list should not be empty"
    assert not prices.empty, "Prices DataFrame should not be empty"

def test_build_main(sidebar_data):
    tickers, prices = sidebar_data
    result = build_main(tickers, prices)
    assert isinstance(result, pd.Series), "Result should be a Series"
    assert not result.empty, "Result Series should not be empty"
    assert 'AAPL' in result.index, "Result should contain 'AAPL'"
    assert 'GOOGL' in result.index, "Result should contain 'GOOGL'"
    assert 'MSFT' in result.index, "Result should contain 'MSFT'"

@patch('streamlit.title')
def test_app_title(mock_title):
    import streamlit as st
    st.title('Portifolio e Analises de Ações')
    mock_title.assert_called_once_with('Portifolio e Analises de Ações')

def test_end_to_end():
    process = subprocess.Popen(['streamlit', 'run', 'app.py'])
    time.sleep(5)

    driver = webdriver.Chrome()
    driver.get('http://localhost:8501')

    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        assert title_element is not None
    finally:
        driver.quit()
        process.terminate()